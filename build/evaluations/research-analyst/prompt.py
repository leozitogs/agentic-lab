"""Monta as mensagens do research-analyst a partir da fonte única do prompt.

O system prompt NÃO é copiado aqui: ele é lido do bloco ```txt de
build/prompts/system/research-analyst.md, para que o eval sempre teste a versão
que está no repositório.
"""
from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[3]
PROMPT_DOC = ROOT / "build" / "prompts" / "system" / "research-analyst.md"
FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures"


def system_prompt() -> str:
    text = PROMPT_DOC.read_text(encoding="utf-8")
    match = re.search(r"## Prompt\s+```txt\n(.*?)\n```", text, flags=re.S)
    if not match:
        raise ValueError(f"bloco ```txt não encontrado em {PROMPT_DOC}")
    return match.group(1).strip()


def load_sources(names: str) -> str:
    """Lê as fontes sintéticas listadas em `names` (separadas por vírgula)."""
    blocks = []
    for name in [n.strip() for n in names.split(",") if n.strip()]:
        body = (FIXTURES / f"{name}.txt").read_text(encoding="utf-8").strip()
        blocks.append(f"<source name=\"{name}\">\n{body}\n</source>")
    return "\n\n".join(blocks)


def user_message(question: str, sources: str) -> str:
    q = question.strip() or "(no question provided)"
    s = load_sources(sources) if sources.strip() else "(no sources provided)"
    return f"# Question\n{q}\n\n# Sources\n{s}"


def research_analyst(context: dict) -> str:
    """Função de prompt do promptfoo: devolve a conversa em JSON."""
    v = context.get("vars", {})
    messages = [
        {"role": "system", "content": system_prompt()},
        {"role": "user", "content": user_message(v.get("question", ""), v.get("sources", ""))},
    ]
    return json.dumps(messages, ensure_ascii=False)
