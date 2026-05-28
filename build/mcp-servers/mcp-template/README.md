---
tipo: mcp
maturidade: draft
versao: 0.1.0
autores: [seu-nome]
criado_em: YYYY-MM-DD
atualizado_em: YYYY-MM-DD
---

# Nome do MCP Server

## Objetivo

O que este servidor expõe e por quê.

## Tools, resources, prompts

| Primitiva | Nome | Descrição | Risco |
|-----------|------|-----------|-------|
| tool | `example_tool` | ... | leitura / escrita / destrutivo |
| resource | `example_resource` | ... | público / sensível |
| prompt | `example_prompt` | ... | — |

## Setup

```bash
# Instalação
pip install -e .  # ou npm install

# Variáveis de ambiente
export API_KEY=...
export LOG_LEVEL=info

# Rodar local
python -m server  # ou node dist/server.js
```

## Integração com clientes

### Claude Desktop

Adicione ao `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "nome-do-server": {
      "command": "python",
      "args": ["-m", "server"],
      "env": {
        "API_KEY": "..."
      }
    }
  }
}
```

### Cursor / VS Code

Instruções específicas.

## Segurança

- [ ] Tools destrutivas exigem confirmação explícita.
- [ ] Dry-run disponível para todas as escritas.
- [ ] Logs estruturados de toda invocação.
- [ ] Schema de input com validação estrita.
- [ ] Rate limiting por sessão.

Análise de risco completa em `ops/security/<nome>.md`.

## Troubleshooting

| Sintoma | Causa provável | Solução |
|---------|----------------|---------|
| ... | ... | ... |

## Testes

Casos manuais em `tests.md`.

## Changelog

- `0.1.0` — versão inicial.
