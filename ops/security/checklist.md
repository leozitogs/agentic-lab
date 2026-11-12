---
tipo: guide
maturidade: tested
versao: 0.2.0
autores: [time]
criado_em: 2026-05-28
atualizado_em: 2026-11-12
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

## Agentes com ferramentas e conteúdo externo

Itens que saíram do [kit de prompt injection](../../build/evaluations/prompt-injection/README.md) do módulo 07. Os números e o porquê de cada um estão na [ADR-0004](../decisions/ADR-0004-mitigacoes-prompt-injection.md).

- [ ] Modelo de ameaça escrito: quais ferramentas leem conteúdo de terceiros (e-mail, web, documentos, resultados de busca) e quais têm efeito fora do contexto (enviar, publicar, pagar, apagar, escrever arquivo).
- [ ] Menor privilégio: cada tarefa recebe só as ferramentas de que precisa; tarefa de leitura não tem ferramenta de envio.
- [ ] Ação irreversível (enviar, publicar, apagar, pagar) passa por confirmação humana, com destinatário e conteúdo visíveis para quem aprova. Destinatário fora do pedido é negado por padrão.
- [ ] Filtro de saída: URLs, links e imagens markdown para domínios fora de uma lista permitida são removidos da resposta e do que o agente envia (canal clássico de exfiltração).
- [ ] Conteúdo externo chega ao modelo marcado (spotlighting/datamarking ou delimitação explícita), com instrução de sistema dizendo que é dado, não instrução. Tratar como camada de redução, não como barreira.
- [ ] Onde der, plan-then-execute (dual LLM): o plano e os destinatários são decididos antes de ler conteúdo externo, e o conteúdo só passa por um modelo sem ferramentas.
- [ ] Segredos fora do contexto do modelo. Se não der, o segredo é canário nos testes: o teste falha se ele aparecer em e-mail enviado ou URL.
- [ ] Suíte de injeção indireta rodando contra o agente (ASR e utilidade, com e sem ataque), cobrindo pelo menos: instrução no corpo, comentário HTML, assinatura, anexo, urgência falsa e mensagem falsa do sistema.
- [ ] Log de toda chamada de ferramenta, inclusive as negadas: tentativa barrada é sinal de ataque e precisa aparecer no monitoramento.
- [ ] Mitigação de sistema (aprovação, filtro, isolamento) tem teste com um modelo falso que obedece às injeções: a defesa precisa barrar o ataque mesmo quando o modelo falha.

## Geral

- [ ] LGPD: nenhum dado pessoal de terceiros sem base legal.
- [ ] Sem segredos no histórico do git (verificar com `gitleaks` ou similar).
- [ ] Dependências revisadas.
- [ ] Caso de incidente documentado e resolução registrada em ADR.
