---
tipo: guide
maturidade: reviewed
versao: 0.1.0
autores: [time]
criado_em: 2026-05-28
atualizado_em: 2026-05-28
---

# Semana 7 — Segurança

## Objetivo

Mapear riscos de prompts, skills e MCPs, e criar checklist operacional do time.

## Pré-requisitos

Semanas 4, 5 e 6 fechadas.

## O que estudar

1. **Prompt injection**: direta e indireta (via documentos, páginas web, resources).
2. **Data exfiltration**: como dados sensíveis vazam por tools ou contexto.
3. **Confused deputy**: agente sendo usado como vetor.
4. **Tool misuse**: ação destrutiva acionada por engano.
5. Padrões defensivos: allowlists, confirmação humana, dry-run, sandboxing.
6. Auditoria: logs estruturados, tracing de tool calls.
7. Privacidade: dados pessoais, LGPD, retenção.
8. Modelos de ameaça aplicados a sistemas com IA.

## Leituras sugeridas

- OWASP Top 10 for LLM Applications.
- Documentação de segurança do MCP.
- Casos públicos de prompt injection bem-sucedido.

## Entregável

1. **Checklist de segurança** em `ops/security/checklist.md`.
2. **Análise de risco** de pelo menos 1 prompt, 1 skill e 1 MCP existentes no repo.
3. **ADR** registrando padrão do time para human-in-the-loop.

## Critério de aceite

- [ ] Checklist cobre prompts, skills e MCPs.
- [ ] Pelo menos 1 vulnerabilidade real encontrada e documentada.
- [ ] Padrão de HITL definido e aplicado retroativamente aos MCPs existentes.
- [ ] Logs de auditoria implementados onde aplicável.

## Antipadrões a evitar

- "Não tem dado sensível aqui" como justificativa para pular.
- Checklist genérico copiado da internet.
- Análise de risco que não vira mudança no código.

## Como apresentar

Mostre **uma vulnerabilidade real** encontrada no próprio repo, e a correção aplicada.
