---
tipo: guide
maturidade: tested
versao: 0.1.0
autores: [time]
criado_em: 2026-05-28
atualizado_em: 2026-11-12
---

# Glossário

Linguagem comum do time. Quando alguém usa um termo aqui, ele significa exatamente isso. Se você quer adicionar um termo, abra PR.

## Modelos e geração

**LLM (Large Language Model).** Modelo de linguagem treinado em larga escala que recebe tokens e produz tokens.

**Token.** Unidade básica de processamento de um LLM. Aproximadamente 0,75 palavras em português. Toda chamada tem custo e limite em tokens.

**Janela de contexto.** Quantidade máxima de tokens (entrada + saída) que o modelo aceita em uma chamada.

**Temperatura.** Parâmetro que controla a aleatoriedade da geração. 0 = determinístico, 1+ = criativo.

**Top-p / nucleus sampling.** Estratégia alternativa à temperatura para controlar diversidade.

**Alucinação.** Quando o modelo gera informação plausível mas falsa, sem indicar incerteza.

## Prompts

**System prompt.** Instrução de mais alto nível, define identidade, regras e formato.

**User prompt.** Mensagem do usuário final, contém a tarefa específica.

**Developer instructions.** Diretrizes técnicas dadas pelo desenvolvedor, geralmente concatenadas ao system prompt.

**Few-shot prompting.** Incluir exemplos de input/output no prompt para guiar o modelo.

**Zero-shot prompting.** Pedir a tarefa sem exemplos, confiando na capacidade do modelo.

**Chain-of-thought (CoT).** Pedir explicitamente que o modelo pense passo a passo antes de responder.

**Output schema.** Especificação do formato esperado da resposta (JSON, tabela, markdown).

**Prompt injection.** Ataque onde input do usuário tenta sobrescrever instruções do sistema.

## Agentes

**Agente.** Sistema onde um LLM toma decisões iterativas sobre quais ações executar.

**Tool / Tool call.** Função que o agente pode invocar para interagir com o mundo (ler arquivo, buscar na web, escrever no banco).

**Tool use loop.** Ciclo de pensar → escolher tool → executar → observar resultado → repetir.

**Human-in-the-loop (HITL).** Padrão onde ações sensíveis exigem confirmação humana antes de executar.

## RAG

**RAG (Retrieval-Augmented Generation).** Padrão onde se recupera contexto relevante de uma base externa e injeta no prompt antes de gerar.

**Embedding.** Representação vetorial de um pedaço de texto, usada para busca semântica.

**Vector store.** Banco de dados otimizado para busca por similaridade de embeddings.

**Chunking.** Quebrar documentos em pedaços menores para indexação e recuperação.

## Skills

**Skill.** Pasta com `SKILL.md` e recursos auxiliares que um agente carrega dinamicamente quando o contexto exige aquela competência.

**Progressive disclosure.** Princípio de manter o `SKILL.md` enxuto e mover detalhes para arquivos referenciados, carregados apenas quando necessário.

**SKILL.md.** Arquivo principal de uma skill, com front-matter (`name`, `description`) e instruções operacionais.

## MCP

**MCP (Model Context Protocol).** Protocolo aberto para conectar aplicações de LLM a fontes de dados e ferramentas externas.

**MCP client.** Aplicação que consome um servidor MCP (ex.: Claude Desktop, Cursor, IDEs).

**MCP server.** Programa que expõe tools, resources e prompts para clientes MCP.

**Tool (no MCP).** Ação que o modelo pode chamar via servidor (consultar API, escrever arquivo, executar query).

**Resource (no MCP).** Dado que o servidor expõe ao modelo (arquivos, schemas, contexto estático).

**Prompt (no MCP).** Template parametrizável que o servidor oferece ao cliente.

## Avaliação

**Eval.** Procedimento que mede a qualidade de uma resposta segundo critérios definidos.

**Scorecard.** Tabela de critérios com peso e nota, usada para avaliar artefatos.

**Golden set.** Conjunto curado de casos com respostas esperadas, usado como referência.

**Reprodutibilidade.** Capacidade de obter resultados consistentes ao repetir o mesmo experimento.

## Segurança

**Prompt injection.** Ver acima.

**Data exfiltration.** Risco de o modelo vazar dados sensíveis presentes no contexto.

**Tool misuse.** Risco de o agente usar uma tool de forma indevida (deletar arquivo errado, gastar crédito, etc.).

**Confused deputy.** Ataque onde o agente é manipulado para executar ação em nome de outro.

## Padrões e arquitetura

**Workflow.** Sequência de passos definida no código, em que o LLM executa partes mas não decide o caminho.

**Orchestrator-workers.** Um modelo divide a tarefa e distribui partes para outros, depois junta os resultados.

**Evaluator-optimizer.** Um modelo gera, outro avalia, e o ciclo repete até passar no critério.

**Structured output.** Saída do modelo forçada a seguir um schema (ex.: JSON Schema).

**Agente de código.** Assistente que lê, escreve e executa código num repositório, com revisão humana.

## Recuperação

**Busca híbrida.** Combinação de busca lexical (ex.: BM25) com busca por embeddings.

**Reranker.** Modelo que reordena os resultados de uma busca pela relevância para a pergunta.

**RRF (Reciprocal Rank Fusion).** Forma simples de juntar vários rankings somando 1/(k + posição) de cada um.

**GraphRAG.** RAG que organiza o conhecimento como grafo de entidades e relações.

## Avaliação e operação

**LLM como juiz.** Uso de um modelo para avaliar respostas de outro. Precisa ser calibrado contra avaliação humana.

**Red teaming.** Busca deliberada de entradas que fazem o sistema falhar ou se comportar mal.

**pass@k.** Probabilidade de pelo menos uma de k tentativas passar nos testes.

**Tracing.** Registro de cada chamada de modelo e de ferramenta de uma execução, para investigar o que aconteceu.

**Prompt caching.** Reaproveitamento de prefixos de prompt já processados para reduzir custo e latência.

## Segurança

**Prompt injection indireta.** Instrução maliciosa escondida em conteúdo que o agente lê (página, e-mail, documento).

**Menor privilégio.** O agente recebe só as permissões mínimas para a tarefa.

**Sandbox.** Ambiente isolado onde o agente executa código sem acesso ao sistema real.

## Modelos

**Quantização.** Redução da precisão numérica dos pesos para o modelo caber em menos memória.

**LoRA.** Técnica de fine-tuning que treina poucas matrizes adicionais em vez do modelo inteiro.

**Destilação.** Treinar um modelo pequeno para imitar um grande.

## Processo interno

**Artefato.** Qualquer entrega catalogada no repo com front-matter (prompt, skill, MCP, eval, case, ADR).

**ADR (Architectural Decision Record).** Documento curto que registra uma decisão técnica e seu contexto.

**MVP.** Mínimo conjunto de entregáveis que valida uma hipótese.
