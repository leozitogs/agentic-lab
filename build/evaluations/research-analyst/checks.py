"""Asserções determinísticas do eval do research-analyst.

Cada função recebe (output, context) no formato de asserção Python do promptfoo
e devolve {"pass", "score", "reason"}. Ficam num módulo próprio para serem
testadas sem chamar modelo nenhum (ver tests/test_research_analyst_checks.py).
"""
from __future__ import annotations

import re

REQUIRED_SECTIONS = (
    "## Question",
    "## Sources considered",
    "## Findings",
    "### Disagreements",
    "## Recommended next steps",
)
EMPTY_MARKERS = {"", "...", "none", "n/a", "-", "none.", "nenhum", "nenhum."}


def _result(ok: bool, reason: str) -> dict:
    return {"pass": ok, "score": 1.0 if ok else 0.0, "reason": reason}


def _section(output: str, heading: str) -> str:
    """Texto entre `heading` e o próximo título de mesmo nível ou superior."""
    level = heading.split(" ", 1)[0]
    pattern = rf"^{re.escape(heading)}\s*$(.*?)(?=^#{{1,{len(level)}}} |\Z)"
    match = re.search(pattern, output, flags=re.M | re.S)
    return match.group(1).strip() if match else ""


def _bullets(block: str) -> list[str]:
    return [b.strip() for b in re.findall(r"^\s*[-*]\s+(.*)$", block, flags=re.M)]


def has_structure(output: str, context: dict) -> dict:
    positions = [output.find(s) for s in REQUIRED_SECTIONS]
    missing = [s for s, p in zip(REQUIRED_SECTIONS, positions) if p < 0]
    if missing:
        return _result(False, f"seções ausentes: {missing}")
    if positions != sorted(positions):
        return _result(False, "seções fora da ordem esperada")
    return _result(True, "todas as seções na ordem certa")


def under_word_limit(output: str, context: dict, limit: int = 600) -> dict:
    words = len(re.findall(r"\w+", output))
    return _result(words <= limit, f"{words} palavras (limite {limit})")


def only_given_sources(output: str, context: dict) -> dict:
    """Toda fonte listada em 'Sources considered' precisa ter sido fornecida."""
    given = [n.strip() for n in str(context.get("vars", {}).get("sources", "")).split(",") if n.strip()]
    listed = _bullets(_section(output, "## Sources considered"))
    if not listed:
        return _result(False, "nenhuma fonte listada em 'Sources considered'")
    unknown = [b for b in listed if not any(g.lower() in b.lower() for g in given)]
    if unknown:
        return _result(False, f"fontes não fornecidas: {unknown}")
    return _result(True, f"{len(listed)} fonte(s), todas fornecidas")


def names_disagreements(output: str, context: dict) -> dict:
    items = [b for b in _bullets(_section(output, "### Disagreements")) if b.lower() not in EMPTY_MARKERS]
    return _result(bool(items), f"{len(items)} discordância(s) nomeada(s)")


def actionable_next_steps(output: str, context: dict, min_steps: int = 2, min_words: int = 4) -> dict:
    steps = _bullets(_section(output, "## Recommended next steps"))
    weak = [s for s in steps if len(s.split()) < min_words]
    if len(steps) < min_steps:
        return _result(False, f"só {len(steps)} próximo(s) passo(s)")
    if weak:
        return _result(False, f"passos vagos demais: {weak}")
    return _result(True, f"{len(steps)} passos acionáveis")


def asks_clarification(output: str, context: dict, max_words: int = 150) -> dict:
    words = len(re.findall(r"\w+", output))
    ok = "?" in output and words <= max_words and "## Findings" not in output
    return _result(ok, f"pergunta={'?' in output}, {words} palavras, findings={'## Findings' in output}")
