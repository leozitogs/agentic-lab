# Tests — research-synthesis

## Casos que DEVEM disparar a skill

| # | Input | Comportamento esperado | Status |
|---|-------|------------------------|--------|
| 1 | 3 papers + pergunta de pesquisa | skill carrega, gera síntese com 5 seções | ok |
| 2 | 2 blog posts contraditórios | skill carrega, marca disagreement explicitamente | ok |
| 3 | 4 docs internos + "compare abordagens" | skill carrega, agrupa por tema | ok |

## Casos que NÃO devem disparar a skill

| # | Input | Comportamento esperado | Status |
|---|-------|------------------------|--------|
| 1 | 1 paper sozinho | skill NÃO carrega, modelo resume | ok |
| 2 | "Me ajude a escrever um conto" | skill NÃO carrega | ok |
| 3 | "Qual a capital do Brasil?" | skill NÃO carrega | ok |

## Casos de borda

| # | Input | Comportamento esperado | Status |
|---|-------|------------------------|--------|
| 1 | 2 fontes que dizem coisas opostas sobre mesmo dado | disagreement marcado como "alta importância" | ok |
| 2 | 5 fontes que dizem exatamente a mesma coisa | gaps section deve listar "nenhum disagreement encontrado, considere ampliar fontes" | tentar |
| 3 | Fontes em idiomas diferentes (PT + EN) | síntese em PT, citações no idioma original | ok |
