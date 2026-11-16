---
tipo: guide
maturidade: draft
versao: 0.1.0
autores: [leozitogs]
criado_em: 2026-11-15
atualizado_em: 2026-11-15
---

# Plano de engenharia para a próxima contribuição de segurança

Autoria de Leonardo Gonçalves Sobral. A contribuição inicial implementa a etapa 1. As etapas 2 e 3 dependem dessa infraestrutura e de novas execuções experimentais.

## Objetivo e hipótese

Permitir que uma conclusão de segurança seja rastreada até dados, código, parâmetros e respostas preservadas. Depois, investigar se as três camadas recomendadas pelo ADR-0004 preservam utilidade sob ataques adaptativos. A rodada histórica permanece identificada como evidência do experimento original.

## Etapa 1 — identidade experimental e auditoria

1. Calcular SHA-256 de JSON canônico de um manifesto versionado. Incluir hashes de run_eval.py e de todos os módulos pikit/*.py, dados completos carregados, definições das configurações, provedor, endpoint sem credenciais, modelo, temperatura, limite de chamadas, versão Python e identidade explícita do modelo. Registrar revisão Git como proveniência. A revisão não compõe o hash para permitir retomada após um commit que preserva os arquivos experimentais.
2. Acrescentar --model-revision para identificar um snapshot ou digest imutável. Com revisão informada, permitir retomada entre invocações. Sem revisão, isolar cada invocação por UUID e informar essa decisão. Um nome mutável de modelo sozinho não permite afirmar identidade.
3. Criar um diretório por identidade em .cache/prompt-injection/experiments/. Gravar manifesto e registros JSONL completos. Cada registro mantém configuração, tarefa, ataque e semente. Seleções de tarefas, configurações e quantidade de repetições podem reutilizar casos idênticos dentro da mesma identidade. --fresh cria uma execução isolada sem apagar arquivos anteriores. Caches legados ficam disponíveis para consulta e não entram na retomada nova.
4. Usar trava exclusiva por diretório antes de ler ou escrever. Uma segunda execução concorrente falha com mensagem acionável. Liberar a trava em finally. Trava remanescente após interrupção abrupta exige verificar que o processo terminou antes de removê-la manualmente.
5. Recuperar somente uma última linha JSONL incompleta, preservando o fragmento em arquivo separado antes de truncar. Corrupção em linha anterior falha explicitamente. Registros com erro ou limite de chamadas são repetidos na próxima invocação. Validar identidade e chaves ao carregar. A última tentativa válida por chave substitui as anteriores na agregação, inclusive se tiver erro.
6. Preservar resposta final, resposta crua, plano e logs completos antes de compactar a publicação. O resumo mantém compatibilidade com report.render. Publicar manifesto e runs.jsonl completos em results/experiments/<identidade>/, e incluir a referência no results.json. Gravar arquivos de saída por substituição atômica. Atualizações entre arquivos são rastreadas pela identidade, sem prometer transação multiarquivo. Serializar toda publicação e --report-only com uma trava global curta em results/. Pregerar os arquivos antes de publicar e identificar manifesto, JSON e relatório novo com a identidade e o identificador da publicação. Publicações interrompidas são detectáveis por divergência desses identificadores. O histórico existente continua legível por --report-only, com renderização idêntica.
7. Documentar comandos de execução e retomada, arquivos gerados e limites de reprodutibilidade. Provedores podem variar mesmo com parâmetros e revisão fixos. Credenciais e variáveis de segredo nunca entram no manifesto. Rejeitar endpoints com usuário, senha, query ou fragmento para evitar persistência de credenciais.

### Verificação da etapa 1

Testes offline com provedor falso pelo entry point main(), usando diretórios temporários. Cobrir primeira execução, retomada sem novas chamadas, resposta acima de 1.500 caracteres preservada integralmente, identidade alterada por dados/código/parâmetros/revisão, isolamento sem revisão, --fresh preservando histórico, relatório legado, erro repetido, corrupção no meio, cauda interrompida, exclusão concorrente e publicação entre identidades diferentes, incluindo concorrência com --report-only. Testar erro e limite de chamadas repetidos, cauda UTF-8 interrompida e rejeição de endpoints com credenciais. --model-revision é declaração do operador quando o provedor não confirma o snapshot. Rodar os testes do kit, testes da raiz, validador de front-matter e regeneração do relatório histórico com diff vazio. Resultado científico novo depende de executar modelos reais.

## Etapa 2 — configuração do ADR e controles

Adicionar a combinação spotlighting + menor privilégio/aprovação + filtro, sem dual LLM. Comparar baseline, essa combinação e combinação completa em tarefas pareadas. Acrescentar controles benignos com links necessários e conteúdo indispensável em resumos. Registrar ASR, tentativa, exposição, utilidade por tarefa, omissões, erros, tokens e latência. Uma nova rodada e sua análise devem preceder mudanças nas conclusões do ADR.

## Etapa 3 — avaliação adaptativa

Definir previamente ameaça, permissões do atacante, superfícies editáveis, informação de feedback e orçamento por caso. Separar tarefas de desenvolvimento e avaliação final, congelando defesa e critérios antes desta última. Usar dois modelos que consigam executar tarefas benignas. Registrar sucesso acumulado por orçamento e resultados por modelo e canal. Comparar casos pareados, agrupando repetições e variantes por tarefa/objetivo ao estimar incerteza. O ASR condicionado à leitura é descritivo, pois a defesa também altera a exposição. Falhas encontradas viram regressões offline. Custo e quantidade de execuções serão definidos após piloto de latência e capacidade.

## Critérios de aprovação e entrega

O juiz independente recebe este plano e o código atual. Avalia correção, compatibilidade, identidade experimental, recuperação de falhas, segurança de registros, testes e escopo. Aprovação exige ausência de bloqueadores e nota mínima 8/10. Revisões do plano motivadas pelo parecer são submetidas novamente. A aprovação é revisão automatizada e mantém a maturidade tested após implementação, sujeita à revisão humana prevista em CONTRIBUTING.md.

Entregar a etapa 1 em branch com commit de autoria configurada no Git e PR em português, respondendo às seis perguntas do repositório. O PR inclui plano, parecer, implementação, testes e documentação de uso.

## As seis perguntas

- Aprendizado esperado: quais condições tornam uma retomada experimental auditável.
- Reprodução: testes offline e comandos documentados no README do kit.
- Uso: avaliações retomáveis e comparação entre revisões de agentes.
- Limites de uso: identidade registrada não garante determinismo do provedor nem valida a eficácia das defesas.
- Avaliação: critérios verificáveis acima e revisão independente do plano.
- Melhoria: executar as etapas 2 e 3 e revisar decisões com nova evidência.

## Referências científicas

- AgentDojo (2024), ambiente extensível de avaliação de ataques e defesas. https://arxiv.org/abs/2406.13352
- Zhan et al. (2025), avaliação adaptativa de defesas. https://aclanthology.org/2025.findings-naacl.395/
- CaMeL (2025), isolamento de controle e políticas de fluxo de dados. https://arxiv.org/abs/2503.18813v2
- AutoDojo (2026), avaliação adaptativa e relação entre especificação da tarefa e segurança. https://arxiv.org/abs/2606.15057v3
