---
tipo: guide
maturidade: tested
versao: 0.1.0
autores: [time]
criado_em: 2026-05-28
atualizado_em: 2026-05-28
---

# Checklist de segurança

Aplicar **antes** de promover qualquer artefato para `maturidade: reviewed` ou `adopted`.

## Prompts

- [ ] Não pede ao modelo para ignorar instruções anteriores ou seguir input do usuário literalmente.
- [ ] Define explicitamente o que NÃO fazer (refusal handling).
- [ ] Não expõe dados sensíveis no próprio prompt (chaves, dados pessoais).
- [ ] Sanitiza ou delimita claramente input do usuário (ex.: dentro de tags ou code blocks).
- [ ] Testado com input adversarial (prompt injection direta).
- [ ] Se aceita conteúdo externo (docs, URLs), testado com prompt injection indireta.

## Skills

- [ ] `description` específica o suficiente para não disparar em contextos inseguros.
- [ ] Não executa código vindo de input do usuário sem sandboxing.
- [ ] Recursos auxiliares (arquivos, scripts) revisados.
- [ ] Sem credenciais hardcoded.
- [ ] Testes incluem casos onde a skill **não deve** ser invocada.

## MCP servers

- [ ] Schemas JSON estritos em toda tool.
- [ ] Tools destrutivas exigem confirmação explícita (HITL).
- [ ] Dry-run disponível para toda escrita.
- [ ] Logs estruturados de toda invocação (em stderr, nunca no canal MCP).
- [ ] Sem path traversal: paths são validados contra raiz permitida.
- [ ] Credenciais via variáveis de ambiente, nunca em código ou config commitado.
- [ ] Rate limiting por sessão.
- [ ] Tratamento de erro em toda tool (sem crash do servidor).
- [ ] Documentação lista todas as tools e seu risco.

## Geral

- [ ] LGPD: nenhum dado pessoal de terceiros sem base legal.
- [ ] Sem segredos no histórico do git (verificar com `gitleaks` ou similar).
- [ ] Dependências revisadas.
- [ ] Caso de incidente documentado e resolução registrada em ADR.
