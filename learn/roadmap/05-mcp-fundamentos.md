---
tipo: guide
maturidade: reviewed
versao: 0.1.0
autores: [time]
criado_em: 2026-05-28
atualizado_em: 2026-05-28
---

# Semana 5 — Fundamentos de MCP

## Objetivo

Entender o protocolo MCP até conseguir escrever um servidor simples do zero.

## Pré-requisitos

Semana 4 fechada (skills). Conforto com Python ou TypeScript.

## O que estudar

1. O que é o Model Context Protocol e por que existe.
2. Arquitetura cliente-servidor MCP.
3. Três primitivas: **tools**, **resources**, **prompts**.
4. Transportes: stdio, SSE, HTTP streaming.
5. SDK oficial em Python e TypeScript.
6. Como Claude Desktop / Cursor / VS Code consomem servidores MCP.
7. Schemas JSON para tools.
8. Tratamento de erros e idempotência.

## Leituras sugeridas

- Especificação oficial: modelcontextprotocol.io.
- SDK oficial (`python-sdk` ou `typescript-sdk`).
- Exemplos de servidores em `modelcontextprotocol/servers`.

## Entregável

**1 MCP server simples** em `build/mcp-servers/`, com:

- README explicando setup.
- Pelo menos 1 tool, 1 resource e 1 prompt.
- Teste manual documentado.
- Instruções de instalação em Claude Desktop ou cliente similar.

Sugestão: servidor que expõe os artefatos do próprio `agentic-lab` como resources e oferece uma tool de busca.

## Critério de aceite

- [ ] Servidor roda localmente.
- [ ] Cliente MCP (Claude Desktop, Cursor, etc.) consegue se conectar.
- [ ] Tool é invocada e retorna resultado esperado.
- [ ] Resource é listado e lido.
- [ ] Prompt é invocado corretamente.

## Antipadrões a evitar

- Tool sem schema claro de input.
- Tool que faz operação destrutiva sem confirmação.
- Servidor sem tratamento de erro (crasha no primeiro input ruim).
- Mistura de responsabilidades: um servidor para mil coisas.

## Como apresentar

Demo ao vivo conectando no cliente, listando tools, invocando uma e mostrando resultado.
