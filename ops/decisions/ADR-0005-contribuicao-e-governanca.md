---
tipo: adr
maturidade: draft
versao: 0.1.0
autores: [leozitogs]
criado_em: 2026-11-15
atualizado_em: 2026-11-15
status: proposto
---

# ADR-0005 · Contribuição aberta e governança do laboratório

## Contexto

O laboratório já possui trilhas, artefatos, testes e publicação. O guia de contribuição estava apenas em ops, faltavam templates de entrada e revisão e havia dependência de reunião semanal. A main estava sem proteção na consulta inicial ao GitHub. A equipe de manutenção registrada tem uma pessoa.

## Proposta

Adotar entrada pública pelo CONTRIBUTING da raiz, issues para bugs/propostas/vivências, notas em draft, processo assíncrono e critérios proporcionais ao impacto. Definir papéis, crédito, revisão humana e limites da revisão por IA. Manter a organização learn/build/cases/ops existente.

Oferecer `python scripts/check.py` como entrada técnica offline. Executar o check agregado `lab-check` em todo PR, em Linux e Windows. Verificar build do site em PRs. Versionar a proteção da main com PR e CI obrigatórios, resolução de conversas e bloqueio de force push e exclusão. Começar com zero aprovações obrigatórias enquanto há um mantenedor, mantendo revisão de outra pessoa como condição para maturidade reviewed.

## Consequências

Novos participantes podem começar por uma dúvida ou relato e encontrar os comandos necessários para uma contribuição técnica. Revisores conseguem distinguir experiência em construção de resultados avaliados. A manutenção precisa manter orientação, triagem, índices e ownership atualizados.

A configuração remota depende de aplicação por um administrador e deve ser verificada pela API. A CI offline valida implementação e metadados, enquanto execuções científicas seguem seus próprios protocolos. Quando houver mais mantenedores ativos, a contagem de aprovações e os responsáveis podem ser alterados em decisão pública.

## Alternativas consideradas

Reunião como etapa obrigatória restringe participação assíncrona. Aprovação obrigatória de outra pessoa com apenas um mantenedor pode impedir o fluxo de integração. Aceitar artefatos exclusivamente maduros elimina relatos que ainda precisam de colaboração. O desenho proposto permite entrada gradual, mantendo critérios explícitos para adoção.

## Referências

A [governança](../GOVERNANCE.md) documenta as bases consultadas. O [ambiente técnico](../DEVELOPMENT.md) e a [operação do GitHub](../GITHUB.md) detalham os procedimentos.
