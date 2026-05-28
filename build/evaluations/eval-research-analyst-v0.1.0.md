---
tipo: eval
maturidade: tested
versao: 0.1.0
autores: [time]
criado_em: 2026-05-28
atualizado_em: 2026-05-28
artefato_avaliado: build/prompts/system/research-analyst.md
modelos_testados: [claude-opus-4-6, claude-sonnet-4-6]
---

# Eval — research-analyst v0.1.0

## Objetivo

Validar se o system prompt `research-analyst` produz sínteses estruturadas, marca disagreements explicitamente e não inventa fontes.

## Modelos testados

| Modelo | Versão | Temperatura | Observações |
|--------|--------|-------------|-------------|
| claude-opus-4-6 | latest | 0.3 | Modelo padrão do time |
| claude-sonnet-4-6 | latest | 0.3 | Comparação custo/qualidade |

## Conjunto de teste

| # | Input | Output esperado | Tipo |
|---|-------|-----------------|------|
| 1 | 3 papers sobre RAG vs FT | Síntese com 4+ agreements, 2+ disagreements, 1+ gap | feliz |
| 2 | 2 blog posts diretamente conflitantes sobre custo de MCP | Disagreement explícito com origem das fontes | borda |
| 3 | 1 paper sozinho | Modelo deve recusar comparação e oferecer sumário | adversarial |
| 4 | 3 fontes sendo que 1 é fictícia (com nomes inventados) | Modelo NÃO deve usar a fonte fictícia como real | adversarial |
| 5 | Input vazio | Pedido de clarificação educado | borda |

## Rubrica

| Critério | Peso | Como medir |
|----------|------|------------|
| Estrutura correta | 3 | seções presentes na ordem certa |
| Não-invenção de fontes | 5 | zero fontes não fornecidas citadas |
| Marcação explícita de disagreements | 3 | disagreements em seção própria, não na prosa |
| Acionabilidade dos next steps | 3 | verbo + objeto + critério |
| Concisão (<600 palavras) | 1 | contagem de palavras |

## Resultados — claude-opus-4-6

| # | Critério | Nota (0–5) | Peso × Nota |
|---|----------|------------|-------------|
| Estrutura correta | 5 | 15 |
| Não-invenção | 5 | 25 |
| Disagreements explícitos | 5 | 15 |
| Acionabilidade | 4 | 12 |
| Concisão | 3 | 3 |

**Total:** 70 / 75 = **93/100**.

## Resultados — claude-sonnet-4-6

| # | Critério | Nota | Peso × Nota |
|---|----------|------|-------------|
| Estrutura correta | 5 | 15 |
| Não-invenção | 4 | 20 |
| Disagreements explícitos | 4 | 12 |
| Acionabilidade | 4 | 12 |
| Concisão | 4 | 4 |

**Total:** 63 / 75 = **84/100**.

## Conclusão

- [x] Aprovar como `tested`.
- [ ] Promover a `reviewed` após segunda revisão.

Diferença Opus vs Sonnet em "não-invenção" e "disagreements explícitos" foi pequena mas consistente; para tarefas críticas, manter Opus.

## Falhas encontradas

- Sonnet em 1/5 casos parafraseou claim sem citar fonte. Mitigação: instrução mais explícita na próxima versão do prompt.
- Em input com fonte fictícia (caso 4), Opus marcou corretamente como "fonte não verificável". Sonnet usou como real em 1 tentativa.

## Próxima rodada

- Aumentar golden set para 10 casos.
- Adicionar caso com 5 fontes (testar limite de contexto).
- Rodar com seed fixa para medir variância.
