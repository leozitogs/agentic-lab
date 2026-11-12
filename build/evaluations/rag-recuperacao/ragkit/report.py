"""Gera results/report.md a partir do dicionário de resultados."""
from __future__ import annotations

KS = (1, 3, 5, 10)
METRICS = [f"recall@{k}" for k in KS] + ["mrr@10"]


def _pct(x: float) -> str:
    return f"{x:.2f}"


def _rank(r: int | None) -> str:
    return str(r) if r is not None else "-"


def divergent_ids(per_question: list[dict], configs: list[str], k: int = 5) -> list[str]:
    """Perguntas em que pelo menos uma configuração acerta até k e outra não."""
    out = []
    for q in per_question:
        hits = {c: q["ranks"][c] is not None and q["ranks"][c] <= k for c in configs}
        if len(set(hits.values())) > 1:
            out.append(q["id"])
    return out


def render(results: dict, notes: dict[str, str]) -> str:
    cfgs = list(results["configs"])
    env, corpus, params = results["environment"], results["corpus"], results["params"]
    pq = results["per_question"]
    lines: list[str] = []
    add = lines.append

    add("---")
    add("tipo: eval")
    add("maturidade: tested")
    add(f"versao: {results['kit_version']}")
    add("autores: [leozitogs]")
    add("criado_em: 2026-11-12")
    add(f"atualizado_em: {results['run_date']}")
    add("artefato_avaliado: build/evaluations/rag-recuperacao/questions.jsonl")
    add("tags: [rag, bm25, chroma, recall-at-k, mrr]")
    add("---")
    add("")
    add("# Relatório · três configurações de recuperação sobre a doc do MkDocs")
    add("")
    add("> Arquivo gerado por `run_eval.py`. Não edite à mão: rode de novo. "
        "As notas da análise de erros vêm de `error_notes.json`.")
    add("")
    add(f"Corpus: `docs/` do MkDocs `{corpus['tag']}` ({corpus['license']}), "
        f"{corpus['n_files']} arquivos Markdown, {corpus['n_chars']:,} caracteres. "
        f"Conjunto: {len(pq)} perguntas rotuladas "
        f"({results['styles']['parafrase']} de paráfrase, {results['styles']['literal']} literais). "
        "Acerto: algum chunk do top-k contém a `evidence` da pergunta (caixa e espaços normalizados).")
    add("")
    add("## Resultados")
    add("")
    add("| Configuração | " + " | ".join(METRICS) + " | chunks | indexação (s) | consulta média (ms) | consulta p95 (ms) |")
    add("|---|" + "---:|" * (len(METRICS) + 4))
    for c in cfgs:
        r = results["configs"][c]
        m = r["metrics"]
        add(f"| **{c}** · {r['name']} | " + " | ".join(_pct(m[x]) for x in METRICS)
            + f" | {r['n_chunks']} | {r['index_seconds']:.2f} | {r['latency_ms']['mean']:.2f} | {r['latency_ms']['p95']:.2f} |")
    add("")
    add("Intervalo de confiança de 95% por bootstrap (2000 reamostragens das 50 perguntas, semente 0):")
    add("")
    add("| Configuração | recall@5 | MRR@10 |")
    add("|---|---|---|")
    for c in cfgs:
        ci = results["configs"][c]["ci95"]
        add(f"| {c} | {_pct(ci['recall@5'][0])} a {_pct(ci['recall@5'][1])} | {_pct(ci['mrr@10'][0])} a {_pct(ci['mrr@10'][1])} |")
    add("")
    if results.get("comparisons"):
        add("Diferença pareada (mesmas perguntas), com IC de 95% por bootstrap:")
        add("")
        add("| Comparação | Δ recall@5 | Δ MRR@10 |")
        add("|---|---|---|")
        for name, comp in results["comparisons"].items():
            r5, mrr = comp["recall@5"], comp["mrr@10"]
            add(f"| {name} | {r5[0]:+.2f} ({r5[1]:+.2f} a {r5[2]:+.2f}) | {mrr[0]:+.2f} ({mrr[1]:+.2f} a {mrr[2]:+.2f}) |")
        add("")
        add("Quando o intervalo cruza zero, a diferença não se sustenta com 50 perguntas.")
        add("")
    add("### Por estilo de pergunta (recall@5)")
    add("")
    add("| Configuração | literal | paráfrase |")
    add("|---|---:|---:|")
    for c in cfgs:
        s = results["configs"][c]["by_style"]
        add(f"| {c} | {_pct(s['literal'])} | {_pct(s['parafrase'])} |")
    add("")
    add("### Por categoria (recall@5)")
    add("")
    cats = sorted(results["categories"])
    add("| Configuração | " + " | ".join(f"{cat} ({results['categories'][cat]})" for cat in cats) + " |")
    add("|---|" + "---:|" * len(cats))
    for c in cfgs:
        s = results["configs"][c]["by_category"]
        add(f"| {c} | " + " | ".join(_pct(s[cat]) for cat in cats) + " |")
    add("")
    add("## Configurações")
    add("")
    for c in cfgs:
        r = results["configs"][c]
        add(f"- **{c} · {r['name']}.** {r['description']} "
            f"{r['n_chunks']} chunks, média de {r['avg_chunk_chars']} caracteres.")
    add("")
    add("## Análise de erros")
    add("")
    div = divergent_ids(pq, cfgs)
    by_id = {q["id"]: q for q in pq}
    add(f"{len(div)} perguntas em que as configurações divergem no top-5: {', '.join(div) if div else 'nenhuma'}. "
        "Casos comentados (posição do primeiro acerto em cada configuração; \"-\" = fora do top-10):")
    add("")
    for qid, note in notes.items():
        q = by_id.get(qid)
        if q is None:
            continue
        ranks = " · ".join(f"{c}: {_rank(q['ranks'][c])}" for c in cfgs)
        add(f"### {qid} · {q['style']} · {q['category']}")
        add("")
        add(f"> {q['question']}")
        add("")
        add(f"Evidência em `{q['doc']}`: “{q['evidence']}”. Posições: {ranks}.")
        add("")
        add("Top-1 de cada configuração: " + "; ".join(f"{c} → `{q['top1'][c]}`" for c in cfgs) + ".")
        add("")
        add(note)
        add("")
    missed = [f"{q['id']} ({q['style']})" for q in pq if all(q["ranks"][c] is None for c in cfgs)]
    if missed:
        add(f"Nenhuma configuração acerta no top-10: {', '.join(missed)}.")
        add("")
    add("## Ambiente")
    add("")
    add(f"- Data da execução: {results['run_date']} ({results['generated_at']})")
    add(f"- Python {env['python']} em {env['platform']}")
    for pkg, ver in env["packages"].items():
        add(f"- {pkg} {ver}")
    add(f"- Embedder da configuração C: {params['embedder']}")
    add(f"- BM25: k1={params['bm25']['k1']}, b={params['bm25']['b']}, implementação própria (biblioteca padrão)")
    add(f"- Chunk fixo: {params['fixed']['size']} caracteres, sobreposição de {params['fixed']['overlap']}; "
        f"chunk por estrutura: seções por título, quebradas entre parágrafos acima de {params['structure']['max_chars']} caracteres")
    add(f"- Corpus: {corpus['url']} (SHA-256 do tarball `{corpus['archive_sha256'][:16]}…`, "
        f"manifesto de docs/ `{corpus['docs_sha256'][:16]}…`)")
    add(f"- Tempo total da avaliação: {results['total_seconds']:.1f} s "
        f"(carga do modelo de embedding: {results.get('model_load_seconds', 0):.1f} s)")
    add("")
    add("## Limitações")
    add("")
    for item in results["limitations"]:
        add(f"- {item}")
    add("")
    add("## Anexo · posição do primeiro acerto por pergunta")
    add("")
    add("| id | estilo | categoria | " + " | ".join(cfgs) + " |")
    add("|---|---|---|" + "---:|" * len(cfgs))
    for q in pq:
        add(f"| {q['id']} | {q['style']} | {q['category']} | " + " | ".join(_rank(q["ranks"][c]) for c in cfgs) + " |")
    add("")
    return "\n".join(lines)
