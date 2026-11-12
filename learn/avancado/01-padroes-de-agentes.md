---
tipo: guide
maturidade: draft
versao: 0.2.0
autores: [leozitogs]
criado_em: 2026-11-12
atualizado_em: 2026-11-12
---

# Módulo 01 · Padrões de agentes

## Objetivo

Reconhecer os padrões clássicos de sistemas com LLM e escolher o mais simples que resolve o problema.

## Perguntas que o módulo responde

- Quando um workflow fixo basta e quando vale um agente?
- Como dividir trabalho entre vários modelos sem perder o controle?

## Tópicos

1. Prompt chaining, roteamento e paralelização.
2. Orchestrator-workers e evaluator-optimizer.
3. ReAct, plan-and-execute e reflexão.
4. Agente único com ferramentas versus vários agentes.
5. Critérios de parada e limites de iteração.

## Ferramentas para comparar

Escolha pelo menos duas e compare no mesmo exercício. O objetivo é entender o trade-off, não decorar uma ferramenta.

- OpenAI Agents SDK
- Claude Agent SDK
- LangGraph
- CrewAI
- AutoGen
- Implementação "na mão" com a API do modelo

## Leituras

- Anthropic, "Building effective agents" (2024).
- Yao et al., "ReAct" (2022).
- Shinn et al., "Reflexion" (2023).

## Exercício

Resolva o mesmo problema (ex.: responder perguntas sobre um conjunto de PDFs públicos) de três jeitos: workflow fixo, agente único e dois agentes. Compare acerto, custo e tempo.

## Critério de aceite

- [ ] Tabela comparando os três desenhos no mesmo conjunto de perguntas.
- [ ] Recomendação justificada de qual usar e por quê.
