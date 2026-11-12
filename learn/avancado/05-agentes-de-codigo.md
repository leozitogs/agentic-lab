---
tipo: guide
maturidade: draft
versao: 0.2.0
autores: [leozitogs]
criado_em: 2026-11-12
atualizado_em: 2026-11-12
---

# Módulo 05 · Agentes de código no dia a dia

## Objetivo

Usar assistentes e agentes de programação com produtividade e sem perder a qualidade do código.

## Perguntas que o módulo responde

- O que delegar e o que manter na mão?
- Como revisar código gerado por IA?

## Tópicos

1. Arquivos de instrução do repositório (CLAUDE.md, AGENTS.md, regras do editor).
2. Especificar antes de pedir: issue bem escrita, critérios de aceite, testes.
3. TDD com agentes.
4. Revisão de código gerado: o que olhar primeiro.
5. Riscos: dependências inventadas, segredos, código que passa no teste e está errado.

## Ferramentas para comparar

Escolha pelo menos duas e compare no mesmo exercício. O objetivo é entender o trade-off, não decorar uma ferramenta.

- Claude Code
- Codex CLI
- Cursor
- GitHub Copilot
- Aider

## Leituras

- Documentação oficial de cada ferramenta escolhida.
- Jimenez et al., "SWE-bench" (2023).

## Exercício

Implemente a mesma feature pequena em um repositório de exemplo com duas ferramentas diferentes. Compare tempo, número de correções e qualidade dos testes.

## Critério de aceite

- [ ] Relato honesto do que funcionou e do que não funcionou.
- [ ] Checklist de revisão de código gerado por IA em `ops/`.
