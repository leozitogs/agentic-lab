---
tipo: guide
maturidade: draft
versao: 0.2.0
autores: [leozitogs]
criado_em: 2026-11-12
atualizado_em: 2026-11-12
---

# Módulo 03 · RAG e recuperação

## Objetivo

Construir e, principalmente, medir um sistema de recuperação de contexto.

## Perguntas que o módulo responde

- Por que o RAG "ingênuo" falha?
- Como saber se a recuperação melhorou?

## Tópicos

1. Chunking por estrutura versus por tamanho.
2. Embeddings, busca lexical (BM25) e busca híbrida.
3. Rerankers.
4. Contextual retrieval e enriquecimento de chunks.
5. GraphRAG e quando ele compensa.
6. Métricas: recall@k, MRR, nDCG e fidelidade da resposta.

## Ferramentas para comparar

Escolha pelo menos duas e compare no mesmo exercício. O objetivo é entender o trade-off, não decorar uma ferramenta.

- pgvector
- Qdrant
- Chroma
- Elasticsearch / OpenSearch
- LlamaIndex
- RAGAS

## Leituras

- Lewis et al., "Retrieval-Augmented Generation" (2020).
- Anthropic, "Introducing Contextual Retrieval" (2024).
- Microsoft, "GraphRAG" (2024).

## Exercício

Monte um RAG sobre a documentação pública de um projeto open source e compare três configurações de recuperação com 50 perguntas rotuladas.

## Critério de aceite

- [ ] Conjunto de perguntas rotuladas versionado.
- [ ] Relatório com recall@k e MRR por configuração.
- [ ] Decisão registrada em ADR.
