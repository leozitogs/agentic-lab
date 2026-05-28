# Tests — MCP server

## Smoke tests

| # | Cenário | Esperado | Status |
|---|---------|----------|--------|
| 1 | Servidor inicia sem erro | exit 0, logs OK | |
| 2 | Cliente lista tools | retorna lista completa | |
| 3 | Cliente lista resources | retorna lista completa | |
| 4 | Cliente lista prompts | retorna lista completa | |

## Tool tests

| # | Tool | Input | Esperado | Status |
|---|------|-------|----------|--------|
| 1 | `example_tool` | input válido | output esperado | |
| 2 | `example_tool` | input inválido | erro tratado, sem crash | |

## Resource tests

| # | Resource | Esperado | Status |
|---|----------|----------|--------|
| 1 | `example_resource` | retorna conteúdo correto | |

## Segurança

| # | Cenário | Esperado | Status |
|---|---------|----------|--------|
| 1 | Tool destrutiva sem confirmação | rejeitada | |
| 2 | Input com prompt injection | sanitizado ou rejeitado | |
| 3 | Rate limit excedido | bloqueio com mensagem clara | |
