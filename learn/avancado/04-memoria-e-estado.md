---
tipo: guide
maturidade: draft
versao: 0.2.0
autores: [leozitogs]
criado_em: 2026-11-12
atualizado_em: 2026-11-12
---

# Módulo 04 · Memória e estado

## Objetivo

Dar continuidade a conversas e tarefas longas sem estourar o contexto nem perder informação importante.

## Perguntas que o módulo responde

- O que guardar, por quanto tempo e como recuperar?
- Como retomar uma tarefa interrompida?

## Tópicos

1. Memória de curto prazo: janela de contexto e sumarização.
2. Memória de longo prazo: fatos, preferências e episódios.
3. Persistência de estado e checkpoints.
4. Esquecimento e privacidade (LGPD).
5. Compactação de contexto em tarefas longas.

## Ferramentas para comparar

Escolha pelo menos duas e compare no mesmo exercício. O objetivo é entender o trade-off, não decorar uma ferramenta.

- Mem0
- Letta (MemGPT)
- Checkpointers do LangGraph
- Banco relacional simples

## Leituras

- Packer et al., "MemGPT" (2023).
- Documentação de persistência do LangGraph.

## Exercício

Crie um assistente de estudos que lembra o que o usuário já estudou entre sessões e consegue esquecer um dado quando pedido.

## Critério de aceite

- [ ] Retomada correta depois de reiniciar o processo.
- [ ] Pedido de esquecimento removendo o dado de verdade.
