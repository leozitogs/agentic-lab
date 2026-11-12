---
tipo: eval
maturidade: tested
versao: 0.1.0
autores: [leozitogs]
criado_em: 2026-11-12
atualizado_em: 2026-11-12
artefato_avaliado: build/evaluations/rag-recuperacao/questions.jsonl
tags: [rag, bm25, chroma, recall-at-k, mrr]
---

# Relatório · três configurações de recuperação sobre a doc do MkDocs

> Arquivo gerado por `run_eval.py`. Não edite à mão: rode de novo. As notas da análise de erros vêm de `error_notes.json`.

Corpus: `docs/` do MkDocs `1.6.1` (BSD-2-Clause), 19 arquivos Markdown, 284,277 caracteres. Conjunto: 50 perguntas rotuladas (19 de paráfrase, 31 literais). Acerto: algum chunk do top-k contém a `evidence` da pergunta (caixa e espaços normalizados).

## Resultados

| Configuração | recall@1 | recall@3 | recall@5 | recall@10 | mrr@10 | chunks | indexação (s) | consulta média (ms) | consulta p95 (ms) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **A** · BM25 + chunk fixo | 0.58 | 0.72 | 0.78 | 0.82 | 0.67 | 478 | 0.03 | 0.16 | 0.27 |
| **B** · BM25 + chunk por estrutura | 0.68 | 0.78 | 0.78 | 0.82 | 0.73 | 585 | 0.03 | 0.15 | 0.27 |
| **C** · Densa (Chroma) + chunk por estrutura | 0.44 | 0.68 | 0.74 | 0.80 | 0.57 | 585 | 11.06 | 16.26 | 17.18 |

Intervalo de confiança de 95% por bootstrap (2000 reamostragens das 50 perguntas, semente 0):

| Configuração | recall@5 | MRR@10 |
|---|---|---|
| A | 0.66 a 0.88 | 0.55 a 0.78 |
| B | 0.66 a 0.88 | 0.61 a 0.84 |
| C | 0.62 a 0.86 | 0.45 a 0.68 |

Diferença pareada (mesmas perguntas), com IC de 95% por bootstrap:

| Comparação | Δ recall@5 | Δ MRR@10 |
|---|---|---|
| B - A | +0.00 (-0.08 a +0.08) | +0.06 (-0.02 a +0.14) |
| C - A | -0.04 (-0.18 a +0.10) | -0.10 (-0.23 a +0.02) |
| C - B | -0.04 (-0.18 a +0.08) | -0.16 (-0.30 a -0.04) |

Quando o intervalo cruza zero, a diferença não se sustenta com 50 perguntas.

### Por estilo de pergunta (recall@5)

| Configuração | literal | paráfrase |
|---|---:|---:|
| A | 1.00 | 0.42 |
| B | 0.97 | 0.47 |
| C | 0.87 | 0.53 |

### Por categoria (recall@5)

| Configuração | cli (6) | comportamento (6) | conceito (4) | configuracao (12) | deploy (7) | plugins (7) | tema (8) |
|---|---:|---:|---:|---:|---:|---:|---:|
| A | 1.00 | 0.83 | 0.75 | 0.67 | 0.71 | 0.86 | 0.75 |
| B | 0.67 | 0.83 | 0.75 | 0.75 | 0.71 | 1.00 | 0.75 |
| C | 0.67 | 0.83 | 0.75 | 0.58 | 0.86 | 0.86 | 0.75 |

## Configurações

- **A · BM25 + chunk fixo.** BM25 sobre janelas de 800 caracteres com 200 de sobreposição, por arquivo. 478 chunks, média de 787 caracteres.
- **B · BM25 + chunk por estrutura.** BM25 sobre seções por título Markdown, com o caminho de títulos no texto indexado. 585 chunks, média de 482 caracteres.
- **C · Densa (Chroma) + chunk por estrutura.** Embeddings all-MiniLM-L6-v2 dos mesmos chunks de B, busca por similaridade de cosseno no Chroma. 585 chunks, média de 482 caracteres.

## Análise de erros

13 perguntas em que as configurações divergem no top-5: q03, q07, q11, q12, q14, q17, q25, q26, q29, q32, q36, q43, q44. Casos comentados (posição do primeiro acerto em cada configuração; "-" = fora do top-10):

### q03 · literal · configuracao

> Which is the only required option in the configuration file?

Evidência em `getting-started.md`: “option is the only required option in your configuration file”. Posições: A: 1 · B: 1 · C: -.

Top-1 de cada configuração: A → `getting-started.md#fixed-3`; B → `getting-started.md#sec-5`; C → `user-guide/configuration.md#sec-0`.

