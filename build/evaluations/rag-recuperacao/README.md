---
tipo: eval
maturidade: tested
versao: 0.1.0
autores: [leozitogs]
criado_em: 2026-11-12
atualizado_em: 2026-11-12
artefato_avaliado: learn/avancado/03-rag-e-recuperacao.md
tags: [rag, recuperacao, bm25, chroma, eval-as-code]
---

# Kit de RAG · recuperação sobre a documentação do MkDocs

O exercício do [módulo 03](../../../learn/avancado/03-rag-e-recuperacao.md), pronto para rodar: um corpus público fixado numa versão, 50 perguntas rotuladas, três configurações de recuperação comparadas no mesmo conjunto e um relatório gerado por script. A decisão que saiu daqui está na [ADR-0003](../../../ops/decisions/ADR-0003-recuperacao-padrao-rag.md).

## Resultado da rodada de 2026-11-12

| Configuração | recall@1 | recall@3 | recall@5 | recall@10 | MRR@10 | indexação | consulta |
|---|---:|---:|---:|---:|---:|---:|---:|
| A · BM25 + chunk fixo | 0.58 | 0.72 | 0.78 | 0.82 | 0.67 | 0.03 s | 0.2 ms |
| B · BM25 + chunk por estrutura | **0.68** | **0.78** | **0.78** | **0.82** | **0.73** | 0.03 s | 0.2 ms |
| C · densa (Chroma) + chunk por estrutura | 0.44 | 0.68 | 0.74 | 0.80 | 0.57 | 11.1 s | 16 ms |

Nas perguntas literais o BM25 acerta quase tudo no top-5 (A 1.00, B 0.97, C 0.87); nas paráfrases a busca densa vai melhor (C 0.53, B 0.47, A 0.42). Com 50 perguntas, só uma diferença se sustenta no intervalo de confiança: o MRR@10 de B é maior que o de C. Números completos, intervalos, análise de erros e ambiente em [`results/report.md`](results/report.md).

## O que tem aqui

| Arquivo | Papel |
|---|---|
| [`questions.jsonl`](questions.jsonl) | As 50 perguntas rotuladas (versionado) |
| [`run_eval.py`](run_eval.py) | Roda tudo: baixa o corpus, valida as perguntas, indexa as três configurações, mede e escreve `results/` |
| [`validate_questions.py`](validate_questions.py) | Valida o formato das perguntas e, com `--corpus`, cada evidência no corpus |
| [`ragkit/`](ragkit/) | Biblioteca do kit: `corpus`, `chunking`, `bm25`, `dense` (Chroma), `metrics`, `questions`, `report` |
| [`error_notes.json`](error_notes.json) | Comentários da análise de erros, por id de pergunta; o relatório os inclui |
| [`results/`](results/report.md) | `report.md` e `results.json` da última rodada |
| [`tests/`](tests/) | Testes sem rede e sem modelo |
| [`requirements.in`](requirements.in) / [`requirements.txt`](requirements.txt) | Dependência direta (`chromadb`) e o conjunto completo fixado |

## Corpus

