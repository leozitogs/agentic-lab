# Segurança

Esta pasta concentra **análises de risco, checklists e padrões defensivos** aplicados a prompts, skills e MCPs do repo.

## O que mora aqui

- `checklist.md` — checklist obrigatório antes de promover qualquer artefato.
- `<nome-do-artefato>.md` — análise de risco de artefatos específicos (ex.: `repo-knowledge-mcp.md`).

## Quando criar um documento aqui

- MCP server que escreve em qualquer sistema → obrigatório.
- Skill que executa código ou consome conteúdo externo → obrigatório.
- Prompt usado em automação não supervisionada → obrigatório.
- Prompt experimental, skill manual → opcional, mas recomendado.

## Modelo de ameaça simplificado

Para cada artefato, responder:

1. **Quem ataca?** Usuário malicioso? Documento envenenado? Tool comprometida?
2. **O que ataca?** Prompt injection? Exfiltração de dado? Uso indevido de tool?
3. **O que perde?** Dado sensível? Crédito de API? Integridade de arquivos?
4. **Como detectamos?** Logs, alertas, revisão humana?
5. **Como contemos?** Dry-run, allowlist, HITL, kill switch?
