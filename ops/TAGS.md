# Sistema de tags

Todo artefato no `agentic-lab` carrega tags no front-matter YAML. Isso permite filtrar, indexar e gerar relatórios sem depender da estrutura de pastas.

## Tags obrigatórias

```yaml
---
tipo: prompt | skill | mcp | eval | case | note | adr | guide
maturidade: draft | tested | reviewed | adopted
versao: 0.1.0
autores: [nome1, nome2]
criado_em: 2026-05-28
atualizado_em: 2026-05-28
---
```

## Tags opcionais

```yaml
modelos_testados: [claude-opus-4-6, claude-sonnet-4-6, gpt-5.5-thinking]
dependencias: [research-synthesis-skill, vlab-knowledge-mcp]
tags: [pesquisa, sintese, academico]
nota_avaliacao: 82
riscos: [alucinacao, vazamento-contexto]
```

## Semântica das tags principais

### `tipo`

| Valor | Significado | Onde mora |
|-------|-------------|-----------|
| `prompt` | Prompt arquitetado e testado | `build/prompts/` |
| `skill` | Pasta com `SKILL.md` | `build/skills/` |
| `mcp` | Servidor MCP | `build/mcp-servers/` |
| `eval` | Avaliação ou scorecard | `build/evaluations/` |
| `case` | Estudo de caso real | `cases/` |
| `note` | Nota de estudo | `learn/notes/` |
| `adr` | Decisão técnica registrada | `ops/decisions/` |
| `guide` | Conteúdo didático ou roteiro | `learn/roadmap/` |

### `maturidade`

| Valor | Significado |
|-------|-------------|
| `draft` | Em construção. Não use em produção. |
| `tested` | Testado pelo autor com casos reais. Aceitável usar com cuidado. |
| `reviewed` | Revisado por outra pessoa. Pronto para uso interno. |
| `adopted` | Padrão do time. Mudanças exigem ADR. |

## Por que tags em vez de só pastas

Pastas dizem **onde mora**. Tags dizem **o que é** e **como tratar**.
Um mesmo prompt pode estar pronto para adoção (`reviewed`) ou ainda em testes (`draft`), independente de qual pasta vive. A separação `/learn` vs `/build` é macro; tags resolvem o micro.

## Convenção de busca

Para encontrar tudo o que está pronto para uso:

```bash
grep -rH "maturidade: reviewed\|maturidade: adopted" --include="*.md" .
```

Para listar prompts em rascunho:

```bash
grep -rlH "tipo: prompt" --include="*.md" . | xargs grep -lH "maturidade: draft"
```