A pasta `docs/` do [MkDocs](https://github.com/mkdocs/mkdocs), fixada na tag **1.6.1** (licença **BSD-2-Clause**, copyright Tom Christie): 19 arquivos Markdown, cerca de 284 mil caracteres, em inglês. As notas de versão (`about/release-notes.md`, 110 mil caracteres) entram de propósito: é o distrator realista que qualquer doc de projeto tem.

O corpus não é versionado aqui. `ragkit/corpus.py` baixa o tarball da tag do GitHub para `.cache/rag-recuperacao/` na raiz do repositório (ignorada pelo git e fora de `build/`, para que o validador de front-matter e o site não enxerguem os `.md` baixados), lê só os `.md` regulares de `docs/` (nada do pacote é executado, caminhos com `..` ou links simbólicos são descartados) e confere dois hashes:

- SHA-256 do tarball (`10b78edf…`). Se diferir, é só aviso: o GitHub gera o arquivo sob demanda.
- SHA-256 de um manifesto com caminho e hash de cada `.md` (`0d6e4427…`). Se diferir, a execução para. É esse hash que garante que todo mundo mede o mesmo texto.

## Perguntas

Cada linha de `questions.jsonl` tem:

| Campo | Conteúdo |
|---|---|
| `id` | `q01` a `q50` |
| `question` | A pergunta, em inglês (o corpus está em inglês e o embedder é monolíngue) |
| `doc` | Arquivo de origem, relativo a `docs/` |
| `evidence` | Trecho literal de 3 a 12 palavras que precisa estar num chunk recuperado para contar acerto |
| `category` | `conceito`, `configuracao`, `cli`, `comportamento`, `tema`, `plugins` ou `deploy` |
| `style` | `literal` (reaproveita termos do texto) ou `parafrase` (evita de propósito os termos do texto) |

São 31 literais e 19 paráfrases. As paráfrases existem para a busca lexical sofrer de verdade: "make the build fail" em vez de "halt processing when a warning is raised", "stylesheet" em vez de "CSS".

A validação (`python validate_questions.py --corpus`, e de novo no começo de `run_eval.py`) exige, para cada pergunta, que a evidência normalizada (caixa baixa, espaços colapsados) apareça no `doc` indicado, apareça no máximo 3 vezes no corpus inteiro e caiba inteira em pelo menos um chunk de **cada** estratégia. A última regra impede que a métrica meça o corte do chunker em vez da busca.

## As três configurações

| | Chunks | Busca |
|---|---|---|
| **A** | Janelas de 800 caracteres com 200 de sobreposição, por arquivo. Corta palavras, seções e código sem cerimônia. | BM25 |
| **B** | Uma seção por título Markdown (`#` a `######`, ignorando `#` dentro de blocos de código). Seções acima de 800 caracteres são quebradas entre parágrafos. O caminho de títulos (ex.: `Configuration > Build directories > theme`) vai na frente do texto indexado. | BM25 |
| **C** | Os mesmos chunks de B. | Densa: embeddings no Chroma, distância cosseno |

**BM25.** Implementação própria em `ragkit/bm25.py` (biblioteca padrão, k1 = 1.2, b = 0.75, idf do Lucene). Tokenizador simples: caixa baixa, sem stopwords, identificadores como `site_name` geram o token inteiro e as partes, sem stemming.

**Teto de 800 caracteres em B e C.** Com teto de 1500, 37% dos chunks passavam de 256 tokens, o limite de entrada do all-MiniLM-L6-v2, e o texto além disso nunca entrava no vetor: em seis das perguntas que C errava no top-5, a evidência estava depois do 256º token. Com 800, que também é o tamanho da janela de A, ficam cerca de 8% acima do limite e A e B passam a comparar chunks do mesmo tamanho.

**Por que o embedder padrão do Chroma.** É o all-MiniLM-L6-v2 exportado para ONNX e rodado com onnxruntime: sem PyTorch (o ambiente inteiro, com Chroma e onnxruntime, ocupa cerca de 300 MB, menos do que o PyTorch costuma ocupar sozinho), roda em CPU comum e na CI, o modelo de ~80 MB é baixado uma vez com checagem de SHA-256 pelo próprio Chroma, e é o baseline mais usado de sentence-transformers para inglês. O kit instancia `ONNXMiniLM_L6_V2` direto em vez de `DefaultEmbeddingFunction` porque esta recria a sessão ONNX a cada chamada (cerca de 130 ms a mais por consulta); o modelo e os vetores são os mesmos.

## Métricas

- **Acerto:** algum chunk do top-k contém a `evidence` normalizada.
- **recall@k** (k = 1, 3, 5, 10): fração de perguntas com acerto até a posição k.
- **MRR@10:** média de 1/posição do primeiro acerto, zero se não há acerto no top-10.
- **Intervalo de 95%** por bootstrap das 50 perguntas (2000 reamostragens, semente fixa) e diferença pareada entre configurações.
- **Tempo de indexação** (chunking mais construção do índice; em C inclui gerar os embeddings, sem contar a carga do modelo) e **latência média e p95 por consulta** (mediana de 3 execuções de cada pergunta).

## Como rodar

```bash
# Testes leves: só biblioteca padrão, sem rede e sem modelo
cd build/evaluations/rag-recuperacao
python -m unittest discover -s tests -v

# Avaliação completa (Python 3.11+). Crie o venv na raiz do repositório
# (.venv/ é ignorado pelo git), não dentro de build/.
cd ../../..
python -m venv .venv && . .venv/bin/activate   # no Windows: .venv\Scripts\activate
pip install -r build/evaluations/rag-recuperacao/requirements.txt
cd build/evaluations/rag-recuperacao
python validate_questions.py --corpus
python run_eval.py                # A, B e C; escreve results/report.md e results/results.json
python run_eval.py --configs A,B  # só BM25, dispensa o Chroma
```

Na primeira execução o corpus (4,5 MB) e o modelo ONNX (~80 MB) são baixados. Numa máquina comum a avaliação completa leva menos de um minuto (20 s na rodada registrada, contando o download do corpus e com o modelo já em cache).

Para trocar o conjunto de dependências: edite `requirements.in` e regenere `requirements.txt` com o comando do cabeçalho do arquivo. O corte `--exclude-newer` garante que toda versão fixada foi publicada pelo menos 2 semanas antes.

## Na CI

O workflow [`.github/workflows/rag-kit.yml`](../../../.github/workflows/rag-kit.yml) roda os testes leves e a validação de formato das perguntas em todo push e PR que toca o kit. A avaliação completa roda sob demanda (`workflow_dispatch`): instala as dependências, baixa o corpus e o modelo, roda os testes com Chroma, roda as três configurações e publica `results/` como artefato da execução.

## As seis perguntas

1. **O que aprendemos?** Em documentação técnica, BM25 com chunks por estrutura é um baseline difícil de bater: empata ou vence a busca densa em recall e ranqueia melhor (MRR), custando quase nada. A busca densa ganha nas paráfrases e perde nas perguntas literais, principalmente com chunks curtos e genéricos ou chunks dominados por código. O tamanho do chunk precisa respeitar a janela do embedder, ou o modelo nem lê a resposta.
2. **Como reproduzir?** `pip install -r requirements.txt && python run_eval.py`. Corpus, perguntas e dependências estão fixados.
3. **Quando usar?** Como ponto de partida para escolher a recuperação de um RAG sobre documentação em inglês, e como molde para montar um conjunto rotulado sobre a sua própria doc.
4. **Quando NÃO usar?** Para concluir algo sobre corpus em português ou multilíngue, sobre perguntas de usuários reais (as daqui foram escritas olhando o texto) ou sobre qualidade de resposta final: o kit mede só a recuperação.
5. **Como avaliar?** Pelo próprio relatório: recall@k e MRR com intervalos de confiança, cortes por estilo e categoria, e a lista de perguntas em que as configurações divergem.
6. **Como melhorar?** Perguntas de usuários reais e mais de um rotulador; um analisador com stemming no BM25; blocos de código grandes em chunks próprios; avaliar a resposta gerada (fidelidade) além da recuperação.

## Limitações

- As perguntas foram escritas por uma pessoa olhando o corpus, o que favorece a busca lexical nas literais (A acerta 100% delas no top-5).
- Acerto é casamento literal da evidência: um chunk que responde com outras palavras, ou a mesma informação em outro arquivo, conta como erro.
- B muda duas coisas em relação a A (fronteiras e caminho de títulos); o experimento não separa os efeitos.
- 50 perguntas dão intervalos largos. A lista completa está no relatório.
