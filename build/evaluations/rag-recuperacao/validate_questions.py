"""Valida questions.jsonl.

Uso:
    python validate_questions.py           # só formato (sem rede)
    python validate_questions.py --corpus  # baixa/usa o corpus e confere cada evidência

Sai com código 1 se houver problema.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

KIT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(KIT))

from ragkit import corpus, questions  # noqa: E402
from run_eval import build_chunks  # noqa: E402  (mesmos parâmetros da avaliação)

QUESTIONS = KIT / "questions.jsonl"
CACHE = corpus.DEFAULT_CACHE


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--corpus", action="store_true", help="confere as evidências no corpus")
    args = parser.parse_args(argv)

    rows = questions.load(QUESTIONS)
    problems = questions.validate_format(rows)
    if args.corpus and not problems:
        docs = corpus.load_docs(corpus.fetch(CACHE))
        problems = questions.validate_against_corpus(rows, docs, build_chunks(docs)[0])
    for p in problems:
        print(f"ERRO  {p}")
    print(f"{len(rows)} pergunta(s), {len(problems)} problema(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
