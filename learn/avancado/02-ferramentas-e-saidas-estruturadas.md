---
tipo: guide
maturidade: draft
versao: 0.2.0
autores: [leozitogs]
criado_em: 2026-11-12
atualizado_em: 2026-11-12
---

# Módulo 02 · Ferramentas e saídas estruturadas

## Objetivo

Fazer o modelo chamar ferramentas e devolver dados no formato certo, sempre.

## Perguntas que o módulo responde

- Como desenhar uma ferramenta que o modelo usa bem?
- Como garantir que a saída respeita um schema?

## Tópicos

1. Function calling e tool use.
2. JSON Schema, Pydantic e validação.
3. Ferramentas idempotentes e mensagens de erro úteis para o modelo.
4. Retry com correção a partir do erro de validação.
5. Quando usar MCP em vez de ferramenta embutida.

## Ferramentas para comparar

Escolha pelo menos duas e compare no mesmo exercício. O objetivo é entender o trade-off, não decorar uma ferramenta.

- Structured outputs nativos das APIs
- Instructor
- Pydantic AI
- Outlines
- MCP

## Leituras

- Documentação de tool use da Anthropic e de function calling da OpenAI.
- Documentação do Instructor.

## Exercício

Construa um extrator que lê notas fiscais fictícias e devolve um objeto validado. Meça a taxa de saídas válidas com e sem retry.

## Critério de aceite

- [ ] Schema versionado no repositório.
- [ ] Taxa de saídas válidas reportada em pelo menos 30 documentos sintéticos.
