# Roadmap

Este arquivo descreve **para onde o repo vai**. O roteiro de estudos da equipe está em `learn/roadmap/` e tem cadência semanal; este arquivo é mais alto nível.

## Versão atual: 0.1.0 — MVP estrutural

Entregue:

- Estrutura `/learn`, `/build`, `/cases`, `/ops` com tags.
- README, GLOSSARY, CONTRIBUTING, TAGS.
- Roteiro de 8 semanas com critérios de aceite.
- Templates para prompt, skill, MCP server e evaluation.
- 1 exemplo preenchido de cada artefato.

## v0.2.0 — Biblioteca de prompts

- 10 prompts arquitetados em `build/prompts/`, cada um com testes e nota mínima 70/100.
- `prompt-library.md` consolidando o catálogo.
- Scorecard preenchido para cada prompt.

## v0.3.0 — Primeiras skills funcionais

- 2 skills com `SKILL.md`, exemplos e testes.
- Skill de síntese de pesquisa funcionando ponta a ponta.
- ADR documentando padrão interno de skill.

## v0.4.0 — Primeiro MCP server

- 1 MCP server simples e auditado (sugestão: leitura de arquivos do próprio repo).
- Documentação de segurança preenchida (`ops/security/mcp-security.md`).
- Checklist de human-in-the-loop validado.

## v0.5.0 — Avaliação cruzada

- Comparação entre 3 modelos para os prompts mais críticos.
- Resultados publicados em `build/evaluations/`.
- Decisão técnica sobre modelo padrão registrada em ADR.

## v1.0.0 — Projeto integrador

- Pelo menos 1 caso real em `cases/` combinando prompt + skill + MCP.
- Demo interna gravada.
- Licença escolhida e LICENSE adicionado.
- Repo tornado público.

## Backlog (sem prioridade fixa)

- Pipeline de CI para validar front-matter dos arquivos.
- Workflow de avaliação automatizada (eval as code).
- Página estática gerada (MkDocs ou Docusaurus).
- Tradução EN do README.
