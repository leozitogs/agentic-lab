# Ambiente técnico

## Comece com o núcleo offline

Use Git e Python 3.10 ou superior. A CI verifica o núcleo em Python 3.12, Linux e Windows. Ele utiliza a biblioteca padrão e dispensa chave de API.

```bash
git clone https://github.com/leozitogs/agentic-lab.git
cd agentic-lab
python scripts/check.py
```

No Windows, `py -3` pode substituir `python`. Se o comando não existir, instale Python e Git, reabra o terminal e confira `python --version` e `git --version`. A saída de cada etapa mostra o diretório e o comando executado.

O comando valida metadados e executa os testes da raiz, RAG e prompt injection. Os testes densos do RAG são pulados quando Chroma está ausente. O núcleo offline verifica a implementação e seus exemplos sintéticos. Resultados de modelos reais exigem os procedimentos de cada kit.

## Componentes opcionais

Use um ambiente virtual antes de instalar dependências. Em Linux/macOS, ative `.venv/bin/activate`. No PowerShell, ative `.venv\Scripts\Activate.ps1` conforme a política local de execução. Também é possível chamar diretamente o Python da pasta do ambiente.

```bash
python -m venv .venv
# Após ativar o ambiente, escolha o componente necessário.
python -m pip install -r site/requirements.txt
python scripts/check.py --site

python -m pip install ./build/mcp-servers/repo-knowledge
python scripts/check.py --mcp
```

Para RAG denso, instale `build/evaluations/rag-recuperacao/requirements.txt` e siga o [README do kit](../build/evaluations/rag-recuperacao/README.md). Instalações e downloads de modelos precisam de rede e espaço local. O [eval de research-analyst](../build/evaluations/research-analyst/README.md) documenta promptfoo e a chave de API opcional. O [kit de segurança](../build/evaluations/prompt-injection/README.md) documenta Ollama, modelo e auditoria.

## Mapa de engenharia

| Área | Entrada | Verificação |
|---|---|---|
| Metadados dos artefatos | `ops/TAGS.md` | `scripts/validate_frontmatter.py` |
| Preparação do site | `scripts/build_site.py`, `mkdocs.yml` | `python scripts/check.py --site` |
| MCP somente leitura | `build/mcp-servers/repo-knowledge/` | `python scripts/check.py --mcp` |
| Avaliações | `build/evaluations/` | Testes offline e execução de modelo por kit |
| Integração contínua | `.github/workflows/` | `lab-check` em todo PR e push na main |

Uma mudança de código deve preservar interfaces e dados existentes, tratar falhas e acrescentar teste quando houver uma regressão concreta. Mantenha os PRs focados, evite dependências sem necessidade e registre parâmetros, revisão dos dados e limitações dos experimentos. Segredos ficam em variáveis de ambiente e arquivos ignorados pelo Git.

O check `lab-check` é estável e sempre executa. Workflows especializados mantêm seus gatilhos e dependências. O build do site é verificado em modo estrito em PRs antes da publicação na main; avisos de links quebrados fazem a etapa falhar. Código de forks roda com permissões de leitura, sem depender de segredos.

## Práticas de engenharia aplicadas

| Base | Aplicação no laboratório |
|---|---|
| Requisitos e critérios de aceite | Problema e resultado esperado na issue e no PR |
| Gestão de configuração | Revisões Git, branches, ownership e proteção de integração |
| Projeto e evolução | Reuso de componentes existentes e ADR para decisões com impacto |
| Verificação e qualidade | Testes relevantes, CI offline e documentação compilada |
| Manutenção | Reprodução de falhas, regressões, reversões por PR e versões rastreáveis |
| Compartilhamento de conhecimento | Revisões explicadas, relatos e registro de resultados negativos |

O SWEBOK organiza requisitos, projeto, testes, gestão de configuração e qualidade como áreas de engenharia de software. A tabela traduz essas áreas em procedimentos observáveis do laboratório. [IEEE Computer Society, SWEBOK](https://www.computer.org/education/bodies-of-knowledge/software-engineering/topics)

O estudo de Bacchelli e Bird identificou transferência de conhecimento e desenvolvimento de soluções alternativas entre os benefícios da revisão de código. Por isso, a revisão no lab inclui explicar decisões e apoiar quem está chegando. [Expectations, Outcomes, and Challenges of Modern Code Review](https://www.microsoft.com/en-us/research/publication/expectations-outcomes-and-challenges-of-modern-code-review/)
