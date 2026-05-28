# Examples — research-synthesis

## Exemplo 1: 3 papers sobre RAG

**Input:** 3 PDFs anexados, pergunta "Quando RAG supera fine-tuning?"

**Output esperado (trecho):**

```md
## Question
Quando RAG supera fine-tuning para tarefas de QA em domínio fechado?

## Sources considered
- [Lewis et al., 2020] — proposta original do RAG, foco em open-domain QA.
- [Wang et al., 2024] — benchmark comparando RAG e fine-tuning em corpus jurídico.
- [Blog X, 2025] — argumento prático de equipe de produto.

## Findings

### Agreed across sources
- RAG é preferível quando o corpus muda com frequência. [Lewis, Wang, Blog X]
- Fine-tuning é melhor para tarefas com formato fixo de output. [Wang, Blog X]

### Disagreements
- Custo total: Wang afirma RAG mais caro em latência; Blog X afirma o oposto. Causa provável: configurações diferentes de cache.

### Gaps
- Nenhuma fonte avalia em português.

## Risks and unknowns
- Generalização para domínios médicos (todas as fontes usam outros domínios).

## Recommended next steps
- Rodar benchmark próprio com corpus em PT-BR, comparando latência com e sem cache.
- Definir critério de "formato fixo" antes de decidir entre RAG e FT.
```

## Exemplo 2: caso negativo

**Input:** 1 artigo sobre prompt injection.

**Comportamento esperado:** skill NÃO carrega. Modelo deve resumir o artigo, não comparar com nada.
