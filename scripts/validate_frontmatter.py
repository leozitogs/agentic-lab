"""Valida o front-matter dos artefatos do agentic-lab contra ops/TAGS.md.

Uso:
    python scripts/validate_frontmatter.py            # valida o repositório
    python scripts/validate_frontmatter.py ARQ.md ... # valida só os arquivos dados

Sai com código 1 se algum arquivo violar as regras. Usa só a biblioteca padrão.
"""
from __future__ import annotations

import datetime as dt
import pathlib
import re
import sys
from dataclasses import dataclass

ROOT = pathlib.Path(__file__).resolve().parent.parent

SCOPES = ("learn", "build", "cases", "ops/decisions")
COMPANION_FILES = {"examples.md", "references.md", "tests.md"}
EXEMPT_PATHS = {"cases/README.md"}

REQUIRED = ("tipo", "maturidade", "versao", "autores", "criado_em", "atualizado_em")
TIPOS = {"prompt", "skill", "mcp", "eval", "case", "note", "adr", "guide"}
MATURIDADES = {"draft", "tested", "reviewed", "adopted"}
ADR_STATUS = {"proposto", "aceito", "substituido", "descartado"}

# Onde cada tipo pode morar (prefixos relativos à raiz).
HOMES = {
    "prompt": ("build/prompts/",),
    "skill": ("build/skills/",),
    "mcp": ("build/mcp-servers/",),
    "eval": ("build/evaluations/",),
    "case": ("cases/",),
    "note": ("learn/notes/",),
    "adr": ("ops/decisions/",),
    # guias didáticos moram em learn/; catálogos (ex.: prompt-library.md) em build/
    "guide": ("learn/", "build/"),
}

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
DATE_PLACEHOLDER = "YYYY-MM-DD"


@dataclass
class Problem:
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


def parse_frontmatter(text: str) -> dict[str, object] | None:
    """Lê o bloco YAML simples do topo do arquivo (chave: valor, listas [a, b])."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    data: dict[str, object] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return data
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"linha de front-matter sem ':' -> {line!r}")
        key, _, raw = line.partition(":")
        value = raw.strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key.strip()] = [v.strip() for v in inner.split(",") if v.strip()] if inner else []
        else:
            data[key.strip()] = value
    raise ValueError("front-matter aberto com '---' mas nunca fechado")


def is_template(rel: str) -> bool:
    return "TEMPLATE" in rel or "-template/" in rel


def requires_frontmatter(rel: str) -> bool:
    if rel in EXEMPT_PATHS:
        return False
    return pathlib.PurePosixPath(rel).name not in COMPANION_FILES


def parse_date(value: object) -> dt.date | None:
    try:
        return dt.date.fromisoformat(str(value))
    except ValueError:
        return None


def validate_file(path: pathlib.Path, root: pathlib.Path = ROOT) -> list[Problem]:
    rel = path.relative_to(root).as_posix()
    problems: list[Problem] = []

    def bad(msg: str) -> None:
        problems.append(Problem(rel, msg))

    try:
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        bad(str(exc))
        return problems

    if fm is None:
        if requires_frontmatter(rel):
            bad("sem front-matter (ver ops/TAGS.md)")
        return problems

    for key in REQUIRED:
        if key not in fm or fm[key] in ("", None):
            bad(f"campo obrigatório ausente: {key}")
    if problems:
        return problems

    tipo, maturidade = str(fm["tipo"]), str(fm["maturidade"])
    if tipo not in TIPOS:
        bad(f"tipo inválido: {tipo!r} (use um de {sorted(TIPOS)})")
    if maturidade not in MATURIDADES:
        bad(f"maturidade inválida: {maturidade!r} (use um de {sorted(MATURIDADES)})")
    if not SEMVER.match(str(fm["versao"])):
        bad(f"versao fora do padrão X.Y.Z: {fm['versao']!r}")
    if not isinstance(fm["autores"], list) or not fm["autores"]:
        bad("autores deve ser uma lista não vazia, ex.: [nome]")

    template = is_template(rel)
    dates = {}
    for key in ("criado_em", "atualizado_em"):
        value = fm[key]
        if template and value == DATE_PLACEHOLDER:
            continue
        parsed = parse_date(value)
        if parsed is None:
            bad(f"{key} não é uma data AAAA-MM-DD: {value!r}")
        else:
            dates[key] = parsed
    if len(dates) == 2 and dates["atualizado_em"] < dates["criado_em"]:
        bad("atualizado_em é anterior a criado_em")

    if tipo in HOMES and not template and not rel.startswith(HOMES[tipo]):
        bad(f"tipo {tipo!r} deveria morar em {', '.join(HOMES[tipo])}")

    if tipo == "adr":
        status = fm.get("status")
        if status is None and not template:
            bad("ADR sem campo status")
        elif status is not None and not template and status not in ADR_STATUS:
            bad(f"status de ADR inválido: {status!r} (use um de {sorted(ADR_STATUS)})")

    nota = fm.get("nota_avaliacao")
    if nota not in (None, "null"):
        try:
            if not 0 <= int(str(nota)) <= 100:
                raise ValueError
        except ValueError:
            bad(f"nota_avaliacao deve ser inteiro de 0 a 100: {nota!r}")

    return problems


def collect(root: pathlib.Path = ROOT) -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for scope in SCOPES:
        base = root / scope
        if base.exists():
            files.extend(sorted(base.rglob("*.md")))
    return files


def main(argv: list[str]) -> int:
    targets = [pathlib.Path(a).resolve() for a in argv] if argv else collect()
    targets = [t for t in targets if t.suffix == ".md"]
    problems = [p for t in targets for p in validate_file(t)]
    for p in problems:
        print(f"ERRO  {p}")
    print(f"{len(targets)} arquivo(s) verificados, {len(problems)} problema(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
