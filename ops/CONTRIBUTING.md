# Como contribuir

Você pode contribuir com vivências de uso de IA, conhecimento de sua área, perguntas, escuta, documentação, revisão, pesquisa e código. Design, pedagogia, administração e qualquer outra área têm espaço no laboratório. A [matriz de contribuições e escuta ativa](MATRIZ-DE-CONTRIBUICOES.md) define modalidades, critérios de revisão e apoio para participar.

## Comece no formato que funciona para você

Conte o contexto e o que gostaria de compartilhar ou compreender em uma [issue](https://github.com/leozitogs/agentic-lab/issues/new/choose) ou pelo contato [agenticlab.playbook@gmail.com](mailto:agenticlab.playbook@gmail.com). O mantenedor pode combinar ajuda para organizar o relato e preparar os arquivos. A publicação de conteúdo recebido em privado depende da sua autorização e validação da síntese. Os prazos e o apoio são combinados conforme disponibilidade.

Você pode participar de uma conversa, revisar pela perspectiva de sua área ou trazer uma necessidade. A escolha de transformar isso em artefato é feita com você. Consulte o [processo de escuta ativa](MATRIZ-DE-CONTRIBUICOES.md#escuta-ativa-como-parte-do-trabalho).

## Escolha um caminho

| Quero participar com | Comece por | Entrega possível |
|---|---|---|
| Conhecimento de uma área | [Matriz de contribuições](MATRIZ-DE-CONTRIBUICOES.md) | Critérios, exemplos ou revisão de domínio |
| Escuta e facilitação | [Processo de escuta](MATRIZ-DE-CONTRIBUICOES.md#escuta-ativa-como-parte-do-trabalho) | Síntese validada e devolutiva |
| Uma dúvida ou tentativa | [Issue de vivência](https://github.com/leozitogs/agentic-lab/issues/new/choose) | Discussão e próximos passos |
| Uma experiência prática | [Template de relato](../learn/notes/EXPERIENCE-TEMPLATE.md) | Nota em `learn/notes/` com maturidade draft |
| Documentação ou tradução | Página que gerou dificuldade | PR pequeno explicando a melhoria |
| Reprodução ou revisão | README do artefato escolhido | Ambiente, comandos, resultado e diferenças observadas |
| Um novo artefato | [Roadmap](../ROADMAP.md) e templates abaixo | Proposta e PR com evidência |
| Código e infraestrutura | [Ambiente técnico](DEVELOPMENT.md) | Mudança focada e verificação reproduzível |

Veja [good first issue](https://github.com/leozitogs/agentic-lab/labels/good%20first%20issue) e [help wanted](https://github.com/leozitogs/agentic-lab/labels/help%20wanted). Se a lista estiver vazia, proponha uma tarefa ou use uma destas sugestões de entrada, que ainda precisam ser combinadas em issue.

- Compartilhar uma experiência de uso de IA em sua área, com o resultado e as dificuldades percebidas.
- Revisar um exemplo com critérios de design, educação, administração ou outra prática.
- Ajudar a acolher e organizar um relato com validação da pessoa que o trouxe.
- Reproduzir o núcleo offline em um ambiente diferente e relatar dificuldades.
- Revisar uma definição do glossário com fonte e exemplo.
- Reproduzir uma pergunta do kit de RAG e explicar um erro de recuperação.
- Compartilhar uma tentativa com agente de código, incluindo resultado negativo e condições de reprodução.

## Para contribuir por PR

1. Leia o [código de conduta](../CODE_OF_CONDUCT.md) e escolha um escopo pequeno. Correções simples podem ir direto para PR. Para mudanças maiores, abra proposta para discutir objetivo e critério de conclusão.
2. Faça um fork pelo GitHub se você não tem acesso de escrita. Clone seu fork e adicione o original como upstream. Quem tem escrita pode clonar o original e trabalhar em uma branch.
3. Crie uma branch a partir da main atualizada. Use `tipo/descricao-curta`, por exemplo `docs/primeiro-relato` ou `eval/novo-caso`.
4. Construa a contribuição. Use PR em rascunho para receber orientação cedo. Declare dúvidas, limites e verificações ainda pendentes.
5. Execute `python scripts/check.py` para mudanças técnicas. Para conteúdo, revise a clareza, as fontes e os metadados. A CI também verifica o núcleo automaticamente.
6. Abra PR para `leozitogs/agentic-lab:main`, preencha o template e vincule a issue quando existir. Solicite revisão e responda às observações.
7. Após integração, registre aprendizados e referências cruzadas quando houver novo conhecimento. A participação ocorre de forma assíncrona.

```bash
# Após criar seu fork, substitua SEU-USUARIO.
git clone https://github.com/SEU-USUARIO/agentic-lab.git
cd agentic-lab
git remote add upstream https://github.com/leozitogs/agentic-lab.git
git fetch upstream
git switch -c docs/primeiro-relato upstream/main
python scripts/check.py
git add learn/notes/seu-relato.md
git commit -m "docs: registrar experiência reproduzível"
git push -u origin docs/primeiro-relato
```

No PowerShell ou no terminal Linux/macOS, esses comandos Git têm a mesma forma. Configure nome e e-mail do Git conforme a autoria desejada, usando o endereço privado do GitHub se preferir. O arquivo do exemplo precisa ser criado antes de `git add`.

## As seis perguntas

Uma contribuição deve ajudar a responder o que aprendemos, como reproduzir, quando usar, quando as condições deixam de valer, como avaliar e como melhorar. O template de PR oferece essas perguntas. Correções pequenas podem reuni-las em uma explicação curta. Incertezas e resultados negativos podem ser registrados com maturidade `draft`. Quem revisa ajuda a completar contexto e critérios.

## Tipos de contribuição

| Tipo | Pasta | Template |
|---|---|---|
| Prompt | `build/prompts/` | [Prompt](../build/prompts/PROMPT-TEMPLATE.md) |
| Skill | `build/skills/` | [Skill](../build/skills/skill-template/SKILL.md) |
| MCP server | `build/mcp-servers/` | [MCP](../build/mcp-servers/mcp-template/README.md) |
| Avaliação | `build/evaluations/` | [Eval](../build/evaluations/EVAL-TEMPLATE.md) |
| Caso de uso | `cases/` | [Caso](../cases/CASE-TEMPLATE.md) |
| Vivência e nota | `learn/notes/` | [Relato](../learn/notes/EXPERIENCE-TEMPLATE.md) |
| Decisão técnica | `ops/decisions/` | [ADR](decisions/ADR-TEMPLATE.md) |

## Critérios de revisão

| Contribuição | Evidência esperada |
|---|---|
| Correção de conteúdo | Explicação da mudança, fontes quando aplicável e leitura dos links |
| Relato de experiência | Contexto, processo em linguagem cotidiana, observações e limites, mesmo em draft |
| Revisão de domínio | Critérios da área, exemplos e alcance da interpretação |
| Escuta e facilitação | Síntese validada, consentimento e devolutiva combinada |
| Código | Comportamento esperado, verificações relevantes e tratamento de falhas |
| Prompt ou skill | Exemplo e avaliação inicial compatível com a maturidade |
| MCP | Interfaces, testes e análise de permissões e segurança |
| Experimento | Dados, versões, critérios, comandos e resultados rastreáveis |

Revise comportamento existente e compatibilidade. Use dados públicos ou sintéticos e materiais que você tenha direito de compartilhar. Relatos profissionais devem remover identificadores e respeitar consentimento. Segredos e vulnerabilidades seguem [SECURITY.md](../SECURITY.md).

## Convenções e maturidade

Commits usam prefixos como `feat:`, `fix:`, `docs:`, `eval:`, `skill:`, `mcp:`, `prompt:` e `refactor:`. Mensagens podem ser em português ou inglês, com consistência dentro da contribuição. Pastas e arquivos usam kebab-case, preservando os nomes convencionais existentes.

Documentação humana fica em PT-BR. Prompts e instruções operacionais consumidos por agentes ficam em inglês conforme a convenção do laboratório. Relatos e perguntas podem ser apresentados no idioma em que a pessoa consegue participar; a revisão ajuda a incorporar o conteúdo ao padrão do repositório.

Artefatos em learn, build, cases e decisões usam o front-matter de [TAGS.md](TAGS.md). `draft` indica trabalho em construção. `tested` exige evidência registrada pelo autor. `reviewed` exige revisão de outra pessoa. `adopted` indica padrão aceito pelo time. Preserve autores, fontes e limites ao evoluir um artefato.

O [modelo de governança](GOVERNANCE.md) descreve quem decide, como novos mantenedores entram e como integrar contribuições enquanto o laboratório tem um único mantenedor. Assistência de IA relevante para código, resultados ou conclusões deve ser descrita junto de sua validação.
