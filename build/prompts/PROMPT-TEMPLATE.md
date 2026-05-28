---
tipo: prompt
maturidade: draft
versao: 0.1.0
autores: [seu-nome]
criado_em: YYYY-MM-DD
atualizado_em: YYYY-MM-DD
modelos_testados: []
tags: []
nota_avaliacao: null
---

# Nome do prompt

## Objetivo

Em uma frase, o que este prompt resolve.

## Quando usar

Situações concretas onde ele se encaixa.

## Quando NÃO usar

Situações onde ele falha, é caro demais ou é inseguro.

## Categoria

`system` | `task` | `evaluation`

## Prompt

> Prompts são escritos em inglês por convenção (LLMs performam melhor). A documentação em volta fica em português.

```txt
You are <role>.

# Goal
<one-line goal>

# Instructions
1. ...
2. ...
3. ...

# Output format
<schema or example>

# Constraints
- ...
- ...
```

## Entradas esperadas

| Variável | Tipo | Descrição |
|----------|------|-----------|
| `input_a` | string | ... |
| `input_b` | json | ... |

## Saída esperada

Formato, schema ou exemplo de output válido.

## Critérios de qualidade

O que define uma boa resposta. Use isto no scorecard.

- ...
- ...

## Testes realizados

| # | Modelo | Input resumido | Resultado | Nota | Observações |
|---|--------|----------------|-----------|------|-------------|
| 1 | claude-opus-4-6 | ... | ... | 80 | ... |
| 2 | gpt-5.5-thinking | ... | ... | 75 | ... |

## Falhas conhecidas

Cenários onde o prompt falha de forma reprodutível.

- ...

## Variantes consideradas e descartadas

Versões que foram testadas e não foram para o catálogo. Anote por quê.

## Próxima versão

O que melhorar na próxima iteração.

## Changelog

- `0.1.0` — versão inicial.
