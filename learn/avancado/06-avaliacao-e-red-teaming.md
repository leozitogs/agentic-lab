---
tipo: guide
maturidade: draft
versao: 0.2.0
autores: [leozitogs]
criado_em: 2026-11-12
atualizado_em: 2026-11-12
---

# Módulo 06 · Avaliação e red teaming

## Objetivo

Avaliar sistemas com LLM de forma contínua e procurar falhas antes dos usuários.

## Perguntas que o módulo responde

- Como transformar "parece bom" em número?
- Como achar os casos em que o sistema quebra?

## Tópicos

1. Evals offline e online.
2. Conjuntos de teste: dourados, adversariais e de regressão.
3. LLM como juiz e sua calibração contra humanos.
4. pass@k e métricas por tarefa.
5. Red teaming manual e automatizado.
6. Critério de sucesso definido antes do experimento.

## Ferramentas para comparar

Escolha pelo menos duas e compare no mesmo exercício. O objetivo é entender o trade-off, não decorar uma ferramenta.

- promptfoo
- Inspect (UK AISI)
- DeepEval
- OpenAI Evals
- LangSmith
- Langfuse

## Leituras

- Zheng et al., "Judging LLM-as-a-Judge" (2023).
- Chen et al., "Evaluating Large Language Models Trained on Code" (2021).
- Perez et al., "Red Teaming Language Models with Language Models" (2022).

## Exercício

Escolha um artefato de `build/` e monte uma suíte de eval com casos normais, adversariais e de regressão, rodando na CI.

## Critério de aceite

- [ ] Suíte rodando com um comando.
- [ ] Pelo menos 5 casos adversariais documentados.
- [ ] Pelo menos um resultado negativo registrado em `learn/notes/`.
