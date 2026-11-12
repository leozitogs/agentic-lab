---
tipo: adr
maturidade: tested
versao: 0.1.0
autores: [leozitogs]
criado_em: 2026-11-12
atualizado_em: 2026-11-12
status: aceito
---

# ADR-0004 · Mitigações padrão contra prompt injection em agentes com ferramentas

## Status

Aceito.

## Contexto

O módulo 07 da trilha avançada pede um agente de exemplo com e-mail fictício, atacado por injeção indireta antes e depois de mitigações. O [kit de prompt injection](../../build/evaluations/prompt-injection/README.md) fez isso: um agente com laço de tool-calling próprio e quatro ferramentas (`list_emails`, `read_email`, `search_contacts`, `send_email` simulado), uma caixa fictícia com um código de recuperação como canário, 4 tarefas legítimas e 6 injeções (instrução no corpo, comentário HTML, assinatura falsa, anexo, urgência falsa, mensagem falsa do sistema). As medidas seguem o AgentDojo: ASR (o objetivo do atacante aconteceu?) e utilidade (a tarefa foi cumprida?), com critérios determinísticos.

Quatro mitigações da literatura, isoladas e combinadas:

- **Spotlighting (datamarking)**, Hines et al. (2024): o conteúdo de terceiros chega marcado e o prompt diz que é dado.
- **Menor privilégio + aprovação humana** (OWASP LLM06, Excessive Agency): tarefa de leitura não recebe `send_email`; todo envio passa por uma política de aprovação simulada que só aceita os destinatários da tarefa.
- **Filtro de saída** (OWASP LLM05, Improper Output Handling): URLs e imagens markdown para domínios fora da lista permitida saem da resposta e dos e-mails.
- **Dual LLM / plan-then-execute** (Willison, 2023; CaMeL, Debenedetti et al., 2025, simplificado): o planejador não vê o conteúdo; um extrator sem ferramentas lê.

Resultado da rodada de 2026-11-12 com `ahc-qwen3:4b-instruct-8k` no Ollama, 48 execuções com ataque e 8 sem ataque por configuração ([relatório completo](../../build/evaluations/prompt-injection/results/report.md)):

| Configuração | ASR | IC 95% | tentativa | utilidade sob ataque | utilidade sem ataque | chamadas ao modelo | tokens |
|---|---:|---|---:|---:|---:|---:|---:|
| baseline | 0.23 | 0.08 a 0.40 | 0.23 | 0.90 | 0.75 | 3.4 | 3405 |
| spotlighting | 0.04 | 0.00 a 0.10 | 0.04 | 0.96 | 0.88 | 3.7 | 4217 |
| menor privilégio + aprovação | 0.29 | 0.12 a 0.46 | 0.29 | 0.96 | 1.00 | 4.6 | 5173 |
| filtro de saída | 0.00 | 0.00 a 0.14 | 0.25 | 0.90 | 0.75 | 3.5 | 3545 |
| dual LLM | 0.08 | 0.00 a 0.19 | 0.08 | 0.96 | 1.00 | 2.0 | 1256 |
| combinada | 0.00 | 0.00 a 0.14 | 0.00 | 0.85 | 1.00 | 2.0 | 1416 |

Três fatos da rodada pesam na decisão:

1. **Todo o ASR veio da resposta, nenhum de ferramenta.** Os quatro ataques que pediam uma ação (A1, A2, A4, A5) não pegaram em nenhuma configuração, nem como tentativa. Os que pegaram foram o link de phishing na assinatura (A3: 0.62 na linha de base) e a imagem markdown com o código na URL (A6: 0.75). Isto é deste modelo: um modelo que obedeça a pedidos de envio inverte o quadro, e os testes com um modelo falso que obedece a tudo mostram que só a aprovação e o dual LLM barram esse canal.
2. **Defesas de sistema e de modelo cobrem canais diferentes.** O filtro zerou o ASR com o modelo ainda sequestrado em 25% dos casos (tentativa de 0.25, contra 0.23 na linha de base). O spotlighting reduziu tanto o sucesso quanto a tentativa (0.23 para 0.04), sem perder utilidade, mas não zerou: os 2 casos restantes foram links copiados para a resposta e para um e-mail legítimo. O dual LLM protegeu o fluxo de controle por construção e deixou passar 4 casos pelo fluxo de dados (o extrator copiou o link de A3 para a resposta).
3. **Mudar ferramentas muda o que o agente lê.** Sem `send_email`, o agente passou a abrir todos os e-mails para resumir, e com isso leu a injeção que na linha de base ignorava: por isso menor privilégio + aprovação ficou com ASR acima da linha de base. A mitigação não piora as ações; ela simplesmente não protege o canal da resposta.

## Decisão

Todo agente do laboratório que lê conteúdo de terceiros e tem pelo menos uma ferramenta com efeito fora do contexto adota, por padrão, **as três camadas abaixo juntas**:

1. **Filtro de saída com lista permitida de domínios**, aplicado à resposta final e a tudo o que o agente envia ou publica (links, imagens markdown, URLs soltas). É a mitigação que mais reduziu o ASR medido (0.23 para 0.00), é determinística, custa quase nada e não mexeu na utilidade.
2. **Menor privilégio e aprovação humana para ação irreversível.** Cada tarefa recebe só as ferramentas de que precisa; enviar, publicar, apagar ou pagar passa por confirmação, com destinatário fora do pedido negado por padrão. Nesta rodada ela não reduziu o ASR, porque o modelo nunca tentou uma ação maliciosa; fica como obrigatória porque é a única barreira determinística para o canal das ferramentas (provada nos testes contra o modelo que obedece às injeções) e porque é o que o OWASP recomenda para excesso de agência.
3. **Spotlighting (datamarking) em todo conteúdo externo.** Reduziu o ASR de 0.23 para 0.04 e a tentativa na mesma proporção, sem custo de utilidade (sem ataque, 0.88 contra 0.75 da linha de base) e com cerca de 24% a mais de tokens. É camada de redução, não barreira: nunca é a única defesa de um canal.

Para agentes de **alto risco** (ação irreversível com consequência real, ou dados sensíveis no contexto) cuja tarefa cabe num plano decidido antes de ler o conteúdo, o padrão passa a ser **plan-then-execute (dual LLM) com as três camadas**, que é a configuração combinada medida: ASR 0.00, tentativa 0.00, utilidade sem ataque 1.00, com menos chamadas ao modelo que a linha de base (2.0 contra 3.4 por caso).

Fica valendo também: **segredo não entra no contexto do modelo.** Quando entra (como o canário aqui), qualquer suíte de testes do agente checa se ele aparece em URL ou em mensagem enviada.

## Consequências

### Positivas

- Cada canal de exfiltração medido (ferramenta de envio, link e imagem na resposta, link num e-mail legítimo) tem pelo menos uma defesa determinística no padrão.
- O kit fica como régua: qualquer agente novo, modelo novo ou guardrail novo roda no mesmo conjunto e é comparado com estes números.
- A distinção entre tentativa e sucesso vira prática: tentativa barrada é registrada e serve de sinal de ataque.

### Negativas

- O filtro de saída limita respostas legítimas com links externos; a lista permitida precisa ser mantida.
- A aprovação humana custa atenção de quem aprova e sofre de fadiga; a política simulada aqui é um teto, não uma previsão.
- O dual LLM restringe o agente a uma linguagem de plano e custa engenharia por domínio. Na rodada, a versão combinada omitiu o e-mail contaminado do resumo de T1 (utilidade de T1 sob ataque 0.42): parte da segurança veio de descartar conteúdo, o que é custo de utilidade.

### Neutras

- Os números valem para um modelo de 4B parâmetros, ataques escritos à mão e não adaptativos, e um conjunto sintético pequeno. Um modelo maior, que obedeça a pedidos de ação, ou um atacante adaptativo pedem nova rodada antes de reaproveitar a ordem das mitigações; a decisão por camadas não depende dessa ordem.
- A combinação das três camadas sem o dual LLM não foi medida como conjunto; a expectativa vem dos resultados por canal e precisa ser confirmada numa próxima rodada.
- A maturidade fica em `tested`: falta revisão de outra pessoa, um segundo modelo e a comparação com guardrails prontos (NeMo Guardrails, Llama Guard) que o módulo pede.

## Alternativas consideradas

| Alternativa | Por que não como padrão |
|-------------|-------------|
| Só spotlighting | Barato e eficaz neste modelo (0.04), mas depende de o modelo respeitar o aviso: contra o modelo falso que obedece a tudo, não barra nada. Não pode ser a única defesa de um canal. |
| Só menor privilégio + aprovação | Não toca o canal da resposta, que foi o único explorado nesta rodada (ASR 0.29). |
| Só filtro de saída | Zerou o ASR desta rodada, mas só porque o modelo não tentou ações; não impede um envio malicioso nem o código em texto puro dentro de um e-mail. |
| Dual LLM sempre | Melhor proteção estrutural, mas nem toda tarefa cabe num plano fixo e a versão simplificada deixa passar injeção pelo fluxo de dados (ASR 0.08 sozinho). Fica como padrão só para alto risco. |
| Classificador de injeção na entrada (guardrail pronto) | Não medido nesta rodada; é o próximo experimento do kit. |

## Referências

- [Kit de prompt injection](../../build/evaluations/prompt-injection/README.md) e [relatório da rodada](../../build/evaluations/prompt-injection/results/report.md).
- [Módulo 07 · Segurança de agentes](../../learn/avancado/07-seguranca-de-agentes.md) e [checklist de segurança](../security/checklist.md).
- OWASP, "Top 10 for LLM Applications" (2025): LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM05 Improper Output Handling, LLM06 Excessive Agency.
- Greshake et al., "Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection" (2023).
- Hines et al., "Defending Against Indirect Prompt Injection Attacks With Spotlighting" (2024).
- Debenedetti et al., "AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents" (2024).
- Debenedetti et al., "Defeating Prompt Injections by Design" (CaMeL, 2025).
- Simon Willison, "The Dual LLM pattern for building AI assistants that can resist prompt injection" (2023).