A e B acertam no topo porque a pergunta repete quase as mesmas palavras da nota em getting-started.md ("only required option", "configuration file"). Em C, o primeiro lugar é o chunk de abertura de configuration.md ("Guide to all available configuration settings."): um trecho curto e genérico, que fica perto de qualquer pergunta sobre configuração no espaço vetorial. Chunks curtos e genéricos funcionam como ímãs na busca densa; na lexical eles perdem porque têm poucos termos.

### q14 · literal · cli

> Which command initializes a new translation catalog for a built-in theme?

Evidência em `dev-guide/translations.md`: “Use the `init_catalog` command on each theme's directory”. Posições: A: 5 · B: - · C: 1.

Top-1 de cada configuração: A → `dev-guide/themes.md#fixed-61`; B → `dev-guide/themes.md#sec-74`; C → `dev-guide/translations.md#sec-8`.

Aqui o caminho de títulos atrapalha B. A seção certa se chama "Initializing the localization catalogs" e a pergunta diz "initializes" e "translation": sem stemming, "initializes" não casa "Initializing", e "translation" aparece no caminho de títulos de várias seções vizinhas ("Updating the translation catalogs", "Packaging Translations with your theme"), que sobem no ranking. A janela fixa de A pega o bloco de comandos `pybabel init` e acerta em 5º. C entende que "initializes" e "Initializing" são a mesma ideia e acerta no topo.

### q26 · parafrase · comportamento

> How do I make the build fail instead of just printing a warning?

Evidência em `user-guide/configuration.md`: “Set to `true` to halt processing when a”. Posições: A: - · B: - · C: 3.

Top-1 de cada configuração: A → `about/release-notes.md#fixed-34`; B → `about/release-notes.md#sec-43`; C → `dev-guide/plugins.md#sec-43`.

Paráfrase típica: a pergunta fala em "make the build fail" e "printing a warning"; a resposta (opção `strict`) diz "halt processing when a warning is raised". BM25 vai atrás de "build" e "warning", que aparecem muito nas notas de versão, e enche o top-10 com elas. A busca densa liga "fail" a "halt" e acha a seção `strict` em 3º.

### q29 · literal · comportamento

> Is the hook module reloaded on each build when running mkdocs serve?

Evidência em `user-guide/configuration.md`: “the hook module will *not* be reloaded on each build”. Posições: A: 1 · B: 1 · C: -.

Top-1 de cada configuração: A → `user-guide/configuration.md#fixed-48`; B → `user-guide/configuration.md#sec-59`; C → `about/release-notes.md#sec-75`.

A pergunta é literal e o BM25 acerta em 1º nas duas variantes. C erra: a frase da resposta mora num chunk dominado por um exemplo de código Python (o "Advanced example" de hooks), e o vetor do chunk representa mais o código do que a frase. Chunks que misturam prosa e código longo prejudicam a busca densa; separar blocos de código grandes em chunks próprios é uma melhoria candidata.

### q36 · literal · plugins

> What does the prebuild_index option of the search plugin require?

Evidência em `user-guide/configuration.md`: “This option requires that [Node.js] be installed”. Posições: A: 5 · B: 1 · C: -.

Top-1 de cada configuração: A → `about/release-notes.md#fixed-107`; B → `user-guide/configuration.md#sec-70`; C → `user-guide/configuration.md#sec-71`.

O teto de 800 caracteres partiu a seção `prebuild_index` em dois chunks: o do aviso ("requires that Node.js be installed") e o da nota sobre sites pequenos. B acerta em 1º porque o caminho de títulos ("... Search > prebuild_index") vai para os dois pedaços e o termo raro `prebuild_index` pesa muito no BM25. C põe a nota irmã em 1º e deixa o pedaço com a resposta fora do top-10. A janela fixa de A perde para trechos das notas de versão que citam opções da busca e só acerta em 5º.

Nenhuma configuração acerta no top-10: q10 (parafrase), q20 (parafrase), q22 (parafrase), q41 (parafrase), q50 (parafrase).

## Ambiente

- Data da execução: 2026-11-12 (2026-11-12T10:18:50-03:00)
- Python 3.13.7 em Windows-11-10.0.26200-SP0
- chromadb 1.5.9
- onnxruntime 1.31.1
- tokenizers 0.23.3
- numpy 2.5.4
- Embedder da configuração C: all-MiniLM-L6-v2 em ONNX, o embedder padrão do Chroma (ONNXMiniLM_L6_V2), 384 dimensões, entrada truncada em 256 tokens, distância cosseno
- BM25: k1=1.2, b=0.75, implementação própria (biblioteca padrão)
- Chunk fixo: 800 caracteres, sobreposição de 200; chunk por estrutura: seções por título, quebradas entre parágrafos acima de 800 caracteres
- Corpus: https://github.com/mkdocs/mkdocs/archive/refs/tags/1.6.1.tar.gz (SHA-256 do tarball `10b78edfc02bf376…`, manifesto de docs/ `0d6e44279879d181…`)
- Tempo total da avaliação: 19.3 s (carga do modelo de embedding: 0.4 s)

