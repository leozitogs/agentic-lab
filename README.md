# agentic-lab

> Laboratório aberto de **prática e engenharia de IA**.
> Da arquitetura de prompts a agentes em produção: tudo que aprendemos vira artefato reutilizável.
>
> 📖 Leia como site: **[leozitogs.github.io/agentic-lab](https://leozitogs.github.io/agentic-lab/)**

## O que é isso

Este repositório é um **playbook vivo** para pessoas e equipes que utilizam, estudam e constroem com IA. Reúne vivências de diferentes áreas, conhecimento de domínio e engenharia para transformar perguntas e práticas em aprendizado compartilhado e artefatos reutilizáveis.

A regra fundadora é simples: **toda coisa que entra aqui precisa responder seis perguntas**.

1. O que aprendemos?
2. Como reproduzir?
3. Quando usar?
4. Quando NÃO usar?
5. Como avaliar?
6. Como melhorar?

Essas perguntas orientam a evolução dos artefatos. Experiências em andamento podem entrar como `draft`, com incertezas explícitas e um próximo passo de colaboração.

## Objeto de estudo

O laboratório estuda como **construir sistemas com IA que dá para confiar**: que resolvem o problema, mostram de onde tiraram cada informação, respeitam limites e são medidos.

### Trilha de fundamentos · 8 semanas · [`learn/roadmap/`](learn/roadmap/00-overview.md)

Fundamentos de LLMs e agentes, arquitetura de prompts, avaliações, skills, MCP (do protocolo ao servidor útil), segurança e um projeto integrador.

### Trilha avançada · 11 módulos de ritmo livre · [`learn/avancado/`](learn/avancado/README.md)

| Base | Aprofundamento (qualquer ordem) | Fechamento |
|---|---|---|
| 01 Padrões de agentes | 05 Agentes de código no dia a dia | 11 Projeto integrador |
| 02 Ferramentas e saídas estruturadas | 06 Avaliação e red teaming | |
| 03 RAG e recuperação | 07 Segurança de agentes | |
| 04 Memória e estado | 08 Observabilidade e LLMOps | |
| | 09 Modelos abertos e otimização | |
| | 10 Multimodal | |

Todo módulo compara **pelo menos duas ferramentas** no mesmo exercício e usa só **dados públicos ou sintéticos**.

## Ferramentas comparadas

O laboratório não adota uma stack única: compara alternativas e registra a escolha em ADR.

| Frente | Alternativas estudadas |
|---|---|
| Agentes e orquestração | OpenAI Agents SDK, Claude Agent SDK, LangGraph, CrewAI, AutoGen |
| Ferramentas e protocolos | MCP, function calling, Instructor, Pydantic AI |
| Recuperação | pgvector, Qdrant, Chroma, OpenSearch, LlamaIndex, rerankers |
| Memória | Mem0, Letta, checkpointers |
| Agentes de código | Claude Code, Codex CLI, Cursor, GitHub Copilot, Aider |
| Avaliação | promptfoo, Inspect, DeepEval, RAGAS, LangSmith |
| Segurança | NeMo Guardrails, Guardrails AI, Llama Guard, sandboxes |
| Observabilidade | OpenTelemetry, Langfuse, Arize Phoenix, Helicone |
| Modelos | APIs da Anthropic, OpenAI e Gemini; Ollama, llama.cpp, vLLM, Hugging Face, Unsloth |
| Multimodal | Whisper, Docling, Unstructured, OCR |

## Como o repo está organizado

A arquitetura separa **aprender** de **produzir**, e marca cada arquivo com uma **tag de tipo** (ver `ops/TAGS.md`).

```
agentic-lab/
├── learn/        → onde estudamos (roadmap, trilha avançada, glossário, notas)
├── build/        → onde produzimos (prompts, skills, MCP servers, evals)
├── cases/        → onde aplicamos (estudos de caso reais)
├── ops/          → como nos organizamos (decisões, segurança, contribuição)
└── assets/       → diagramas e screenshots
```

A separação `/learn` vs `/build` é proposital. Estudar é diferente de entregar, e misturar os dois cria confusão sobre o que é maduro e o que é rascunho.

## Participe do laboratório

Você pode chegar com uma pergunta, relatar uma tentativa, compartilhar conhecimento de design, pedagogia, administração ou qualquer outra área, acolher participantes, revisar ou construir artefatos. O trabalho é assíncrono e inclui pessoas em diferentes etapas de aprendizado. A escuta ativa faz parte da formulação de problemas e das decisões.

- [Matriz de contribuições e escuta ativa](ops/MATRIZ-DE-CONTRIBUICOES.md) — modalidades, critérios e apoio para participar.
- [Como contribuir](CONTRIBUTING.md) — primeira tarefa, fork, PR e critérios de revisão.
- [Vivências e aprendizados](learn/notes/README.md) — relatos, dúvidas e resultados negativos.
- [Ambiente técnico](ops/DEVELOPMENT.md) — execute `python scripts/check.py` para verificar o núcleo offline.
- [Governança](ops/GOVERNANCE.md) — papéis, decisões, crédito e manutenção.
- [Abra uma issue](https://github.com/leozitogs/agentic-lab/issues/new/choose) — problema, proposta ou experiência.

## Por onde começar

Se você acabou de chegar, leia nesta ordem:

1. `ops/CONTRIBUTING.md` — como contribuir e padrão de PR.
2. `learn/glossary/GLOSSARY.md` — linguagem comum do time.
3. `learn/roadmap/00-overview.md` — visão geral do roteiro de 8 semanas.
4. `build/prompts/PROMPT-TEMPLATE.md` — como documentar um prompt.
5. `build/skills/skill-template/SKILL.md` — como estruturar uma skill.

## Princípios

1. **Artefato sobre anotação.** Aprendeu algo? Vira template, skill, prompt ou eval.
2. **Tudo é versionado.** Prompts têm `v0.1`, skills têm changelog, MCPs têm tag.
3. **Avaliação antes de adoção.** Nada vira "padrão do time" sem scorecard.
4. **Documentação em português, instrução para IA em inglês.** A doc humana é em PT-BR; system prompts e instruções operacionais ficam em EN porque LLMs respondem melhor.
5. **Humano no loop em qualquer ação destrutiva.** MCPs com tools que escrevem em sistemas reais exigem confirmação explícita.

## Convenções

- **Idioma:** documentação humana em PT-BR. Prompts, system instructions e arquivos consumidos por agentes em EN.
- **Nomenclatura:** kebab-case para pastas e arquivos. `SKILL.md` e `README.md` em CAPS.
- **Tags:** todo arquivo tem `tipo`, `maturidade` e `versão` no front-matter. Ver `ops/TAGS.md`.
- **Commits:** convencional (`feat:`, `docs:`, `eval:`, `skill:`, `mcp:`, `prompt:`).

## Status

Versão atual: `0.2.5`: [site no GitHub Pages](https://leozitogs.github.io/agentic-lab/), trilha avançada em módulos ([ADR-0002](ops/decisions/ADR-0002-trilha-avancada.md)), validador de front-matter na CI, o primeiro [eval como código](build/evaluations/research-analyst/README.md), o primeiro [servidor MCP](build/mcp-servers/repo-knowledge/README.md), o [kit de RAG](build/evaluations/rag-recuperacao/README.md) do módulo 03 ([ADR-0003](ops/decisions/ADR-0003-recuperacao-padrao-rag.md)) e o [kit de prompt injection](build/evaluations/prompt-injection/README.md) do módulo 07 ([ADR-0004](ops/decisions/ADR-0004-mitigacoes-prompt-injection.md)).
Próximo marco: ver `ROADMAP.md`.

## Licença

Apache License 2.0. Ver [LICENSE](LICENSE).
