---
tipo: guide
maturidade: reviewed
versao: 0.1.0
autores: [time]
criado_em: 2026-05-28
atualizado_em: 2026-05-28
---

# Semana 4 — Skills

## Objetivo

Transformar procedimento repetível em **pacote reutilizável**: a skill.

## Pré-requisitos

Semanas 2 e 3 fechadas (prompts e evals).

## O que estudar

1. Anatomia de uma skill: `SKILL.md`, front-matter (`name`, `description`), arquivos auxiliares.
2. **Progressive disclosure**: manter `SKILL.md` enxuto, mover detalhes para arquivos referenciados.
3. Como escrever uma `description` que dispare a skill no contexto certo.
4. Scripts auxiliares dentro de skills.
5. Quando criar skill vs. quando ficar só com prompt.
6. Testes de skill: como provar que ela é invocada quando deveria e não é quando não deveria.

## Leituras sugeridas

- Repositório `anthropics/skills` no GitHub.
- Documentação oficial de skills da Anthropic.
- Skills de exemplo já existentes em ferramentas como Claude Code / Cowork.

## Entregável

Pelo menos **2 skills funcionais** em `build/skills/`, cada uma com:

- `SKILL.md` com front-matter.
- Pelo menos um arquivo auxiliar (exemplos, referências, ou script).
- Pelo menos um teste documentado (input → output esperado).

Sugestões de skills:

- Skill de síntese de pesquisa.
- Skill de revisão de código.
- Skill de extração estruturada de PDFs.

## Critério de aceite

- [ ] 2 skills com `maturidade: tested` mínimo.
- [ ] `description` testada: a skill é invocada nos casos esperados.
- [ ] Skill funciona em ferramenta real (Claude Code, Cowork, ou similar).
- [ ] Cada skill tem pelo menos 1 caso de teste de "não-invocação" (input que NÃO deveria disparar a skill).

## Antipadrões a evitar

- `description` genérica demais (dispara em tudo).
- `SKILL.md` gigante que carrega tudo de uma vez (quebra progressive disclosure).
- Skill que duplica capacidade já presente no modelo base.
- Skill sem teste — vira código morto.

## Como apresentar

Demo ao vivo: mostre o input que **deveria** disparar a skill, e mostre o input parecido que **não deveria**.
