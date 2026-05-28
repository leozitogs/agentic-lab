# agentic-lab

> Laboratório aberto de **arquitetura de prompts**, **skills** e **MCP servers**.
> Tudo que aprendemos vira artefato reutilizável.

## O que é isso

Este repositório é um **playbook vivo** para times que querem ir além de "usar IA" e começar a **construir sistemas com IA**. Não é um curso, não é um blog, não é uma coleção de links. É uma máquina de transformar estudo em entregável.

A regra fundadora é simples: **toda coisa que entra aqui precisa responder seis perguntas**.

1. O que aprendemos?
2. Como reproduzir?
3. Quando usar?
4. Quando NÃO usar?
5. Como avaliar?
6. Como melhorar?

Se a resposta a alguma delas for "não sei", o artefato ainda não está pronto pra entrar.

## Como o repo está organizado

A arquitetura separa **aprender** de **produzir**, e marca cada arquivo com uma **tag de tipo** (ver `ops/TAGS.md`).

```
agentic-lab/
├── learn/        → onde estudamos (roadmap, glossário, notas semanais)
├── build/        → onde produzimos (prompts, skills, MCP servers, evals)
├── cases/        → onde aplicamos (estudos de caso reais)
├── ops/          → como nos organizamos (decisões, segurança, contribuição)
└── assets/       → diagramas e screenshots
```

A separação `/learn` vs `/build` é proposital. Estudar é diferente de entregar, e misturar os dois cria confusão sobre o que é maduro e o que é rascunho.

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

Versão atual: `0.1.0` (MVP de estrutura).
Próximo marco: ver `ROADMAP.md`.

## Licença

Apache License 2.0. Ver [LICENSE](LICENSE).
