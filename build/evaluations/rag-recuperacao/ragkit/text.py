"""Normalização de texto e tokenização para BM25."""
from __future__ import annotations

import re

_WS = re.compile(r"\s+")
_TOKEN = re.compile(r"[a-z0-9_]+")

# Lista curta de stopwords do inglês (o corpus e as perguntas estão em EN).
STOPWORDS = frozenset(
    """a an and are as at be but by can do does for from how i if in into is it
    its me my of on or so that the their them then there these this to was
    what when where which who why will with would you your""".split()
)


def normalize(text: str) -> str:
    """Caixa baixa e espaços colapsados. É a régua para casar `evidence`."""
    return _WS.sub(" ", text).strip().lower()


def tokenize(text: str) -> list[str]:
    """Tokens alfanuméricos em caixa baixa, sem stopwords.

    Identificadores com sublinhado (``site_name``) geram o token inteiro e
    também as partes (``site``, ``name``), para que "site name" case com a
    opção de configuração. Não há stemming: "excluded" não casa "exclude".
    """
    out: list[str] = []
    for raw in _TOKEN.findall(text.lower()):
        parts = [p for p in raw.split("_") if p]
        if not parts:
            continue
        candidates = [raw.strip("_")] + parts if len(parts) > 1 else parts
        out.extend(t for t in candidates if t not in STOPWORDS)
    return out
