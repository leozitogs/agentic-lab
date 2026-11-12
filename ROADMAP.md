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

## Próximos marcos

### 0.3.0 — Biblioteca de prompts

- 10 prompts arquitetados em `build/prompts/`, cada um com testes e nota mínima 70/100.
- `prompt-library.md` consolidando o catálogo.

### 0.4.0 — Skills e MCP

- 2 skills com `SKILL.md`, exemplos e testes.
- 1 MCP server simples e auditado, com checklist de human-in-the-loop validado.

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

- Validador de front-matter na CI (hoje é um placeholder).
- Avaliação automatizada como código (eval as code).
- Página estática gerada (MkDocs ou Docusaurus).
- Tradução EN do README.
