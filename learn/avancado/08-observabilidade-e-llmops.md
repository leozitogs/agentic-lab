---
tipo: guide
maturidade: draft
versao: 0.2.0
autores: [leozitogs]
criado_em: 2026-11-12
atualizado_em: 2026-11-12
---

# Módulo 08 · Observabilidade e LLMOps

## Objetivo

Operar sistemas com LLM em produção: ver o que acontece, quanto custa e quando degrada.

## Perguntas que o módulo responde

- Por que o sistema respondeu isso?
- Quanto custa cada tarefa e onde dá para economizar?

## Tópicos

1. Tracing de chamadas e ferramentas.
2. Versionamento de prompts e de modelos.
3. Custo, latência e cache de prompt.
4. Processamento em lote.
5. Monitoramento de qualidade em produção e alertas.
6. Implantação gradual e rollback.

## Ferramentas para comparar

Escolha pelo menos duas e compare no mesmo exercício. O objetivo é entender o trade-off, não decorar uma ferramenta.

- OpenTelemetry (GenAI semantic conventions)
- Langfuse
- Arize Phoenix
- Helicone
- LangSmith

## Leituras

- Documentação de prompt caching e batch das APIs.
- OpenTelemetry, convenções semânticas para GenAI.

## Exercício

Instrumente um dos artefatos do repositório com tracing e produza um painel com custo, latência e taxa de erro por versão de prompt.

## Critério de aceite

- [ ] Traces navegáveis de ponta a ponta.
- [ ] Comparação de custo antes e depois de ativar cache.
