---
tipo: mcp
maturidade: tested
versao: 0.2.0
autores: [leozitogs]
criado_em: 2026-05-28
atualizado_em: 2026-11-12
tags: [mcp, dogfood, somente-leitura]
---

# repo-knowledge MCP Server

## Objetivo

Expor o conteúdo do próprio `agentic-lab` (prompts, skills, MCPs, evals, casos, ADRs e guias) a qualquer cliente MCP, com busca por palavra-chave, tipo, maturidade e tag. É dogfood: o laboratório consulta a si mesmo por um agente.

**Somente leitura, de propósito.** Nenhuma tool escreve, apaga ou executa nada.

## Tools

| Nome | O que faz | Risco |
|------|-----------|-------|
| `search_artifacts` | Busca por palavras-chave, com filtros opcionais `tipo`, `maturidade` e `tag`. Devolve cartões estruturados (caminho, título, resumo, maturidade, URI) | leitura |
| `get_artifact` | Devolve o Markdown completo de um artefato pelo caminho | leitura |
| `list_by_tag` | Lista os artefatos com uma tag | leitura |

Todas as tools são anunciadas com `readOnlyHint: true` e `destructiveHint: false`.

## Resources

| URI | Conteúdo |
|-----|----------|
| `repo://prompts/index` | Índice de prompts |
| `repo://skills/index` | Índice de skills |
| `repo://mcps/index` | Índice de servidores MCP |
| `repo://evals/index` | Índice de avaliações |
| `repo://cases/index` | Índice de casos |
| `repo://guides/index` | Índice de guias de estudo |
| `repo://artifact/{+path}` | Markdown de um artefato (ex.: `repo://artifact/build/prompts/system/research-analyst.md`) |

## Prompts

| Nome | O que faz |
|------|-----------|
| `find_similar_prompt` | Dado um objetivo, orienta o modelo a buscar e comparar prompts existentes |
| `find_skill_for_task` | Dada uma tarefa, orienta o modelo a buscar as skills que se aplicam |

## Instalação

Requer Python 3.10+. A partir desta pasta:

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate    Windows: .venv\Scripts\activate
pip install .
repo-knowledge          # sobe o servidor via stdio
```

Por padrão o servidor lê o repositório em que está instalado. Para apontar para outro clone, defina `REPO_ROOT`.

## Conectar a um cliente

**Claude Code**

```bash
claude mcp add repo-knowledge -- python -m repo_knowledge_server
```

**Claude Desktop, Cursor e outros** (`mcpServers` no arquivo de configuração do cliente):

```json
{
  "mcpServers": {
    "repo-knowledge": {
      "command": "python",
      "args": ["-m", "repo_knowledge_server"],
      "env": { "REPO_ROOT": "/caminho/para/agentic-lab" }
    }
  }
}
```

## Testes

```bash
python -m unittest discover -s tests -v
```

| Suíte | O que cobre |
|---|---|
| `test_catalog.py` | Indexação só de artefatos com front-matter, título e resumo, busca (ranking, acentos, filtros), tags, leitura e **bloqueio de caminhos inseguros** (`..`, absolutos, `C:/`, ocultos, não-`.md`, byte nulo, fora das pastas expostas) |
| `test_server.py` | Pelo protocolo MCP: lista as primitivas, confere que toda tool é somente leitura, busca, leitura, recusa de traversal, resources, prompts e uma **ida e volta por stdio com o cliente oficial**, como um cliente real faria |

A CI (`.github/workflows/mcp-repo-knowledge.yml`) roda tudo em Linux e Windows, com Python 3.10 e 3.13.

## Segurança

- Só lê arquivos `.md` dentro de `learn/`, `build/`, `cases/`, `ops/decisions/` e da raiz do repositório.
- Recusa caminho absoluto, `..`, letra de drive, byte nulo, pastas ocultas e arquivos acima de 200 KB. O SDK também rejeita traversal nos resources; a checagem do servidor é uma segunda camada.
- Erros esperados voltam como mensagem clara para o modelo (`ToolError`), sem traceback.
- Logs vão para stderr, nunca para o canal MCP.

Análise completa: [`ops/security/repo-knowledge-mcp.md`](../../../ops/security/repo-knowledge-mcp.md).

## Stack

Python, SDK oficial do MCP (`mcp` 2.3.0, `MCPServer`), transporte stdio. Sem dependências além do SDK.

## Próximos passos

- Notificar o cliente quando um arquivo do repositório mudar (subscriptions).
- Transporte Streamable HTTP para uso remoto, com autenticação.
- Comparar a busca por palavra-chave com busca semântica no módulo 03 da trilha avançada.

## Changelog

- `0.2.0` — implementação: 3 tools, 7 resources, 2 prompts, testes e CI.
- `0.1.0` — especificação.
