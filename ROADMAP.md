# Roadmap

Este arquivo descreve **para onde o repo vai**. O roteiro de estudos está em `learn/roadmap/` e tem cadência semanal; este arquivo é mais alto nível.

## Entregue

### 0.1.0 — MVP estrutural

- Estrutura `/learn`, `/build`, `/cases`, `/ops` com tags.
- README, GLOSSARY, CONTRIBUTING, TAGS.
- Roteiro de 8 semanas com critérios de aceite.
- Templates para prompt, skill, MCP server e evaluation.
- 1 exemplo preenchido de cada artefato.
- Licença Apache 2.0.

### 0.2.0 — Trilha avançada (versão atual)

- `learn/avancado/` com 11 módulos de ritmo livre: padrões de agentes, ferramentas e saídas estruturadas, RAG, memória, agentes de código, avaliação e red teaming, segurança, observabilidade e LLMOps, modelos abertos, multimodal e projeto integrador.
- Glossário ampliado.
- ADR-0002 registrando a organização em módulos.

### 0.2.1 — CI de verdade

- Validador de front-matter (`scripts/validate_frontmatter.py`) com testes, rodando em todo push e PR.
- Eval como código do `research-analyst` em `build/evaluations/research-analyst/`: suíte promptfoo com 5 casos, asserções determinísticas testadas contra saídas de referência e `llm-rubric` para o que exige julgamento.

### 0.2.2 — Primeiro MCP server

- `build/mcp-servers/repo-knowledge/` implementado com o SDK oficial: 3 tools somente leitura, 7 resources e 2 prompts.
- Testes de catálogo, de protocolo e de ida e volta por stdio, rodando na CI em Linux e Windows.
- Análise de segurança em `ops/security/repo-knowledge-mcp.md`.

### 0.2.3 — Site

- Site com MkDocs Material publicado no GitHub Pages a cada mudança: [leozitogs.github.io/agentic-lab](https://leozitogs.github.io/agentic-lab/).
- O conteúdo continua na raiz; `scripts/build_site.py` monta as páginas e aponta links de código para o GitHub.

## Próximos marcos

### 0.3.0 — Biblioteca de prompts

- 10 prompts arquitetados em `build/prompts/`, cada um com testes e nota mínima 70/100.
- `prompt-library.md` consolidando o catálogo.

### 0.4.0 — Skills e MCP

- 2 skills com `SKILL.md`, exemplos e testes.
- Um MCP com tool de escrita protegida por confirmação humana (human-in-the-loop).

### 0.5.0 — Kits de recuperação e avaliação

- Kit de RAG com conjunto de perguntas rotuladas e comparação de configurações (módulo 3).
- Suíte de eval com casos adversariais rodando na CI (módulo 6).

### 0.6.0 — Kits de segurança e operação

- Agente de exemplo para exercícios de prompt injection, com mitigações (módulo 7).
- Exemplo instrumentado com tracing e painel de custo (módulo 8).
- Comparação entre LLM via API, modelo aberto e classificador clássico (módulo 9).

### 1.0.0 — Projetos integradores

- Caso da trilha de fundamentos (semana 8) e caso da trilha avançada (módulo 11) em `cases/`.
- Demos gravadas.

## Backlog (sem prioridade fixa)

- Calibrar o juiz do `llm-rubric` contra avaliação humana.
- Levar o eval como código para os próximos prompts e skills.
- Tradução EN do README.
