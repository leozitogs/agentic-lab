---
tipo: eval
maturidade: draft
versao: 0.1.0
autores: [seu-nome]
criado_em: YYYY-MM-DD
atualizado_em: YYYY-MM-DD
artefato_avaliado: <path>
modelos_testados: []
---

# Eval — <nome do artefato>

## Objetivo

O que esta avaliação responde.

## Artefato avaliado

Path relativo + versão.

## Modelos testados

| Modelo | Versão | Temperatura | Observações |
|--------|--------|-------------|-------------|
| ... | ... | ... | ... |

## Conjunto de teste (golden set)

| # | Input | Output esperado | Tipo | Notas |
|---|-------|-----------------|------|-------|
| 1 | ... | ... | feliz / borda / adversarial | ... |
| 2 | ... | ... | ... | ... |

## Rubrica

| Critério | Peso | Como medir |
|----------|------|------------|
| Clareza | 2 | 0–5, julgamento humano com guia |
| Precisão | 3 | 0–5, comparação com output esperado |
| Reprodutibilidade | 3 | mesmo input → mesmo output? |
| Segurança | 3 | nenhuma resposta perigosa |
| Utilidade prática | 4 | resolveria o problema real? |
| Facilidade de uso | 2 | esforço para usar |

## Resultados

| # | Critério | Nota | Peso × Nota | Observação |
|---|----------|------|-------------|------------|
| 1 | Clareza | 4 | 8 | ... |
| ... | ... | ... | ... | ... |

**Total ponderado:** _(soma)_ / _(soma de pesos × 5)_ × 100 = **XX/100**

## Conclusão

- [ ] Rejeitar
- [ ] Melhorar antes de adotar
- [ ] Aprovar como `tested`
- [ ] Promover a `reviewed` ou `adopted`

## Falhas encontradas

Listar e linkar para issue/PR de correção.

## Próxima rodada de avaliação

O que mudar no protocolo para a próxima medição.
