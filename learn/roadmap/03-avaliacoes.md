---
tipo: guide
maturidade: reviewed
versao: 0.1.0
autores: [time]
criado_em: 2026-05-28
atualizado_em: 2026-05-28
---

# Semana 3 — Avaliações

## Objetivo

Aprender a **medir** qualidade. Sem avaliação, prompt engineering vira achismo.

## Pré-requisitos

Semana 2 fechada (prompts documentados).

## O que estudar

1. Critérios de qualidade: precisão, completude, formato, segurança, tom.
2. **Golden sets**: como construir um conjunto de referência.
3. Avaliação manual vs. avaliação automatizada.
4. **LLM-as-judge**: usar um modelo para avaliar outro.
5. Métricas: acurácia, F1, BLEU, ROUGE, e quando cada uma faz sentido.
6. Reprodutibilidade: seed, temperatura, versão do modelo.
7. Detecção de alucinação.
8. Comparação cruzada entre modelos.

## Leituras sugeridas

- Documentação de evals da OpenAI ou Anthropic.
- Artigo sobre LLM-as-judge.
- Discussões sobre limitações de métricas automáticas.

## Entregável

Pelo menos **3 avaliações completas** em `build/evaluations/`:

1. Eval de um prompt da Semana 2.
2. Eval comparando 2 modelos para a mesma tarefa.
3. Eval de robustez (mesmo prompt, inputs adversariais).

Cada eval deve usar `EVAL-TEMPLATE.md` e produzir scorecard.

## Critério de aceite

- [ ] 3 evals com scorecard preenchido.
- [ ] Pelo menos um eval revela falha não-óbvia do artefato avaliado.
- [ ] Eval comparativo gera ADR em `ops/decisions/` recomendando um modelo.
- [ ] Conjunto de teste (golden set) versionado junto com o eval.

## Antipadrões a evitar

- Avaliar com 2 casos e dizer "passou".
- Critérios subjetivos sem rubrica.
- Comparar modelos com prompts diferentes (não é comparação justa).
- Ignorar variância: mesmo modelo, mesma input, outputs diferentes.

## Como apresentar

Mostre **um caso onde o artefato falhou**. Explique por quê e proponha melhoria.