## Limitações

- 50 perguntas escritas por uma pessoa a partir do próprio corpus: há viés de quem já conhece o texto, e os intervalos de confiança são largos. Diferenças pequenas entre configurações não são conclusivas.
- Acerto é casamento literal da evidência no chunk. Um chunk que responde a pergunta com outras palavras (por exemplo, a mesma opção explicada em outro arquivo) conta como erro.
- Mede só a recuperação. Não há geração de resposta nem avaliação de fidelidade (faithfulness).
- A configuração B muda duas coisas em relação a A: as fronteiras do chunk e o caminho de títulos no texto indexado. O experimento não separa o efeito de cada uma.
- BM25 sem stemming e com tokenizador simples; um analisador com stemming (como o do Lucene) tende a melhorar A e B nas paráfrases morfológicas.
- all-MiniLM-L6-v2 trunca a entrada em 256 word pieces: o fim de um chunk mais longo que isso não entra no vetor. Com o teto de 800 caracteres, cerca de 8% dos chunks por estrutura passam do limite (Markdown com código e URLs gera muitos tokens por caractere).
- Latências medidas numa máquina só, em processo, sem rede (mediana de 3 execuções por consulta); a inferência ONNX em CPU oscilou bastante entre execuções nesta máquina. Servem para comparar ordens de grandeza, não como número de produção.

## Anexo · posição do primeiro acerto por pergunta

| id | estilo | categoria | A | B | C |
|---|---|---|---:|---:|---:|
| q01 | literal | cli | 1 | 1 | 4 |
| q02 | literal | cli | 1 | 1 | 1 |
| q03 | literal | configuracao | 1 | 1 | - |
| q04 | literal | deploy | 2 | 1 | 3 |
| q05 | parafrase | deploy | 2 | 1 | 5 |
| q06 | literal | deploy | 5 | 1 | 5 |
| q07 | parafrase | deploy | 7 | 6 | 1 |
| q08 | literal | deploy | 1 | 1 | 1 |
| q09 | literal | deploy | 1 | 1 | 3 |
| q10 | parafrase | deploy | - | - | - |
| q11 | parafrase | cli | 1 | - | - |
| q12 | parafrase | cli | 1 | 1 | 8 |
| q13 | literal | cli | 1 | 1 | 1 |
| q14 | literal | cli | 5 | - | 1 |
| q15 | parafrase | configuracao | - | - | 6 |
| q16 | literal | configuracao | 1 | 1 | 2 |
| q17 | parafrase | configuracao | 2 | 1 | 7 |
| q18 | literal | configuracao | 1 | 1 | 2 |
| q19 | literal | configuracao | 1 | 1 | 1 |
| q20 | parafrase | configuracao | - | - | - |
| q21 | literal | configuracao | 1 | 1 | 3 |
| q22 | parafrase | configuracao | - | - | - |
| q23 | literal | configuracao | 1 | 1 | 1 |
| q24 | literal | configuracao | 1 | 1 | 1 |
| q25 | parafrase | configuracao | 8 | 3 | 1 |
| q26 | parafrase | comportamento | - | - | 3 |
| q27 | literal | comportamento | 1 | 1 | 1 |
| q28 | literal | comportamento | 1 | 1 | 1 |
| q29 | literal | comportamento | 1 | 1 | - |
| q30 | literal | comportamento | 1 | 1 | 1 |
| q31 | literal | comportamento | 1 | 1 | 2 |
| q32 | parafrase | plugins | - | 3 | 2 |
| q33 | literal | plugins | 1 | 2 | 2 |
| q34 | literal | plugins | 1 | 1 | 1 |
| q35 | parafrase | plugins | 1 | 1 | 1 |
| q36 | literal | plugins | 5 | 1 | - |
| q37 | parafrase | plugins | 2 | 2 | 1 |
| q38 | literal | plugins | 1 | 1 | 1 |
| q39 | literal | tema | 2 | 1 | 1 |
| q40 | parafrase | tema | 1 | 1 | 1 |
| q41 | parafrase | tema | - | - | - |
| q42 | parafrase | tema | 2 | 1 | 1 |
| q43 | literal | tema | 1 | 1 | - |
| q44 | parafrase | tema | - | 9 | 2 |
| q45 | literal | tema | 1 | 1 | 1 |
| q46 | literal | tema | 2 | 2 | 2 |
| q47 | literal | conceito | 1 | 1 | 1 |
| q48 | literal | conceito | 1 | 1 | 2 |
| q49 | literal | conceito | 1 | 1 | 1 |
| q50 | parafrase | conceito | - | - | - |
