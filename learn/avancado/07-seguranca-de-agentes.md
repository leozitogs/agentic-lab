---
tipo: guide
maturidade: draft
versao: 0.2.0
autores: [leozitogs]
criado_em: 2026-11-12
atualizado_em: 2026-11-12
---

# Módulo 07 · Segurança de agentes

## Objetivo

Entender como agentes são atacados e como reduzir o estrago quando algo der errado.

## Perguntas que o módulo responde

- O que muda na segurança quando o modelo pode agir?
- Como limitar o que um agente comprometido consegue fazer?

## Tópicos

1. Prompt injection direta e indireta.
2. Exfiltração de dados por ferramentas e links.
3. OWASP Top 10 for LLM Applications.
4. Menor privilégio, sandbox e segredos fora do contexto.
5. Human-in-the-loop para ações irreversíveis.
6. Guardrails de entrada e de saída.

## Ferramentas para comparar

Escolha pelo menos duas e compare no mesmo exercício. O objetivo é entender o trade-off, não decorar uma ferramenta.

- NeMo Guardrails
- Guardrails AI
- Llama Guard
- Sandbox com contêiner

## Leituras

- OWASP, "Top 10 for LLM Applications".
- Greshake et al., "Not what you've signed up for" (2023).
- Simon Willison, textos sobre prompt injection.

## Exercício

Monte um agente de exemplo com acesso a e-mail fictício e tente quebrá-lo com injeção indireta. Depois aplique mitigações e repita.

## Critério de aceite

- [ ] Relatório antes e depois das mitigações.
- [ ] Checklist de segurança de `ops/security/` atualizado.
