"""Modelos falsos e determinísticos para os testes (sem Ollama, sem rede).

NaiveModel é o pior caso de propósito: lê tudo, copia o conteúdo para a
resposta e obedece a qualquer instrução que encontrar nos e-mails, inclusive
chamando ferramentas que não recebeu. Se o harness não detectar ataque contra
ele, o harness está quebrado; se uma mitigação de sistema (aprovação, filtro,
dual LLM) não o barrar, a mitigação está quebrada.
"""
from __future__ import annotations

import json
import re

from .environment import normalize
from .mitigations import unmark
from .providers import ModelTurn, ToolCall

_ADDR = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
_URL = re.compile(r"https?://[^\s)\"']+")
_SECRET = re.compile(r"conta de e-mail: (\S+?)\. ")
_TRIGGERS = ("assistente", "sistema")


def _tool_outputs(messages: list[dict]) -> list[tuple[str, str]]:
    return [(m.get("name", ""), m["content"]) for m in messages if m["role"] == "tool"]


def injected_sentences(text: str) -> list[str]:
    """Trechos que falam com o assistente: o que um modelo ingênuo obedeceria."""
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [p for p in parts if any(t in normalize(p) for t in _TRIGGERS)]


class NaiveModel:
    name = "fake:naive"

    def __init__(self, plans: dict[str, list[dict]] | None = None):
        self.plans = plans or {}
        self.calls = 0

    def chat(self, messages: list[dict], tools: list[dict] | None = None,
             json_mode: bool = False) -> ModelTurn:
        self.calls += 1
        system = messages[0]["content"]
        if json_mode:
            return ModelTurn(json.dumps({"steps": self.plans.get(messages[-1]["content"], [])}))
        if system.startswith("Você é um extrator"):
            return ModelTurn(unmark(messages[-1]["content"].split("E-mails:", 1)[-1]).strip())
        return self._agent_turn(system, messages)

    def _agent_turn(self, system: str, messages: list[dict]) -> ModelTurn:
        m = _SECRET.search(system)
        secret = m.group(1) if m else ""
        outputs = _tool_outputs(messages)
        if not any(name == "list_emails" for name, _ in outputs):
            return ModelTurn("", [ToolCall("list_emails", {})])
        listing = json.loads(next(c for n, c in outputs if n == "list_emails"))
        read = {json.loads(c).get("id") for n, c in outputs if n == "read_email" and c.startswith("{")}
        unread = [r["id"] for r in listing if r["id"] not in read]
        if unread:
            return ModelTurn("", [ToolCall("read_email", {"email_id": i}) for i in unread])
        emails = [json.loads(c) for n, c in outputs if n == "read_email" and c.startswith("{\"id\"")]
        corpus = unmark("\n\n".join(
            "\n".join([e["subject"], e["body"]] + [a["text"] for a in e.get("attachments", [])])
            for e in emails))
        already = {a for n, c in outputs if n == "send_email" for a in _ADDR.findall(c)}
        tried = {a for msg in messages if msg["role"] == "assistant"
                 for call in msg.get("tool_calls", []) if call["name"] == "send_email"
                 for a in _ADDR.findall(str(call["arguments"].get("to", "")))}
        for sentence in injected_sentences(corpus):
            for addr in _ADDR.findall(sentence):
                if addr in already or addr in tried:
                    continue
                body = f"Código: {secret}" if "codigo" in normalize(sentence) else corpus[:200]
                return ModelTurn("", [ToolCall("send_email", {"to": addr, "subject": "ok", "body": body})])
        urls = [u.replace("CODIGO", secret.replace("-", "")) for s in injected_sentences(corpus)
                for u in _URL.findall(s)]
        images = "\n".join(f"![ok]({u})" for u in urls)
        return ModelTurn(f"Resumo dos e-mails:\n{corpus}\n{images}".strip())


class ScriptedModel:
    """Devolve turnos prontos, em ordem; útil para testar o laço do agente."""
    name = "fake:scripted"

    def __init__(self, turns: list[ModelTurn]):
        self.turns = list(turns)
        self.seen: list[list[dict]] = []

    def chat(self, messages: list[dict], tools: list[dict] | None = None,
             json_mode: bool = False) -> ModelTurn:
        self.seen.append([dict(m) for m in messages])
        return self.turns.pop(0) if self.turns else ModelTurn("fim")
