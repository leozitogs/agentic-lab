---
tipo: eval
maturidade: tested
versao: 0.1.0
autores: [leozitogs]
criado_em: 2026-11-12
atualizado_em: 2026-11-12
artefato_avaliado: build/prompts/system/research-analyst.md
tags: [eval-as-code, promptfoo]
---

# Eval como código · research-analyst

A avaliação manual de [`eval-research-analyst-v0.1.0.md`](../eval-research-analyst-v0.1.0.md) virou uma suíte que roda com um comando e na CI.

## O que tem aqui

| Arquivo | Papel |
|---|---|
| `promptfooconfig.yaml` | Os 5 casos do conjunto de teste (feliz, borda e adversariais) e as asserções |
| `prompt.py` | Monta a conversa lendo o system prompt **direto** de `build/prompts/system/research-analyst.md` (fonte única) |
| `checks.py` | Asserções determinísticas: estrutura, fontes não inventadas, discordâncias nomeadas, próximos passos acionáveis, limite de palavras, pedido de clarificação |
| `fixtures/*.txt` | Fontes **sintéticas** usadas nos casos, mais uma saída de referência boa e uma ruim |
| `offline_provider.py` | Provider falso para testar a fiação da suíte sem chave de API |

As asserções que dependem de julgamento (atribuição de claims, tratamento de fonte não verificável) usam `llm-rubric`, com um modelo diferente dos avaliados como juiz.

## Como rodar

```bash
# 1. Testar a régua: as checagens aprovam a saída boa e pegam a ruim (sem modelo)
python -m unittest tests.test_research_analyst_checks -v

# 2. Testar a fiação da suíte sem chave de API
npx -y promptfoo@0.125.1 eval -c build/evaluations/research-analyst/promptfooconfig.yaml \
  --providers file://offline_provider.py --grader file://offline_provider.py --no-cache

# 3. Rodar de verdade nos modelos (precisa de ANTHROPIC_API_KEY)
npx -y promptfoo@0.125.1 eval -c build/evaluations/research-analyst/promptfooconfig.yaml
npx -y promptfoo@0.125.1 view
```

## Na CI

O workflow `.github/workflows/eval-research-analyst.yml` roda os passos 1 e 2 em todo PR que mexe no prompt ou na suíte. O passo 3 só roda quando o segredo `ANTHROPIC_API_KEY` está configurado no repositório, e o resultado fica como artefato da execução.

## Limitações conhecidas

- `only_given_sources` confere os nomes listados em "Sources considered"; uma fonte inventada citada só no meio do texto é responsabilidade do `llm-rubric`.
- `actionable_next_steps` mede tamanho e quantidade, não se o passo é bom. Isso também fica para o juiz.
- O juiz (`llm-rubric`) ainda não foi calibrado contra avaliação humana. Próximo passo: 20 saídas avaliadas por duas pessoas e comparação com o juiz.
