# Operação do GitHub

## Triagem e manutenção

Issues são o ponto de entrada para problemas, propostas e vivências. Os formulários em `.github/ISSUE_TEMPLATE/` organizam contexto e reprodução, mantendo a opção de issue livre. Use os labels existentes `bug`, `documentation`, `enhancement`, `question`, `good first issue` e `help wanted`.

Antes de marcar uma tarefa como `good first issue`, inclua os arquivos envolvidos, resultado esperado, verificação e alguém disponível para orientar. Uma conversa pode virar nota, experimento ou caso. Ao fechar, registre a conclusão e vincule os artefatos. Evite fechamento automático por inatividade enquanto a equipe constrói seus hábitos de colaboração.

## Proteção da main

O payload `.github/main-protection.json` define PR obrigatório, check `lab-check`, resolução de conversas e bloqueio de force push e exclusão, inclusive para administradores. A contagem de aprovações começa em zero conforme a governança de mantenedor único.

Após o workflow `Lab check` produzir o check `lab-check` em um PR, um administrador pode aplicar a configuração versionada. O comando substitui a proteção clássica da branch, portanto confira o estado remoto antes de reaplicar para preservar mudanças posteriores.

```bash
gh api repos/leozitogs/agentic-lab/branches/main/protection
gh api --method PUT repos/leozitogs/agentic-lab/branches/main/protection --input .github/main-protection.json
gh api repos/leozitogs/agentic-lab/branches/main/protection
```

O primeiro comando retorna 404 se a branch ainda estiver sem proteção. O JSON de resposta final é a evidência da configuração aplicada. Este arquivo e o payload, isoladamente, descrevem a política desejada. Rulesets adicionais devem ser inspecionados nas configurações do repositório. A CI usa um check estável sem filtros de caminho para permitir a exigência em todo PR.

## Rotina de revisão

Verifique CI, escopo, evidência e crédito antes de integrar. Classifique comentários como bloqueadores ou sugestões, explique os motivos e ajude a pessoa a reproduzir falhas. Mantenha maturidade coerente com as revisões realizadas. Registre exceções e mudanças de padrão publicamente.

Antes de publicar uma release, confira o commit, as notas do roadmap, o estado dos testes e a disponibilidade do site. Divulgue resultados negativos junto das condições em que foram observados. Os templates e CODEOWNERS precisam acompanhar a evolução da equipe.

## Referências

Arquivos de comunidade em locais reconhecidos permitem que novos participantes encontrem as orientações pelo próprio GitHub. [GitHub Community Profiles](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories)

Proteção de branches permite exigir verificações e impedir reescrita do histórico. Nomes de checks devem ser únicos para evitar ambiguidade. [GitHub Protected Branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

## Relatos privados de vulnerabilidade

O recurso nativo de private vulnerability reporting foi habilitado nesta organização do laboratório. O procedimento está em [SECURITY.md](../SECURITY.md). Um administrador pode verificar seu estado com `gh api repos/leozitogs/agentic-lab/private-vulnerability-reporting`. Esse canal trata de segurança técnica. O contato privado próprio para conduta ainda precisa ser definido pelo mantenedor.
