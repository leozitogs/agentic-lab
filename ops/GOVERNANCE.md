# Governança do agentic-lab

## Propósito e participação

O laboratório reúne estudo, prática e evidência sobre engenharia de IA. Pessoas podem propor, experimentar, revisar e manter artefatos. Participação assíncrona por issues e PRs permite acompanhar decisões e contribuir em qualquer ritmo.

## Papéis atuais

| Papel | Responsabilidade | Como participar |
|---|---|---|
| Participante | Perguntar, relatar experiências, propor e executar contribuições | Abrir issue, comentar ou enviar PR |
| Revisor | Conferir escopo, reprodução, resultados e clareza | Comentar evidências e limites em PRs |
| Mantenedor | Fazer triagem, decidir integração, cuidar de acessos e releases | Nomeação pública após contribuições e concordância explícita |

O mantenedor atual é Leonardo Gonçalves Sobral, [@leozitogs](https://github.com/leozitogs). `CODEOWNERS` encaminha revisões para ele. Novos responsáveis são registrados neste documento e no arquivo de ownership quando aceitarem o papel. Documentação, acolhimento e revisão também contam para assumir manutenção.

## Decisões

Correções pequenas seguem direto para PR. Mudanças de arquitetura, padrões de segurança, critérios científicos ou governança começam com uma proposta em issue e registram a decisão em `ops/decisions/` usando o template de ADR. O mantenedor procura consenso nos argumentos, registra objeções e explica a decisão quando houver divergência. Questões podem ser reabertas com novas evidências.

Uma issue deve deixar explícitos problema, responsável voluntário, próximo passo e critério de conclusão. Ninguém precisa assumir uma tarefa para fazer uma pergunta. PRs em rascunho recebem feedback durante a construção. Issues paradas podem ser retomadas por outra pessoa, com aviso no próprio tópico e preservação do crédito.

## Revisão e integração

Contribuições devem ter verificações adequadas ao impacto. Mudanças técnicas precisam de reprodução e testes relevantes. Relatos podem entrar como `draft` com contexto e limitações. Uma revisão automatizada deve identificar ferramenta, escopo e limitações. A promoção para `reviewed` exige revisão de outra pessoa.

Enquanto há um único mantenedor, ele pode integrar mudanças após CI e justificativa pública mesmo sem uma segunda aprovação. Os artefatos conservam sua maturidade real. Quando houver dois mantenedores ativos, a exigência de aprovação humana poderá ser ativada com uma atualização pública desta política.

Na `main`, a configuração técnica proposta exige PR, o check `lab-check` e resolução de conversas, bloqueia force push e exclusão e se aplica também ao administrador. Aprovações obrigatórias começam em zero para permitir o fluxo com um mantenedor. A configuração versionada e seu procedimento de ativação estão em [GITHUB.md](GITHUB.md). A existência deste documento não comprova que a proteção remota foi aplicada.

Use merge commit quando o histórico de autoria e as etapas ajudarem a revisão. Squash pode reunir ajustes de uma mesma contribuição com crédito de coautoria no commit final. Evite reescrever branches compartilhadas. Reversões são feitas por novos PRs que referenciam a mudança original.

## Crédito, licença e uso de IA

Preserve autoria dos commits e inclua coautores quando houver trabalho conjunto. Notas e experimentos registram autores e participantes com consentimento. Cite fontes e as licenças de dados e dependências. A licença do repositório é Apache-2.0; somente envie conteúdo que você possa compartilhar sob os termos aplicáveis.

Descreva assistência de IA que tenha produzido código, avaliação ou conclusões materiais, incluindo como o resultado foi verificado. A responsabilidade pela contribuição e suas fontes fica com quem a submete.

## Continuidade

Releases devem apontar para um commit, resumir entregas e distinguir resultados experimentais das mudanças de infraestrutura. Se um mantenedor se afastar, pode anunciar a transição em issue e indicar quem aceitou continuar. Novos acessos são concedidos pelo administrador após concordância pública. O roadmap recebe mudanças discutidas em issues. Nenhuma frequência de reunião ou resposta é condição para participar.

## Bases usadas

O OpenSSF recomenda processo público de contribuição, rastreabilidade e governança documentada. O desenho do laboratório aplica esses critérios com papéis compatíveis com a equipe atual. [OpenSSF Best Practices](https://www.bestpractices.dev/en/criteria)

Karl Fogel descreve revisão pública, comunicação registrada e ampliação da manutenção para participantes além de quem escreve código. Essas práticas orientam as decisões e o crédito neste laboratório. [Producing Open Source Software](https://producingoss.com/en/producingoss.html)

A revisão de Steinmacher e colaboradores sobre barreiras a novos participantes fundamenta a atenção a documentação de entrada, escolha da primeira tarefa e acolhimento. [Estudo de 2015](https://doi.org/10.1016/j.infsof.2014.11.001)
