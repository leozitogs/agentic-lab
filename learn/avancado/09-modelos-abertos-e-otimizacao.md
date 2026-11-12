---
tipo: guide
maturidade: draft
versao: 0.2.0
autores: [leozitogs]
criado_em: 2026-11-12
atualizado_em: 2026-11-12
---

# Módulo 09 · Modelos abertos e otimização

## Objetivo

Saber quando um modelo aberto, pequeno ou ajustado resolve melhor que um modelo grande via API.

## Perguntas que o módulo responde

- Quando vale rodar modelo local?
- Fine-tuning, RAG ou prompt: qual resolve meu problema?

## Tópicos

1. Ecossistema de modelos abertos e licenças.
2. Servir modelos: Ollama, llama.cpp, vLLM.
3. Quantização e seus efeitos na qualidade.
4. Fine-tuning com LoRA/QLoRA.
5. Destilação de um modelo grande para um pequeno.
6. Modelos clássicos de ML quando o problema é tabular.

## Ferramentas para comparar

Escolha pelo menos duas e compare no mesmo exercício. O objetivo é entender o trade-off, não decorar uma ferramenta.

- Ollama
- llama.cpp
- vLLM
- Hugging Face Transformers + PEFT
- Unsloth
- scikit-learn

## Leituras

- Hu et al., "LoRA" (2021).
- Dettmers et al., "QLoRA" (2023).
- Hinton et al., "Distilling the Knowledge in a Neural Network" (2015).

## Exercício

Classifique tickets de suporte sintéticos com (a) um LLM grande via API, (b) um modelo aberto local e (c) um classificador clássico. Compare acerto, custo e latência.

## Critério de aceite

- [ ] Tabela com as três abordagens no mesmo conjunto de teste.
- [ ] Recomendação para cada faixa de volume.
