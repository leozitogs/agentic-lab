---
tipo: adr
maturidade: adopted
versao: 0.1.0
autores: [time]
criado_em: 2026-05-28
atualizado_em: 2026-05-28
status: aceito
---

# ADR-0001 — Separar /learn de /build com sistema de tags

## Status

Aceito.

## Contexto

A primeira proposta usava pastas numeradas (`00-start-here`, `01-study-roadmap`, ...). Isso é familiar e impõe ordem de leitura, mas mistura **conteúdo de estudo** (notas, leituras, glossário) com **conteúdo de produção** (prompts, skills, MCPs, evals). Em repositórios públicos com colaboradores externos, essa mistura confunde:

- Quem chega para estudar não sabe o que está pronto vs. rascunho.
- Quem chega para usar artefatos precisa navegar entre notas pessoais e código.
- Reviewers acabam sendo permissivos com notas e rigorosos com código, mesmo na mesma pasta.

## Decisão

1. Estrutura de primeiro nível separa `learn/` (estudar) de `build/` (produzir), com `cases/` (aplicar) e `ops/` (organizar) ao lado.
2. Todo artefato carrega **tags no front-matter** (`tipo`, `maturidade`, `versao`) — ver `ops/TAGS.md`.
3. Pastas dizem **onde mora**; tags dizem **o que é** e **como tratar**.

## Consequências

### Positivas

- Visitante externo entende em 30 segundos o que é estudo e o que é asset.
- Reviewers usam critérios diferentes para `learn/` e `build/` sem ambiguidade.
- Tags permitem filtrar por maturidade independente de pasta.
- Promoção de maturidade (`draft → tested → reviewed → adopted`) é mecânica clara.

### Negativas

- Mais convenção para internalizar no onboarding.
- Front-matter exige disciplina; PR de quem esquece volta.

### Neutras

- Dois "índices" coexistem: organização física (pastas) e organização lógica (tags). Documentar bem em `ops/TAGS.md` resolve.

## Alternativas consideradas

| Alternativa | Por que não |
|-------------|-------------|
| Pastas numeradas (00-08) | Mistura estudo e produção; promoção de maturidade fica ambígua. |
| Pastas por maturidade (`drafts/`, `production/`) | Move artefato de pasta a cada promoção, quebra links. |
| Só tags, sem separação macro | Visitante sem ferramenta de filtragem se perde no `ls`. |

## Referências

- Discussão inicial: conversa com ChatGPT 5.5 Thinking.
- Conceito de tags inspirado em padrões de documentação como Diátaxis.
