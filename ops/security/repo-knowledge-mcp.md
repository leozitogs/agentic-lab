---
tipo: guide
maturidade: tested
versao: 0.1.0
autores: [leozitogs]
criado_em: 2026-11-12
atualizado_em: 2026-11-12
---

# Análise de segurança · repo-knowledge MCP

## Superfície

| Primitiva | Exposição | Pode alterar algo? |
|---|---|---|
| Tools `search_artifacts`, `get_artifact`, `list_by_tag` | Conteúdo `.md` do repositório | Não |
| Resources de índice e `repo://artifact/{+path}` | Conteúdo `.md` do repositório | Não |
| Prompts | Texto fixo com o argumento do usuário | Não |

## Ameaças e mitigação

| Ameaça | Mitigação | Teste |
|---|---|---|
| Path traversal (`../`, absoluto, `C:/`) | `Catalog.safe_path` recusa; o SDK também rejeita traversal em resources | `test_read_blocks_unsafe_paths`, `test_traversal_is_refused` |
| Leitura de segredos (`.env`, chaves, `.git/`) | Só `.md`; pastas ocultas recusadas; só pastas expostas | `test_read_blocks_unsafe_paths` |
| Arquivo gigante travando o cliente | Limite de 200 KB por arquivo | — |
| Prompt injection dentro de um artefato | O servidor não executa nada e não tem tools de escrita; o pior caso é o modelo ler instrução maliciosa num `.md`. Revisão de PR continua sendo a barreira para o que entra no repo | — |
| Vazamento de stack trace | Falhas esperadas viram `ToolError` com mensagem curta | `test_traversal_is_refused` |
| Poluição do canal MCP por logs | Logs só em stderr | `test_stdio_roundtrip` |

## Checklist

- [x] Nenhuma tool de escrita ou destrutiva.
- [x] Tools anunciadas como somente leitura.
- [x] Caminhos validados no servidor, além do SDK.
- [x] Testes de segurança na CI.
- [ ] Revisão por outra pessoa.
