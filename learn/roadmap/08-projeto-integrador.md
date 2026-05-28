---
tipo: guide
maturidade: reviewed
versao: 0.1.0
autores: [time]
criado_em: 2026-05-28
atualizado_em: 2026-05-28
---

# Semana 8 — Projeto integrador

## Objetivo

Juntar tudo. Prompt + skill + MCP + eval, resolvendo um problema real, com demo.

## Pré-requisitos

Semanas 1 a 7 fechadas.

## Escopo

Um **caso de uso integrado** documentado em `cases/`, que use:

- Pelo menos 1 prompt arquitetado.
- Pelo menos 1 skill.
- Pelo menos 1 MCP server.
- Pelo menos 1 avaliação que mostre que funciona.

Sugestão de caso (escolham juntos):

- **Agente de pesquisa interno**: consulta o repo via MCP, sintetiza via skill, formata via prompt.
- **Pipeline de revisão de documentos**: skill extrai → MCP busca contexto → prompt gera revisão.
- **Assistente de standup**: MCP lê commits → prompt resume → skill formata para o time.

## Entregável

1. Caso completo em `cases/<nome-do-caso>/` usando `CASE-TEMPLATE.md`.
2. Demo gravada (ou ao vivo) de 10 minutos.
3. Retrospectiva em `learn/notes/retro-8-semanas.md`.

## Critério de aceite

- [ ] Caso usa os 3 tipos de artefato (prompt, skill, MCP).
- [ ] Avaliação numérica mostra que a solução é melhor que a alternativa sem IA, ou que IA básica sem skill/MCP.
- [ ] Solução é usada por pelo menos uma pessoa fora do time construtor.
- [ ] Retrospectiva responde: o que aprendemos? o que faríamos diferente? quais os próximos 8 semanas?

## Como apresentar

Demo ao vivo. Mostre o problema, mostre a solução rodando, mostre a avaliação. Conclua com o que falhou.

## Depois disso

A v1.0.0 do repo está pronta. Hora de:

- Tornar público (definir licença antes).
- Planejar o próximo ciclo: aprofundamento em uma frente específica ou novo projeto integrador.
- Atualizar `ROADMAP.md`.
