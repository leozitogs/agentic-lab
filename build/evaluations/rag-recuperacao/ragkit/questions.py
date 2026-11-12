"""Leitura e validação do conjunto de perguntas rotuladas (questions.jsonl)."""
from __future__ import annotations

import json
import pathlib
import re
from collections.abc import Iterable

from .chunking import Chunk
from .text import normalize

REQUIRED = ("id", "question", "doc", "evidence", "category", "style")
CATEGORIES = {"conceito", "configuracao", "cli", "comportamento", "tema", "plugins", "deploy"}
STYLES = {"literal", "parafrase"}
ID_PATTERN = re.compile(r"^q\d{2}$")
EVIDENCE_WORDS = (3, 12)
MAX_OCCURRENCES = 3  # a evidência pode aparecer em "poucos lugares", não espalhada


def load(path: pathlib.Path) -> list[dict]:
    rows = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"linha {n}: JSON inválido ({exc})") from exc
    return rows


def validate_format(rows: list[dict], expected_count: int | None = 50) -> list[str]:
    """Problemas de formato que dá para ver sem o corpus."""
    problems: list[str] = []
    if expected_count is not None and len(rows) != expected_count:
        problems.append(f"esperava {expected_count} perguntas, achei {len(rows)}")
    seen: set[str] = set()
    for n, row in enumerate(rows, start=1):
        where = f"linha {n} ({row.get('id', '?')})"
        missing = [k for k in REQUIRED if not isinstance(row.get(k), str) or not row[k].strip()]
        if missing:
            problems.append(f"{where}: campos ausentes ou vazios: {missing}")
            continue
        extra = set(row) - set(REQUIRED)
        if extra:
            problems.append(f"{where}: campos desconhecidos: {sorted(extra)}")
        if not ID_PATTERN.match(row["id"]):
            problems.append(f"{where}: id fora do padrão qNN")
        if row["id"] in seen:
            problems.append(f"{where}: id repetido")
        seen.add(row["id"])
        if not row["doc"].endswith(".md") or row["doc"].startswith(("/", ".")) or "\\" in row["doc"]:
            problems.append(f"{where}: doc deve ser caminho relativo a docs/ terminado em .md")
        words = len(normalize(row["evidence"]).split(" "))
        if not EVIDENCE_WORDS[0] <= words <= EVIDENCE_WORDS[1]:
            problems.append(f"{where}: evidence com {words} palavras (aceito {EVIDENCE_WORDS[0]} a {EVIDENCE_WORDS[1]})")
        if row["category"] not in CATEGORIES:
            problems.append(f"{where}: category inválida {row['category']!r}")
        if row["style"] not in STYLES:
            problems.append(f"{where}: style inválido {row['style']!r}")
        if not row["question"].rstrip().endswith("?"):
            problems.append(f"{where}: question deve terminar com '?'")
    return problems


def validate_against_corpus(rows: list[dict], docs: dict[str, str],
                            chunkings: dict[str, Iterable[Chunk]]) -> list[str]:
    """Confere cada evidência no corpus e em cada chunking.

    - existe literalmente (após normalizar) no `doc` indicado;
    - aparece no máximo MAX_OCCURRENCES vezes no corpus inteiro;
    - cabe inteira em pelo menos um chunk de cada estratégia (senão o acerto
      seria impossível e a métrica mediria o chunker, não a busca).
    """
    problems: list[str] = []
    norm_docs = {path: normalize(text) for path, text in docs.items()}
    norm_chunks = {name: [normalize(c.text) for c in chunks] for name, chunks in chunkings.items()}
    for row in rows:
        needle = normalize(row["evidence"])
        where = row["id"]
        if row["doc"] not in norm_docs:
            problems.append(f"{where}: doc {row['doc']!r} não existe no corpus")
            continue
        if needle not in norm_docs[row["doc"]]:
            problems.append(f"{where}: evidence não aparece em {row['doc']}")
            continue
        total = sum(text.count(needle) for text in norm_docs.values())
        if total > MAX_OCCURRENCES:
            problems.append(f"{where}: evidence aparece {total} vezes no corpus (máx. {MAX_OCCURRENCES})")
        for name, texts in norm_chunks.items():
            if not any(needle in t for t in texts):
                problems.append(f"{where}: evidence não cabe em nenhum chunk de {name!r}")
    return problems


def occurrences(rows: list[dict], docs: dict[str, str]) -> dict[str, list[str]]:
    """Em quais documentos cada evidência aparece (para o relatório)."""
    norm_docs = {path: normalize(text) for path, text in docs.items()}
    return {r["id"]: [p for p, t in norm_docs.items() if normalize(r["evidence"]) in t] for r in rows}
