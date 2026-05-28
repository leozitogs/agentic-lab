---
tipo: guide
maturidade: reviewed
versao: 0.1.0
autores: [time]
criado_em: 2026-05-28
atualizado_em: 2026-05-28
---

# Semana 6 — MCP aplicado

## Objetivo

Construir um MCP server que **resolve um problema real** do time.

## Pré-requisitos

Semana 5 fechada (MCP fundamentos).

## O que estudar (aprofundamento)

1. Autenticação em servidores MCP (OAuth, API keys, tokens).
2. Rate limiting e cache.
3. Logs estruturados para auditoria.
4. Versionamento de schemas.
5. Distribuição: como instalar em outras máquinas.
6. Padrões de design: um servidor por integração vs. um servidor multifuncional.

## Entregável

**1 MCP server útil**, escolhido pelo time, que será usado de verdade.

Sugestões:

- Servidor que indexa documentos internos e expõe busca.
- Servidor que integra com a API de um serviço que o time usa diariamente.
- Servidor que automatiza uma tarefa repetitiva (geração de relatório, deploy, etc.).

## Critério de aceite

- [ ] Servidor em uso real por pelo menos 2 pessoas do time.
- [ ] Documentação de segurança preenchida em `ops/security/`.
- [ ] Checklist de human-in-the-loop validado para tools sensíveis.
- [ ] Logs estruturados implementados.
- [ ] README com troubleshooting.

## Antipadrões a evitar

- Servidor "interessante" mas que ninguém usa.
- Tool que executa ação destrutiva sem dry-run.
- Sem registro do que a tool fez (auditoria zero).
- Acoplamento com serviço sem fallback.

## Como apresentar

Mostre o servidor sendo usado **pela pessoa que não construiu**. Se ela conseguir resolver o problema dela, está pronto.
