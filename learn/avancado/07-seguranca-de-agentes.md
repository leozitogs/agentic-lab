---
tipo: guide
maturidade: draft
versao: 0.2.1
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

## Kit pronto

O exercício já tem uma versão de referência em [`build/evaluations/prompt-injection/`](../../build/evaluations/prompt-injection/README.md): um agente de e-mail com laço de tool-calling próprio, uma caixa de entrada fictícia, 4 tarefas legítimas e 6 injeções indiretas (instrução no corpo, comentário HTML, assinatura, anexo, urgência falsa e mensagem falsa do sistema). O [relatório](../../build/evaluations/prompt-injection/results/report.md) mede ASR e utilidade, antes e depois de quatro mitigações da literatura (spotlighting, menor privilégio com aprovação humana, filtro de URLs na saída e dual LLM), isoladas e combinadas, num modelo local via Ollama. Na rodada registrada, a linha de base teve ASR 0.23 (todo ele por link ou imagem markdown na resposta); o filtro de saída sozinho levou a 0.00, o spotlighting a 0.04, e a combinação das quatro chegou a ASR 0.00 sem nenhuma tentativa, com utilidade sem ataque de 1.00. As mitigações padrão resultantes estão na [ADR-0004](../../ops/decisions/ADR-0004-mitigacoes-prompt-injection.md), e o [checklist de segurança](../../ops/security/checklist.md) ganhou uma seção para agentes com ferramentas.

Use o kit como molde: troque as ferramentas e as tarefas pelas do seu agente, escreva injeções para os canais que ele lê e rode de novo. A comparação com guardrails prontos (NeMo Guardrails, Llama Guard, Guardrails AI) que o módulo pede ainda não está no kit.

## Critério de aceite

- [ ] Relatório antes e depois das mitigações.
- [ ] Checklist de segurança de `ops/security/` atualizado.
