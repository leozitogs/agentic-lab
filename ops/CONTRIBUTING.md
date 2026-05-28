# Como contribuir

Bem-vindo. Antes de abrir um PR, leia este arquivo inteiro. Ele é curto.

## A regra das seis perguntas

Toda contribuição precisa responder, na descrição do PR ou no próprio arquivo:

1. O que aprendemos?
2. Como reproduzir?
3. Quando usar?
4. Quando NÃO usar?
5. Como avaliar?
6. Como melhorar?

PRs que não respondem essas perguntas são fechados sem revisão.

## Tipos de contribuição

| Tipo | Pasta | Template |
|------|-------|----------|
| Prompt | `build/prompts/` | `build/prompts/PROMPT-TEMPLATE.md` |
| Skill | `build/skills/` | `build/skills/skill-template/SKILL.md` |
| MCP server | `build/mcp-servers/` | `build/mcp-servers/mcp-template/` |
| Avaliação | `build/evaluations/` | `build/evaluations/EVAL-TEMPLATE.md` |
| Caso de uso | `cases/` | `cases/CASE-TEMPLATE.md` |
| Nota de estudo | `learn/notes/` | livre |
| Decisão técnica | `ops/decisions/` | `ops/decisions/ADR-TEMPLATE.md` |

## Fluxo de PR

1. Crie uma branch a partir de `main` no padrão `tipo/descricao-curta` (ex.: `prompt/research-synthesis`).
2. Adicione o artefato com front-matter completo (ver `ops/TAGS.md`).
3. Se for prompt, skill ou MCP, faça pelo menos uma avaliação inicial.
4. Atualize o índice da pasta correspondente, se houver.
5. Abra PR. Use o template de PR do GitHub (a ser adicionado em `.github/`).
6. Pelo menos uma pessoa da equipe revisa.
7. Apresente na próxima reunião semanal.

## Padrão de commits

Convencional:

```
feat: descrição
docs: descrição
prompt: descrição
skill: descrição
mcp: descrição
eval: descrição
fix: descrição
refactor: descrição
```

Mensagens em português ou inglês — coerência interna do PR é o que importa.

## Idioma

- Documentação humana, descrições, comentários de PR: **PT-BR**.
- System prompts, instruções para agentes, exemplos consumidos por LLM: **EN**.
- Front-matter (`name`, `description`): **EN** se o artefato é consumido por agente, **PT** se é só documentação.

Esse padrão existe porque LLMs costumam performar melhor em inglês para instruções operacionais, mas a equipe trabalha em português.

## Maturidade

Use a tag `maturidade` no front-matter:

- `draft` — rascunho, ainda em construção.
- `tested` — testado pelo autor, mas sem revisão de outra pessoa.
- `reviewed` — passou por revisão de pelo menos um colega.
- `adopted` — virou padrão do time, é referência para novos artefatos.

Não promova artefato sem evidência.

## O que NÃO aceitar no repo

- Prompt sem teste documentado.
- Skill sem critério de uso claro.
- MCP sem análise de segurança.
- "Cole aqui o link do ChatGPT que ele resolve" — isso não é artefato.
- Conteúdo que dependa de informação interna não compartilhável.
