---
tipo: guide
maturidade: draft
versao: 0.2.0
autores: [leozitogs]
criado_em: 2026-11-12
atualizado_em: 2026-11-12
---

# Módulo 10 · Multimodal

## Objetivo

Trabalhar com imagem, áudio, vídeo e documentos como entrada de sistemas com LLM.

## Perguntas que o módulo responde

- Como extrair informação confiável de PDFs, imagens e áudios?
- Quando usar um modelo multimodal e quando pré-processar?

## Tópicos

1. Visão: OCR, layout e leitura de gráficos.
2. Áudio: transcrição e diarização.
3. Vídeo: amostragem de frames e detecção de cena.
4. Documentos longos e tabelas.
5. Custo por modalidade.

## Ferramentas para comparar

Escolha pelo menos duas e compare no mesmo exercício. O objetivo é entender o trade-off, não decorar uma ferramenta.

- Whisper e variantes
- Docling
- Unstructured
- Tesseract / PaddleOCR
- vid2llm

## Leituras

- Radford et al., "Whisper" (2022).
- Documentação de visão das APIs da Anthropic, OpenAI e Gemini.

## Exercício

Construa um pipeline que recebe uma aula gravada (vídeo público) e gera um resumo com os slides mais relevantes. Meça a qualidade com um conjunto pequeno de perguntas.

## Critério de aceite

- [ ] Pipeline reproduzível com um comando.
- [ ] Comparação entre pré-processar e mandar direto para o modelo multimodal.
