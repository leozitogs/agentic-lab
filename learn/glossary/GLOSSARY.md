---
tipo: guide
maturidade: tested
versao: 0.1.0
autores: [time]
criado_em: 2026-05-28
atualizado_em: 2026-05-28
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

## Processo interno

**Artefato.** Qualquer entrega catalogada no repo com front-matter (prompt, skill, MCP, eval, case, ADR).

**ADR (Architectural Decision Record).** Documento curto que registra uma decisão técnica e seu contexto.

**MVP.** Mínimo conjunto de entregáveis que valida uma hipótese.
