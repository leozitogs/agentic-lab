"""recall@k, MRR@k e intervalo de confiança por bootstrap."""
from __future__ import annotations

import random
from collections.abc import Sequence

from .text import normalize


def first_hit_rank(ranked_texts: Sequence[str], evidence: str) -> int | None:
    """Posição (1 = topo) do primeiro trecho que contém a evidência normalizada."""
    needle = normalize(evidence)
    for pos, text in enumerate(ranked_texts, start=1):
        if needle in normalize(text):
            return pos
    return None


def recall_at_k(ranks: Sequence[int | None], k: int) -> float:
    """Fração de perguntas com acerto até a posição k."""
    if not ranks:
        return 0.0
    return sum(1 for r in ranks if r is not None and r <= k) / len(ranks)


def reciprocal_rank(rank: int | None, k: int) -> float:
    return 1.0 / rank if rank is not None and rank <= k else 0.0


def mrr_at_k(ranks: Sequence[int | None], k: int = 10) -> float:
    """Média de 1/posição do primeiro acerto; 0 quando não há acerto até k."""
    if not ranks:
        return 0.0
    return sum(reciprocal_rank(r, k) for r in ranks) / len(ranks)


def bootstrap_ci(values: Sequence[float], n_resamples: int = 2000, seed: int = 0,
                 alpha: float = 0.05) -> tuple[float, float]:
    """IC percentil da média por reamostragem com reposição (semente fixa)."""
    if not values:
        return (0.0, 0.0)
    rng = random.Random(seed)
    n = len(values)
    means = sorted(sum(rng.choices(values, k=n)) / n for _ in range(n_resamples))
    lo = means[int((alpha / 2) * n_resamples)]
    hi = means[min(n_resamples - 1, int((1 - alpha / 2) * n_resamples))]
    return (lo, hi)


def paired_bootstrap_diff(a: Sequence[float], b: Sequence[float], n_resamples: int = 2000,
                          seed: int = 0, alpha: float = 0.05) -> tuple[float, float, float]:
    """Diferença média (a - b) por pergunta e seu IC pareado por bootstrap."""
    if len(a) != len(b):
        raise ValueError("listas pareadas precisam ter o mesmo tamanho")
    diffs = [x - y for x, y in zip(a, b)]
    lo, hi = bootstrap_ci(diffs, n_resamples, seed, alpha)
    return (sum(diffs) / len(diffs) if diffs else 0.0, lo, hi)
