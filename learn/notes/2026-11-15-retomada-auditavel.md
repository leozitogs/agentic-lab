---
tipo: note
maturidade: tested
versao: 0.1.0
autores: [leozitogs]
criado_em: 2026-11-15
atualizado_em: 2026-11-15
tags: [vivencia, avaliacao, reprodutibilidade]
---

# Retomada auditável do kit de segurança

## Contexto

Durante a análise do próprio laboratório, encontramos dois pontos no executor de prompt injection. O cache considerava nomes de modelo e IDs de casos sem identificar mudanças no código ou nos dados. As respostas também eram truncadas antes de preservar sua versão completa. Isso dificultava comparar revisões e auditar conclusões.

## O que foi feito e observado

A contribuição [PR #1](https://github.com/leozitogs/agentic-lab/pull/1) adicionou manifesto por conteúdo, diário completo, recuperação de cauda interrompida e publicação serializada. Um LLM com contexto independente revisou o plano e encontrou risco de concorrência entre publicações. Na revisão do código, encontrou perda do histórico de tentativas no artefato publicado e configurações duplicadas. As observações levaram a correções e testes específicos. O [parecer](../../build/evaluations/prompt-injection/plan-review.md) registra o escopo dessa revisão automatizada.

Na entrega, passaram 77 testes do kit e 19 testes da raiz. O relatório científico histórico foi regenerado sem diferenças. As duas verificações de CI do PR passaram antes do merge. Esses resultados verificam a infraestrutura entregue. A eficácia das defesas continua dependente de novas execuções com modelos.

## Como reproduzir

Use o commit `dc2f74e` do PR ou uma revisão posterior que o contenha. Na pasta `build/evaluations/prompt-injection/`, execute `python -m unittest discover -s tests -v`. O README do kit explica a execução com modelo e revisão imutável. Registre seu sistema, versão de Python, revisão Git e eventuais diferenças.

## Aprendizado e limites

Retomar uma avaliação exige identificar o experimento e preservar as tentativas anteriores. A revisão independente encontrou falhas que a proposta inicial não cobria. A revisão por LLM utilizou o mesmo modelo da sessão, com contexto novo, e teve alcance estático. Revisão humana e execução real de novos experimentos continuam como formas de ampliar a evidência.

## Próxima colaboração

Reproduza os testes em outro ambiente ou execute uma rodada com um snapshot de modelo registrado. Abra issue com resultados, erros e contexto. Uma próxima contribuição pode avaliar a combinação de três camadas recomendada pelo ADR-0004 e comparar sua utilidade por tarefa.

## Crédito

Autoria de Leonardo Gonçalves Sobral. Assistência de Codex na análise, implementação e testes, com revisão automatizada em contexto independente. O PR preserva a autoria Git e os resultados das verificações.
