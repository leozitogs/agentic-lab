---
tipo: guide
maturidade: reviewed
versao: 0.2.0
autores: [time]
criado_em: 2026-05-28
atualizado_em: 2026-11-12
---

# Roteiro de 8 semanas

Plano de imersão para sair de "uso casual de IA" para "construção de sistemas com IA". Cada semana tem objetivo claro, leituras, entregáveis e critério de aceite. **Sem entregável, a semana não fecha.**

## Filosofia

1. **Aprendizado gera artefato.** Não basta ler — precisa virar prompt, skill, MCP, eval, caso ou ADR.
2. **Ritmo semanal.** Uma reunião por semana para apresentar entregáveis. Quem não tem entregável apresenta o que falhou.
3. **Pareamento rotativo.** A cada semana, alguém revisa o trabalho do outro. Ninguém valida o próprio artefato.
4. **Falha registrada vale ouro.** Experimento que falhou e foi documentado em `learn/notes/` vale tanto quanto um que deu certo.

## Calendário

| Semana | Tema | Pasta | Entregável principal |
|--------|------|-------|----------------------|
| 1 | Fundamentos de LLMs e agentes | `learn/roadmap/01-...` | Glossário expandido + mapa mental |
| 2 | Arquitetura de prompts | `learn/roadmap/02-...` | 10 prompts em `build/prompts/` |
| 3 | Avaliações | `learn/roadmap/03-...` | 3 evals + scorecard em `build/evaluations/` |
| 4 | Skills | `learn/roadmap/04-...` | 2 skills em `build/skills/` |
| 5 | Fundamentos de MCP | `learn/roadmap/05-...` | 1 MCP simples em `build/mcp-servers/` |
| 6 | MCP aplicado | `learn/roadmap/06-...` | 1 MCP útil para o time |
| 7 | Segurança | `learn/roadmap/07-...` | Checklist em `ops/security/` |
| 8 | Projeto integrador | `learn/roadmap/08-...` | Demo + caso em `cases/` |

## Divisão de papéis (sugestão)

A divisão é rotativa por semana para todo mundo treinar tudo, mas cada pessoa fica como **referência** de uma frente:

| Pessoa | Referência | Responsabilidade contínua |
|--------|------------|---------------------------|
| Pessoa A | Arquitetura de produto | Estrutura do repo, padrões, integração entre artefatos |
| Pessoa B | Prompts e evals | Biblioteca de prompts, scorecards, comparações entre modelos |
| Pessoa C | Agentes e MCP | Servidores MCP, automações, integrações técnicas |

## Como cada semana fecha

Toda sexta-feira, reunião de 60 minutos:

1. Cada pessoa apresenta seu entregável (10 min).
2. Pareamento de revisão (15 min).
3. O que aprendemos? O que falhou? (15 min).
4. Próxima semana: dúvidas e ajustes (10 min).
5. Atualizar `learn/notes/weekly-learnings.md`.

## Não cumprir uma semana

Acontece. A regra é: **registre o motivo**. Crie nota em `learn/notes/` explicando o que travou, e use a próxima semana pra recuperar ou ajustar o plano.

## Depois das 8 semanas

A continuação está na **trilha avançada**, em [`learn/avancado/`](../avancado/README.md): 11 módulos de ritmo livre sobre padrões de agentes, ferramentas e saídas estruturadas, RAG, memória, agentes de código, avaliação e red teaming, segurança, observabilidade, modelos abertos, multimodal e um projeto integrador.
