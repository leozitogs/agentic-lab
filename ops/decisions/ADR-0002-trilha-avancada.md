---
tipo: adr
maturidade: reviewed
versao: 0.2.0
autores: [leozitogs]
criado_em: 2026-11-12
atualizado_em: 2026-11-12
status: aceito
---

# ADR-0002 · Trilha avançada em módulos

## Status

Aceito.

## Contexto

A trilha de fundamentos (8 semanas) cobre prompts, skills, MCP, avaliação e segurança. Quem termina precisa de um caminho para aprofundar, e os temas avançados têm tamanhos e dependências diferentes entre si. Um calendário rígido de semanas não encaixa bem.

## Decisão

Criar a trilha avançada em `learn/avancado/`, organizada em **módulos de ritmo livre** em vez de semanas:

- Módulos 1 a 4 como base (padrões de agentes, ferramentas e saídas estruturadas, RAG, memória).
- Módulos 5 a 10 em qualquer ordem (agentes de código, avaliação e red teaming, segurança, observabilidade, modelos abertos, multimodal).
- Módulo 11 como projeto integrador.

Cada módulo pede a comparação de pelo menos duas ferramentas no mesmo exercício, e todos os exercícios usam dados públicos ou sintéticos.

## Consequências

- O glossário ganha termos de arquitetura, recuperação, avaliação, segurança e modelos.
- O ROADMAP passa a prever kits práticos para os módulos.
- A trilha não reproduz a arquitetura de nenhum sistema interno de terceiros.
