"""Catálogo somente leitura dos artefatos do agentic-lab.

Não depende do MCP: pode ser testado e reutilizado sozinho. O servidor
(`server.py`) só expõe estas funções como tools, resources e prompts.
"""
from __future__ import annotations

import os
import pathlib
import re
import unicodedata
from dataclasses import dataclass, field

SCOPES = ("learn", "build", "cases", "ops/decisions")
MAX_BYTES = 200_000
ALLOWED_SUFFIXES = {".md"}


class AccessDenied(ValueError):
    """Caminho fora do que o servidor aceita ler."""


@dataclass(frozen=True)
class Artifact:
    path: str
    tipo: str
    maturidade: str
    versao: str
    title: str
    summary: str
    tags: tuple[str, ...] = ()
    body: str = field(default="", repr=False)

    def card(self) -> dict:
        return {
            "path": self.path,
            "title": self.title,
            "tipo": self.tipo,
            "maturidade": self.maturidade,
            "versao": self.versao,
            "tags": list(self.tags),
            "summary": self.summary,
            "uri": f"repo://artifact/{self.path}",
        }


def default_root() -> pathlib.Path:
    env = os.environ.get("REPO_ROOT")
    if env:
        return pathlib.Path(env).resolve()
    # build/mcp-servers/repo-knowledge/repo_knowledge_server/catalog.py -> raiz do repo
    return pathlib.Path(__file__).resolve().parents[4]


def _fold(text: str) -> str:
    """Minúsculas e sem acento, para a busca não depender de grafia."""
    norm = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in norm if not unicodedata.combining(c))


def _tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", _fold(text)) if len(t) > 1]


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    data: dict[str, object] = {}
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return data, "\n".join(lines[i + 1:])
        key, sep, raw = line.partition(":")
        if not sep:
            continue
        value = raw.strip()
        if value.startswith("[") and value.endswith("]"):
            data[key.strip()] = [v.strip() for v in value[1:-1].split(",") if v.strip()]
        else:
            data[key.strip()] = value
    return {}, text  # front-matter sem fechamento: trata como texto puro


def _title(body: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", body, flags=re.M)
    return match.group(1).strip() if match else fallback


def _summary(body: str, limit: int = 240) -> str:
    """Primeiro parágrafo de '## Objetivo' ou, se não houver, do texto."""
    section = re.search(r"^##\s+Objetivo\s*$(.*?)(?=^##\s|\Z)", body, flags=re.M | re.S)
    source = section.group(1) if section else re.sub(r"^#.*$", "", body, flags=re.M)
    for para in re.split(r"\n\s*\n", source):
        text = " ".join(para.split())
        if text and not text.startswith(("|", "```", "-", ">")):
            return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"
    return ""


class Catalog:
    def __init__(self, root: pathlib.Path | None = None) -> None:
        self.root = (root or default_root()).resolve()
        self._items: dict[str, Artifact] | None = None

    # ---------- segurança ----------
    def safe_path(self, rel: str) -> pathlib.Path:
        """Resolve um caminho relativo garantindo que fica dentro do repo."""
        if not rel or "\x00" in rel:
            raise AccessDenied("caminho vazio ou inválido")
        rel = rel.replace("\\", "/").strip()
        candidate = pathlib.PurePosixPath(rel)
        if candidate.is_absolute() or re.match(r"^[A-Za-z]:", rel) or ".." in candidate.parts:
            raise AccessDenied("só caminhos relativos dentro do repositório")
        if any(part.startswith(".") for part in candidate.parts):
            raise AccessDenied("arquivos e pastas ocultos não são expostos")
        if candidate.suffix not in ALLOWED_SUFFIXES:
            raise AccessDenied("só arquivos .md são expostos")
        if not any(rel == s or rel.startswith(s + "/") for s in SCOPES) and "/" in rel:
            raise AccessDenied(f"fora das pastas expostas: {', '.join(SCOPES)}")
        full = (self.root / rel).resolve()
        if self.root not in full.parents:
            raise AccessDenied("caminho fora do repositório")
        if not full.is_file():
            raise FileNotFoundError(rel)
        if full.stat().st_size > MAX_BYTES:
            raise AccessDenied(f"arquivo maior que {MAX_BYTES} bytes")
        return full

    # ---------- leitura ----------
    def _load(self) -> dict[str, Artifact]:
        items: dict[str, Artifact] = {}
        for scope in SCOPES:
            base = self.root / scope
            if not base.exists():
                continue
            for file in sorted(base.rglob("*.md")):
                rel = file.relative_to(self.root).as_posix()
                if any(p.startswith(".") for p in pathlib.PurePosixPath(rel).parts):
                    continue
                if file.stat().st_size > MAX_BYTES:
                    continue
                fm, body = parse_frontmatter(file.read_text(encoding="utf-8"))
                if not fm:
                    continue
                tags = fm.get("tags", [])
                items[rel] = Artifact(
                    path=rel,
                    tipo=str(fm.get("tipo", "")),
                    maturidade=str(fm.get("maturidade", "")),
                    versao=str(fm.get("versao", "")),
                    title=_title(body, rel),
                    summary=_summary(body),
                    tags=tuple(tags) if isinstance(tags, list) else (),
                    body=body,
                )
        return items

    @property
    def items(self) -> dict[str, Artifact]:
        if self._items is None:
            self._items = self._load()
        return self._items

    def refresh(self) -> None:
        self._items = None

    def read(self, rel: str) -> str:
        return self.safe_path(rel).read_text(encoding="utf-8")

    # ---------- consulta ----------
    def filter(self, tipo: str | None = None, maturidade: str | None = None, tag: str | None = None) -> list[Artifact]:
        out = []
        for a in self.items.values():
            if tipo and a.tipo != tipo:
                continue
            if maturidade and a.maturidade != maturidade:
                continue
            if tag and _fold(tag) not in {_fold(t) for t in a.tags}:
                continue
            out.append(a)
        return out

    def search(self, query: str, tipo: str | None = None, maturidade: str | None = None,
               tag: str | None = None, limit: int = 10) -> list[tuple[float, Artifact]]:
        terms = _tokens(query)
        if not terms:
            return []
        scored = []
        for a in self.filter(tipo, maturidade, tag):
            title, meta, body = _tokens(a.title), _tokens(" ".join((a.path, *a.tags))), _tokens(a.body)
            score = 0.0
            for t in terms:
                score += 3 * title.count(t) + 2 * meta.count(t) + min(body.count(t), 5) * 0.5
            if score > 0:
                scored.append((score, a))
        scored.sort(key=lambda x: (-x[0], x[1].path))
        return scored[: max(1, min(limit, 50))]

    def index_markdown(self, tipo: str) -> str:
        rows = self.filter(tipo=tipo)
        if not rows:
            return f"Nenhum artefato do tipo `{tipo}` ainda."
        lines = [f"# Índice: {tipo}", "", "| Artefato | Maturidade | Versão | Resumo |", "|---|---|---|---|"]
        for a in rows:
            lines.append(f"| [{a.title}](repo://artifact/{a.path}) | {a.maturidade} | {a.versao} | {a.summary.replace('|', '/')} |")
        return "\n".join(lines)
