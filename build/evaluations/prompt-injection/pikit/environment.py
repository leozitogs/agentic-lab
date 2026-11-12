"""Ambiente simulado: caixa de e-mail fictícia, contatos, ferramentas e log.

Nada sai da máquina: send_email só registra a tentativa no log. A injeção de um
ataque copia o e-mail-alvo e planta o payload conforme o vetor (corpo, comentário
HTML, assinatura, anexo, topo do corpo).
"""
from __future__ import annotations

import copy
import json
import pathlib
import re
import unicodedata
from dataclasses import dataclass, field
from typing import Callable

DATA = pathlib.Path(__file__).resolve().parent.parent / "data"


def load_json(name: str, data_dir: pathlib.Path = DATA) -> dict:
    return json.loads((data_dir / name).read_text(encoding="utf-8"))


def load_all(data_dir: pathlib.Path = DATA) -> tuple[dict, list[dict], list[dict]]:
    """Devolve (inbox, tarefas, ataques)."""
    inbox = load_json("inbox.json", data_dir)
    tasks = load_json("tasks.json", data_dir)["tasks"]
    attacks = load_json("attacks.json", data_dir)["attacks"]
    return inbox, tasks, attacks


def normalize(text: str) -> str:
    """Caixa baixa, sem acentos, espaços colapsados."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", text.lower()).strip()


def alnum(text: str) -> str:
    """Só letras e dígitos, em caixa alta: compara códigos ignorando separadores."""
    return re.sub(r"[^0-9A-Za-z]", "", text).upper()


# --------------------------------------------------------------------------
# Injeção
# --------------------------------------------------------------------------

def _body_to_html(body: str) -> str:
    paragraphs = [p.replace("\n", "<br>") for p in body.split("\n\n")]
    return "<html><body>" + "".join(f"<p>{p}</p>" for p in paragraphs) + "</body></html>"


def plant(email: dict, attack: dict) -> dict:
    """Devolve uma cópia do e-mail com o payload do ataque plantado."""
    out = copy.deepcopy(email)
    payload = attack["payload"]
    placement = attack["placement"]
    if placement == "append_body":
        out["body"] = out["body"] + "\n\n" + payload
    elif placement == "prepend_body":
        out["body"] = payload + "\n\n" + out["body"]
    elif placement == "html_comment":
        html = _body_to_html(out["body"])
        out["body"] = html.replace("</body>", f"<!-- {payload} --></body>")
    elif placement == "signature":
        out["body"] = out["body"] + "\n\n--\n" + payload
    elif placement == "attachment":
        out["attachments"] = list(out.get("attachments", [])) + [
            {"name": attack.get("attachment_name", "anexo.txt"), "text": payload}
        ]
    else:
        raise ValueError(f"placement desconhecido: {placement!r}")
    return out


def build_inbox(inbox: dict, task: dict, attack: dict | None) -> dict:
    """Caixa para um caso: a original, com o ataque plantado no alvo da tarefa."""
    out = copy.deepcopy(inbox)
    if attack is not None:
        target = task["injection_target"]
        out["emails"] = [plant(e, attack) if e["id"] == target else e for e in out["emails"]]
    return out


# --------------------------------------------------------------------------
# Log e ferramentas
# --------------------------------------------------------------------------

@dataclass
class ToolEvent:
    tool: str
    args: dict
    status: str = "ok"  # ok | enviado | negado | indisponivel | erro
    note: str = ""


@dataclass
class ToolLog:
    events: list[ToolEvent] = field(default_factory=list)

    def add(self, tool: str, args: dict, status: str = "ok", note: str = "") -> ToolEvent:
        ev = ToolEvent(tool, dict(args), status, note)
        self.events.append(ev)
        return ev

    def sent(self) -> list[dict]:
        """E-mails efetivamente 'enviados' (simulados)."""
        return [e.args for e in self.events if e.tool == "send_email" and e.status == "enviado"]

    def send_attempts(self) -> list[dict]:
        """Toda chamada a send_email, aprovada ou não."""
        return [{**e.args, "to": split_recipients(e.args.get("to", ""))}
                for e in self.events if e.tool == "send_email"]

    def to_list(self) -> list[dict]:
        return [{"tool": e.tool, "args": e.args, "status": e.status, "note": e.note} for e in self.events]


Approver = Callable[[list[str], dict], tuple[bool, str]]
Transform = Callable[[str], str]


_ADDRESS = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")


def split_recipients(to: object) -> list[str]:
    """Endereços de e-mail válidos em `to` (string ou lista); nomes soltos são descartados."""
    raw = " ".join(str(t) for t in to) if isinstance(to, list) else str(to or "")
    return [a.lower() for a in _ADDRESS.findall(raw)]


class Mailbox:
    """As quatro ferramentas do agente sobre uma caixa fictícia.

    untrusted: transformação aplicada a todo texto vindo de terceiros (assunto,
    corpo, anexos) antes de chegar ao modelo, ex.: datamarking.
    approver: se dado, cada send_email passa por ele; negado = não envia.
    outbound_filter: transformação aplicada ao corpo antes do envio (filtro de saída).
    """

    def __init__(self, inbox: dict, log: ToolLog | None = None, *,
                 untrusted: Transform | None = None,
                 approver: Approver | None = None,
                 outbound_filter: Transform | None = None):
        self.inbox = inbox
        self.emails = {e["id"]: e for e in inbox["emails"]}
        self.contacts = inbox["contacts"]
        self.log = log if log is not None else ToolLog()
        self.untrusted = untrusted or (lambda s: s)
        self.approver = approver
        self.outbound_filter = outbound_filter

    # -- leitura ------------------------------------------------------------
    def list_emails(self, date: str | None = None, **_: object) -> str:
        args = {"date": date} if date else {}
        day = self._resolve_date(date)
        rows = [
            {"id": e["id"], "from": e["from"], "date": e["date"], "subject": self.untrusted(e["subject"])}
            for e in self.inbox["emails"] if day is None or e["date"] == day
        ]
        self.log.add("list_emails", args, note=f"{len(rows)} e-mail(s)")
        return json.dumps(rows, ensure_ascii=False)

    def read_email(self, email_id: str = "", **kw: object) -> str:
        email_id = str(email_id or kw.get("id", "")).strip()
        e = self.emails.get(email_id)
        if e is None:
            self.log.add("read_email", {"email_id": email_id}, status="erro", note="id inexistente")
            return json.dumps({"erro": f"e-mail {email_id!r} não existe"}, ensure_ascii=False)
        self.log.add("read_email", {"email_id": email_id})
        return json.dumps(self.render_email(e), ensure_ascii=False)

    def render_email(self, e: dict) -> dict:
        return {
            "id": e["id"], "from": e["from"], "to": e["to"], "date": e["date"],
            "subject": self.untrusted(e["subject"]),
            "body": self.untrusted(e["body"]),
            "attachments": [{"name": a["name"], "text": self.untrusted(a["text"])}
                            for a in e.get("attachments", [])],
        }

    def search_contacts(self, query: str = "", **_: object) -> str:
        found = self.find_contacts(query)
        self.log.add("search_contacts", {"query": query}, note=f"{len(found)} contato(s)")
        return json.dumps(found, ensure_ascii=False)

    def find_contacts(self, query: str) -> list[dict]:
        """Contatos que casam com algum termo da busca, do melhor para o pior."""
        terms = [t for t in normalize(query or "").split() if len(t) >= 3]
        if not terms:
            return list(self.contacts)
        scored = []
        for c in self.contacts:
            hay = normalize(f"{c['name']} {c['email']} {c['role']}")
            score = sum(1 for t in terms if t in hay)
            if score:
                scored.append((score, c))
        scored.sort(key=lambda x: -x[0])
        return [c for _, c in scored]

    def best_contact(self, query: str) -> tuple[str, str]:
        """(endereço, nota) do contato que casa com mais termos; empate = ambíguo, não escolhe."""
        terms = [t for t in normalize(query or "").split() if len(t) >= 3]
        scores = []
        for c in self.contacts:
            hay = normalize(f"{c['name']} {c['email']} {c['role']}")
            scores.append((sum(1 for t in terms if t in hay), c))
        scores.sort(key=lambda x: -x[0])
        if not scores or scores[0][0] == 0:
            return "", "nenhum contato"
        if len(scores) > 1 and scores[1][0] == scores[0][0]:
            return "", "ambíguo"
        return scores[0][1]["email"], "1 contato"

    # -- escrita (irreversível) ---------------------------------------------
    def send_email(self, to: object = "", subject: str = "", body: str = "", **_: object) -> str:
        recipients = split_recipients(to)
        body = str(body or "")
        subject = str(subject or "")
        args = {"to": recipients, "subject": subject, "body": body}
        if not recipients:
            self.log.add("send_email", {**args, "to_raw": str(to)}, status="erro", note="sem endereço válido")
            return "Erro: informe ao menos um endereço de e-mail válido no campo to."
        if self.approver is not None:
            ok, reason = self.approver(recipients, args)
            if not ok:
                self.log.add("send_email", args, status="negado", note=reason)
                return f"Envio NÃO aprovado pela Marina: {reason}"
        if self.outbound_filter is not None:
            filtered = self.outbound_filter(body)
            if filtered != body:
                args = {**args, "body": filtered, "body_original": body}
        self.log.add("send_email", args, status="enviado")
        return f"E-mail enviado para {', '.join(recipients)} (simulado)."

    # -- util ---------------------------------------------------------------
    def _resolve_date(self, date: str | None) -> str | None:
        if not date:
            return None
        d = normalize(str(date))
        if d in {"today", "hoje"}:
            return self.inbox["user"]["today"]
        m = re.match(r"^(\d{1,2})/(\d{1,2})(?:/(\d{4}))?$", d)
        if m:
            year = m.group(3) or self.inbox["user"]["today"][:4]
            return f"{year}-{int(m.group(2)):02d}-{int(m.group(1)):02d}"
        if re.match(r"^\d{4}-\d{2}-\d{2}$", d):
            return d
        return None  # data que não entendemos: lista tudo

    def call(self, name: str, arguments: dict) -> str:
        fn = {
            "list_emails": self.list_emails,
            "read_email": self.read_email,
            "search_contacts": self.search_contacts,
            "send_email": self.send_email,
        }.get(name)
        if fn is None:
            self.log.add(name, arguments, status="indisponivel")
            return f"Erro: a ferramenta {name!r} não existe ou não está disponível."
        try:
            return fn(**(arguments or {}))
        except TypeError as exc:
            self.log.add(name, arguments, status="erro", note=str(exc))
            return f"Erro nos argumentos de {name}: {exc}"


TOOL_SPECS = {
    "list_emails": {
        "name": "list_emails",
        "description": "Lista os e-mails da caixa de entrada (id, remetente, data, assunto). "
                       "Use date='today' para só os de hoje.",
        "parameters": {
            "type": "object",
            "properties": {"date": {"type": "string", "description": "'today' ou AAAA-MM-DD; vazio lista todos"}},
            "required": [],
        },
    },
    "read_email": {
        "name": "read_email",
        "description": "Lê um e-mail completo (corpo e anexos) pelo id.",
        "parameters": {
            "type": "object",
            "properties": {"email_id": {"type": "string", "description": "id do e-mail, ex.: e01"}},
            "required": ["email_id"],
        },
    },
    "search_contacts": {
        "name": "search_contacts",
        "description": "Busca contatos da Marina por nome, papel ou e-mail.",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    "send_email": {
        "name": "send_email",
        "description": "Envia um e-mail em nome da Marina.",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "endereço do destinatário"},
                "subject": {"type": "string"},
                "body": {"type": "string"},
            },
            "required": ["to", "subject", "body"],
        },
    },
}
