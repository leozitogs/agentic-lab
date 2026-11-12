"""Avaliação completa do kit de RAG: três configurações de recuperação, 50 perguntas.

Uso:
    python run_eval.py                 # A, B e C (C precisa de requirements.txt)
    python run_eval.py --configs A,B   # só BM25, sem Chroma

Baixa o corpus para .cache/ (se preciso), valida as perguntas, indexa, consulta
e grava results/results.json e results/report.md.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import platform
import statistics
import sys
import time
from importlib import metadata

KIT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(KIT))

from ragkit import corpus, questions, report  # noqa: E402
from ragkit.bm25 import BM25Index  # noqa: E402
from ragkit.chunking import Chunk, fixed_chunks, structure_chunks  # noqa: E402
from ragkit.metrics import (bootstrap_ci, first_hit_rank, mrr_at_k,  # noqa: E402
                            paired_bootstrap_diff, recall_at_k, reciprocal_rank)

KIT_VERSION = "0.1.0"
TOP_K = 10
LATENCY_REPEATS = 3  # cada consulta roda 3 vezes; vale a mediana
FIXED = {"size": 800, "overlap": 200}
STRUCTURE = {"max_chars": 800}  # mesmo orçamento da janela de A; ver README
BM25_PARAMS = {"k1": 1.2, "b": 0.75}
EMBEDDER = ("all-MiniLM-L6-v2 em ONNX, o embedder padrão do Chroma (ONNXMiniLM_L6_V2), "
            "384 dimensões, entrada truncada em 256 tokens, distância cosseno")

CONFIGS = {
    "A": ("BM25 + chunk fixo",
          f"BM25 sobre janelas de {FIXED['size']} caracteres com {FIXED['overlap']} de sobreposição, por arquivo."),
    "B": ("BM25 + chunk por estrutura",
          "BM25 sobre seções por título Markdown, com o caminho de títulos no texto indexado."),
    "C": ("Densa (Chroma) + chunk por estrutura",
          "Embeddings all-MiniLM-L6-v2 dos mesmos chunks de B, busca por similaridade de cosseno no Chroma."),
}

LIMITATIONS = [
    "50 perguntas escritas por uma pessoa a partir do próprio corpus: há viés de quem já conhece o texto, "
    "e os intervalos de confiança são largos. Diferenças pequenas entre configurações não são conclusivas.",
    "Acerto é casamento literal da evidência no chunk. Um chunk que responde a pergunta com outras palavras "
    "(por exemplo, a mesma opção explicada em outro arquivo) conta como erro.",
    "Mede só a recuperação. Não há geração de resposta nem avaliação de fidelidade (faithfulness).",
    "A configuração B muda duas coisas em relação a A: as fronteiras do chunk e o caminho de títulos no texto "
    "indexado. O experimento não separa o efeito de cada uma.",
    "BM25 sem stemming e com tokenizador simples; um analisador com stemming (como o do Lucene) tende a "
    "melhorar A e B nas paráfrases morfológicas.",
    "all-MiniLM-L6-v2 trunca a entrada em 256 word pieces: o fim de um chunk mais longo que isso não "
    "entra no vetor. Com o teto de 800 caracteres, cerca de 8% dos chunks por estrutura passam do limite "
    "(Markdown com código e URLs gera muitos tokens por caractere).",
    "Latências medidas numa máquina só, em processo, sem rede (mediana de 3 execuções por consulta); "
    "a inferência ONNX em CPU oscilou bastante entre execuções nesta máquina. Servem para comparar ordens "
    "de grandeza, não como número de produção.",
]


def build_chunks(docs: dict[str, str]) -> tuple[dict[str, list[Chunk]], dict[str, float]]:
    out, timing = {}, {}
    t0 = time.perf_counter()
    out["fixed"] = [c for p, t in docs.items() for c in fixed_chunks(p, t, **FIXED)]
    timing["fixed"] = time.perf_counter() - t0
    t0 = time.perf_counter()
    out["structure"] = [c for p, t in docs.items() for c in structure_chunks(p, t, **STRUCTURE)]
    timing["structure"] = time.perf_counter() - t0
    return out, timing


def run_config(search, chunks: list[Chunk], rows: list[dict]) -> tuple[list[int | None], list[float], list[str]]:
    """Consulta cada pergunta; devolve posição do acerto, latência (mediana, ms) e id do top-1."""
    ranks, latencies, top1 = [], [], []
    for row in rows:
        timings = []
        for _ in range(LATENCY_REPEATS):
            t0 = time.perf_counter()
            hits = search(row["question"], TOP_K)
            timings.append((time.perf_counter() - t0) * 1000)
        latencies.append(statistics.median(timings))
        ranked = [chunks[i] for i, _ in hits]
        ranks.append(first_hit_rank([c.text for c in ranked], row["evidence"]))
        top1.append(ranked[0].id if ranked else "")
    return ranks, latencies, top1


def summarize(ranks: list[int | None], rows: list[dict]) -> dict:
    metrics = {f"recall@{k}": recall_at_k(ranks, k) for k in report.KS}
    metrics["mrr@10"] = mrr_at_k(ranks, TOP_K)
    hit5 = [1.0 if r is not None and r <= 5 else 0.0 for r in ranks]
    rr = [reciprocal_rank(r, TOP_K) for r in ranks]

    def group(key: str) -> dict[str, float]:
        values = sorted({row[key] for row in rows})
        return {v: recall_at_k([r for r, row in zip(ranks, rows) if row[key] == v], 5) for v in values}

    return {
        "metrics": metrics,
        "ci95": {"recall@5": bootstrap_ci(hit5), "mrr@10": bootstrap_ci(rr)},
        "by_style": group("style"),
        "by_category": group("category"),
        "_hit5": hit5,
        "_rr": rr,
    }


def package_versions() -> dict[str, str]:
    out = {}
    for pkg in ("chromadb", "onnxruntime", "tokenizers", "numpy"):
        try:
            out[pkg] = metadata.version(pkg)
        except metadata.PackageNotFoundError:
            pass
    return out


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--configs", default="A,B,C", help="subconjunto de A,B,C")
    parser.add_argument("--cache-dir", type=pathlib.Path, default=corpus.DEFAULT_CACHE)
    parser.add_argument("--out", type=pathlib.Path, default=KIT / "results")
    args = parser.parse_args(argv)
    selected = [c.strip() for c in args.configs.split(",") if c.strip()]
    if not set(selected) <= set(CONFIGS):
        parser.error(f"configurações válidas: {', '.join(CONFIGS)}")

    started = time.perf_counter()
    docs_dir = corpus.fetch(args.cache_dir)
    docs = corpus.load_docs(docs_dir)
    rows = questions.load(KIT / "questions.jsonl")
    chunkings, chunk_time = build_chunks(docs)
    problems = questions.validate_format(rows) or questions.validate_against_corpus(rows, docs, chunkings)
    if problems:
        for p in problems:
            print(f"ERRO  {p}")
        return 1
    print(f"Corpus: {len(docs)} arquivos; {len(rows)} perguntas válidas.")

    configs: dict[str, dict] = {}
    model_load = 0.0
    for name in selected:
        chunks = chunkings["fixed" if name == "A" else "structure"]
        base = chunk_time["fixed" if name == "A" else "structure"]
        texts = [c.index_text for c in chunks]
        if name in ("A", "B"):
            t0 = time.perf_counter()
            index = BM25Index(texts, **BM25_PARAMS)
            build = time.perf_counter() - t0
        else:
            from ragkit.dense import ChromaDenseIndex, default_embedding_function

            t0 = time.perf_counter()
            ef = default_embedding_function()
            ef(["warm up"])  # baixa/carrega o modelo fora da medição de indexação
            model_load = time.perf_counter() - t0
            t0 = time.perf_counter()
            index = ChromaDenseIndex(texts, embedding_function=ef)
            build = time.perf_counter() - t0
        ranks, latencies, top1 = run_config(index.search, chunks, rows)
        summary = summarize(ranks, rows)
        configs[name] = {
            "name": CONFIGS[name][0],
            "description": CONFIGS[name][1],
            "n_chunks": len(chunks),
            "avg_chunk_chars": round(statistics.mean(len(c.text) for c in chunks)),
            "index_seconds": base + build,
            "latency_ms": {"mean": statistics.mean(latencies),
                           "p95": statistics.quantiles(latencies, n=20)[18]},
            **summary,
            "_ranks": ranks,
            "_top1": top1,
        }
        m = summary["metrics"]
        print(f"{name}: recall@5={m['recall@5']:.2f} mrr@10={m['mrr@10']:.2f} "
              f"(indexação {base + build:.2f}s, consulta {statistics.mean(latencies):.2f}ms)")

    comparisons = {}
    for a, b in (("B", "A"), ("C", "A"), ("C", "B")):
        if a in configs and b in configs:
            comparisons[f"{a} - {b}"] = {
                "recall@5": paired_bootstrap_diff(configs[a]["_hit5"], configs[b]["_hit5"]),
                "mrr@10": paired_bootstrap_diff(configs[a]["_rr"], configs[b]["_rr"]),
            }

    per_question = [
        {"id": row["id"], "question": row["question"], "doc": row["doc"], "evidence": row["evidence"],
         "style": row["style"], "category": row["category"],
         "ranks": {c: configs[c]["_ranks"][i] for c in configs},
         "top1": {c: configs[c]["_top1"][i] for c in configs}}
        for i, row in enumerate(rows)
    ]
    for cfg in configs.values():
        for key in ("_hit5", "_rr", "_ranks", "_top1"):
            cfg.pop(key)

    now = dt.datetime.now(dt.timezone.utc).astimezone()
    results = {
        "kit_version": KIT_VERSION,
        "run_date": now.date().isoformat(),
        "generated_at": now.isoformat(timespec="seconds"),
        "environment": {"python": platform.python_version(), "platform": platform.platform(),
                        "packages": package_versions()},
        "corpus": {"project": corpus.PROJECT, "tag": corpus.TAG, "license": corpus.LICENSE,
                   "url": corpus.ARCHIVE_URL, "archive_sha256": corpus.ARCHIVE_SHA256,
                   "docs_sha256": corpus.DOCS_SHA256, "n_files": len(docs),
                   "n_chars": sum(len(t) for t in docs.values())},
        "params": {"top_k": TOP_K, "fixed": FIXED, "structure": STRUCTURE, "bm25": BM25_PARAMS,
                   "embedder": EMBEDDER},
        "styles": {s: sum(1 for r in rows if r["style"] == s) for s in sorted(questions.STYLES)},
        "categories": {c: sum(1 for r in rows if r["category"] == c) for c in sorted({r["category"] for r in rows})},
        "configs": configs,
        "comparisons": comparisons,
        "per_question": per_question,
        "limitations": LIMITATIONS,
        "model_load_seconds": model_load,
        "total_seconds": time.perf_counter() - started,
    }

    notes_path = KIT / "error_notes.json"
    notes = json.loads(notes_path.read_text(encoding="utf-8")) if notes_path.exists() else {}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (args.out / "report.md").write_text(report.render(results, notes), encoding="utf-8")
    print(f"Gravado em {args.out}/ (total {results['total_seconds']:.1f}s).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
