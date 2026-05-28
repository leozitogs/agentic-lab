---
tipo: guide
maturidade: reviewed
versao: 0.1.0
autores: [time]
criado_em: 2026-05-28
atualizado_em: 2026-05-28
---

# Semana 2 — Arquitetura de prompts

## Objetivo

Parar de escrever prompt solto e começar a tratar prompt como **artefato de engenharia**: versionado, testado e documentado.

## Pré-requisitos

Semana 1 fechada (glossário atualizado).

## O que estudar

1. Estrutura **system / developer / user** e quando usar cada uma.
2. Padrões: role, task, exemplos, output schema, restrições, refusal handling.
3. Chain-of-thought e quando ajuda vs. quando atrapalha.
4. Few-shot: quantos exemplos, como escolher, como ordenar.
5. Output em JSON: como forçar e como validar.
6. Como decompor uma tarefa complexa em prompts encadeados.
7. Quando usar **um prompt grande** vs. **vários prompts pequenos**.

## Leituras sugeridas

- Guia de prompt engineering da Anthropic.
- "Prompt engineering best practices" da OpenAI.
- Exemplos de system prompts do Claude, GPT e Gemini (disponíveis publicamente).

## Entregável

Pelo menos **10 prompts** documentados em `build/prompts/`, usando `PROMPT-TEMPLATE.md`. Mínimo de 3 por pessoa, com pelo menos:

- 1 system prompt completo.
- 1 prompt de tarefa específica.
- 1 prompt de avaliação (prompt que avalia output de outro prompt).

Cada prompt precisa de:

- Front-matter completo.
- Pelo menos 1 teste documentado.
- Critério de qualidade explícito.

## Critério de aceite

- [ ] 10 prompts no diretório, cada um com `maturidade: tested` mínimo.
- [ ] `build/prompts/prompt-library.md` atualizado com índice.
- [ ] Pelo menos 3 prompts revisados por outra pessoa (`maturidade: reviewed`).
- [ ] Cada prompt tem nota de avaliação preliminar (mesmo que informal).

## Antipadrões a evitar

- Prompt que pede "responda bem" sem definir o que é bom.
- Prompt que mistura instrução e contexto sem separar.
- Prompt longo demais quando dois prompts menores resolveriam.
- "Funciona pra mim" como critério de aceite.

## Como apresentar

Cada pessoa traz **um** prompt: mostra input, output esperado, output real, e os casos onde ele quebra.
