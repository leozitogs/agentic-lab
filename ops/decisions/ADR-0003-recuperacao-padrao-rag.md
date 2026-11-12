---
tipo: adr
maturidade: tested
versao: 0.1.0
autores: [leozitogs]
criado_em: 2026-11-12
atualizado_em: 2026-11-12
status: aceito
---

# ADR-0003 · BM25 com chunks por estrutura como recuperação padrão para RAG sobre documentação

## Status

Aceito.

## Contexto

O módulo 03 da trilha avançada pede um RAG sobre a documentação pública de um projeto open source, com três configurações de recuperação comparadas em 50 perguntas rotuladas. O [kit de RAG](../../build/evaluations/rag-recuperacao/README.md) fez isso sobre a pasta `docs/` do MkDocs 1.6.1 (19 arquivos, 284 mil caracteres, inglês), com 31 perguntas literais e 19 paráfrases.

As três configurações:

- **A:** BM25 sobre janelas fixas de 800 caracteres com 200 de sobreposição.
- **B:** BM25 sobre seções por título Markdown (teto de 800 caracteres, caminho de títulos no texto indexado).
- **C:** busca densa no Chroma com all-MiniLM-L6-v2 (ONNX) sobre os mesmos chunks de B.

Resultado da rodada de 2026-11-12 ([relatório completo](../../build/evaluations/rag-recuperacao/results/report.md)):

| Configuração | recall@1 | recall@5 | recall@10 | MRR@10 | recall@5 literal | recall@5 paráfrase | indexação | consulta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 0.58 | 0.78 | 0.82 | 0.67 | 1.00 | 0.42 | 0.03 s | 0.2 ms |
| B | 0.68 | 0.78 | 0.82 | 0.73 | 0.97 | 0.47 | 0.03 s | 0.2 ms |
| C | 0.44 | 0.74 | 0.80 | 0.57 | 0.87 | 0.53 | 11.1 s | 16 ms |

Diferenças pareadas com intervalo de 95% por bootstrap:

- B contra A: recall@5 +0.00 (-0.08 a +0.08), MRR@10 +0.06 (-0.02 a +0.14).
- C contra B: recall@5 -0.04 (-0.18 a +0.08), MRR@10 -0.16 (-0.30 a -0.04).

## Decisão

A configuração padrão do laboratório para RAG sobre documentação técnica é a **B: BM25 sobre chunks por estrutura** (seções por título, teto de 800 caracteres, caminho de títulos no texto indexado).

Motivos, em ordem de peso:

1. **Ranqueia melhor.** B tem o maior MRR@10 (0.73) e o maior recall@1 (0.68). Contra C, a vantagem de MRR (+0.16) é a única, entre as diferenças pareadas medidas, cujo intervalo não cruza zero. Para RAG isso importa: o que entra no prompt são os primeiros chunks.
2. **Não perde em cobertura.** recall@5 e recall@10 de B são iguais aos de A e maiores ou iguais aos de C.
3. **Custa quase nada.** Indexa em 0.03 s e responde em 0.2 ms, sem modelo, sem GPU e sem dependência além da biblioteca padrão. C leva 11.1 s para indexar 585 chunks e cerca de 16 ms por consulta, e exige onnxruntime e um modelo de 80 MB.
4. **Chunk por estrutura é melhor unidade de contexto.** Mesmo com recall@5 empatado com A, a seção inteira com o caminho de títulos é um trecho legível e citável; a janela fixa entrega pedaços cortados no meio da frase.

Ficam registrados também dois parâmetros que valem para qualquer configuração futura com embeddings: o chunk precisa caber na janela de entrada do embedder (com teto de 1500 caracteres, 37% dos chunks passavam dos 256 tokens do all-MiniLM-L6-v2), e blocos de código longos atrapalham o vetor da prosa ao redor.

## Consequências

### Positivas

- Um padrão barato e reprodutível para os próximos exercícios e kits que precisam de recuperação.
- O conjunto rotulado e o script ficam como régua: qualquer proposta de troca (outro embedder, reranker, outra estratégia) roda no mesmo conjunto e é comparada com estes números.

### Negativas

- BM25 perde para a busca densa nas paráfrases (recall@5 0.47 contra 0.53). Perguntas de usuário que não usam o vocabulário da documentação vão falhar mais.
- O caminho de títulos às vezes infla seções vizinhas com títulos parecidos (caso q14 no relatório).

### Neutras

- O resultado vale para documentação técnica em inglês com perguntas escritas olhando o texto. Corpus em português, multilíngue ou com perguntas de usuários reais pede nova medição antes de reaproveitar esta decisão.
- A maturidade fica em `tested`: falta revisão de outra pessoa e um segundo rotulador para as perguntas.

## Alternativas consideradas

| Alternativa | Por que não |
|-------------|-------------|
| A · BM25 com chunk fixo | Mesmo recall@5 de B, mas ranqueia pior (MRR 0.67 contra 0.73) e entrega trechos cortados no meio de seções e blocos de código. |
| C · busca densa (Chroma, all-MiniLM-L6-v2) | Ganha nas paráfrases, mas perde no MRR com diferença que se sustenta no intervalo de confiança, erra perguntas literais que o BM25 acerta no topo e custa duas ordens de grandeza a mais para indexar e consultar. Continua como candidata para um conjunto com mais paráfrases. |

## Referências

- [Kit de RAG](../../build/evaluations/rag-recuperacao/README.md) e [relatório da rodada](../../build/evaluations/rag-recuperacao/results/report.md).
- [Módulo 03 · RAG e recuperação](../../learn/avancado/03-rag-e-recuperacao.md).
- Robertson e Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond" (2009).
- Reimers e Gurevych, "Sentence-BERT" (2019), base do all-MiniLM-L6-v2.
