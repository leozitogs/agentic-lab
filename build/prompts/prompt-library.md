---
tipo: guide
maturidade: tested
versao: 0.1.0
autores: [time]
criado_em: 2026-05-28
atualizado_em: 2026-05-28
---

# Biblioteca de prompts

Índice navegável dos prompts catalogados. Quando você adiciona um prompt em `build/prompts/`, registre aqui.

## Por categoria

### System prompts

| Nome | Maturidade | Modelos | Nota |
|------|------------|---------|------|
| [research-analyst](system/research-analyst.md) | tested | claude-opus-4-6 | 82 |

### Task prompts

| Nome | Maturidade | Modelos | Nota |
|------|------------|---------|------|
| _vazio_ | | | |

### Evaluation prompts

| Nome | Maturidade | Modelos | Nota |
|------|------------|---------|------|
| _vazio_ | | | |

## Por tag

Use `grep -rl "tags:.*sintese"` para encontrar prompts por tag.

## Como adicionar um prompt aqui

1. Crie o arquivo em `system/`, `task/` ou `evaluation/` usando `PROMPT-TEMPLATE.md`.
2. Faça pelo menos um teste documentado.
3. Adicione linha na tabela correspondente acima.
4. Abra PR.
