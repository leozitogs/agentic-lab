"""BM25 (Okapi) com índice invertido, só biblioteca padrão."""
from __future__ import annotations

import heapq
import math
from collections import Counter, defaultdict

from .text import tokenize


class BM25Index:
    """Índice BM25 sobre uma lista de textos.

    idf no formato do Lucene, ln(1 + (N - n + 0.5) / (n + 0.5)), que nunca
    fica negativo. Termos repetidos na consulta contam uma vez.
    """

    def __init__(self, texts: list[str], k1: float = 1.2, b: float = 0.75, tokenizer=tokenize):
        self.k1, self.b, self.tokenizer = k1, b, tokenizer
        self.n_docs = len(texts)
        self.lengths: list[int] = []
        self.postings: dict[str, list[tuple[int, int]]] = defaultdict(list)
        for idx, text in enumerate(texts):
            counts = Counter(tokenizer(text))
            self.lengths.append(sum(counts.values()))
            for term, tf in counts.items():
                self.postings[term].append((idx, tf))
        self.avg_len = (sum(self.lengths) / self.n_docs) if self.n_docs else 0.0
        self.idf = {
            term: math.log(1 + (self.n_docs - len(plist) + 0.5) / (len(plist) + 0.5))
            for term, plist in self.postings.items()
        }

    def scores(self, query: str) -> dict[int, float]:
        acc: dict[int, float] = defaultdict(float)
        for term in set(self.tokenizer(query)):
            plist = self.postings.get(term)
            if not plist:
                continue
            idf = self.idf[term]
            for idx, tf in plist:
                norm = 1 - self.b + self.b * (self.lengths[idx] / self.avg_len if self.avg_len else 0)
                acc[idx] += idf * tf * (self.k1 + 1) / (tf + self.k1 * norm)
        return acc

    def search(self, query: str, k: int = 10) -> list[tuple[int, float]]:
        """Os `k` melhores (índice, score); empate desfeito pela ordem do corpus."""
        acc = self.scores(query)
        return heapq.nsmallest(k, ((i, s) for i, s in acc.items()), key=lambda x: (-x[1], x[0]))
