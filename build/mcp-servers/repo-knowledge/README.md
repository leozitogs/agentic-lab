---
tipo: mcp
maturidade: draft
versao: 0.1.0
autores: [time]
criado_em: 2026-05-28
atualizado_em: 2026-05-28
---

# repo-knowledge MCP Server

## Objetivo

Expor o conteúdo do próprio `agentic-lab` (prompts, skills, MCPs, evals, cases) como **resources** consultáveis por um cliente MCP, e oferecer **tools** de busca por tag, maturidade e tipo.

Esse MCP serve como dogfood: o time usa o próprio repo via agente para acelerar consultas.

## Tools

| Nome | Descrição | Risco |
|------|-----------|-------|
| `search_artifacts` | Busca artefatos por query, tipo, tag, maturidade | leitura |
| `get_artifact` | Retorna conteúdo completo de um artefato por path | leitura |
| `list_by_tag` | Lista artefatos com determinada tag | leitura |

Sem tools destrutivas nesta versão — propositalmente.

## Resources

| URI | Descrição |
|-----|-----------|
| `repo://prompts/index` | Índice de todos os prompts |
| `repo://skills/index` | Índice de todas as skills |
| `repo://mcps/index` | Índice de todos os MCP servers |
| `repo://cases/index` | Índice de casos de uso |
| `repo://artifact/<path>` | Conteúdo de um arquivo específico |

## Prompts

| Nome | Descrição |
|------|-----------|
| `find_similar_prompt` | Dado um objetivo, sugere prompts existentes que podem servir |
| `find_skill_for_task` | Dada uma tarefa, sugere skills aplicáveis |

## Setup

```bash
# A partir de build/mcp-servers/repo-knowledge/
python -m venv .venv && source .venv/bin/activate
pip install -e .
export REPO_ROOT=/caminho/para/agentic-lab
python -m repo_knowledge_server
```

## Configuração em Claude Desktop

```json
{
  "mcpServers": {
    "repo-knowledge": {
      "command": "python",
      "args": ["-m", "repo_knowledge_server"],
      "env": {
        "REPO_ROOT": "/caminho/para/agentic-lab"
      }
    }
  }
}
```

## Segurança

- Sem tools de escrita: nada pode modificar o repo via MCP.
- `REPO_ROOT` é o único caminho lido; tentativas de path traversal são rejeitadas.
- Front-matter é parseado com schema estrito.
- Logs estruturados em stderr (não no canal MCP).

Análise completa: `ops/security/repo-knowledge-mcp.md` (a criar).

## Status

Especificação inicial. Implementação prevista para Semana 5 do roteiro.

## Próximos passos

- Implementar em Python usando `mcp` SDK oficial.
- Adicionar busca full-text com índice em memória.
- Considerar exposição como resource subscription (atualização automática quando arquivo muda).
