# Tickets — Fluxo de Desenvolvimento

> Unidade de trabalho do sistema de agentes ([`.claude/agents/`](../.claude/agents/)).
> Criados pela skill `/ticket`; movidos pelo
> [protocolo de tickets](../docs/ai/ticket-protocol.md); auditáveis pelo `log.md` de cada um.

## Estrutura

```
tickets/
  TICKET-TEMPLATE.md        # modelo (não editar; copiar)
  TCK-0001-<slug>/
    ticket.md               # pedido, requisito refinado, critérios de aceite, status
    log.md                  # auditoria append-only: ACTION, HANDOFF, REJECT, SPAWN (com [SEQ])
    assets/                 # screenshots, evidências, diagramas (opcional)
```

## Regras

1. **Numeração** sequencial `TCK-NNNN` (4 dígitos); slug curto en-US
   (`TCK-0003-exercise-player`).
2. **Status vive no `ticket.md`** (campo `status:`) e só muda junto com uma entrada de
   handoff no `log.md`.
3. **`log.md` é append-only** — corrigir registro = entrada `CORRECTION`, nunca edição.
4. Commits do ticket usam o prefixo `TCK-NNNN:`; commit e push só com pedido explícito.
5. Ticket `done` **nunca reabre** — regressão vira ticket novo referenciando o original.
6. Um agente por vez é o **dono** (campo `owner:`); trabalho paralelo exige tickets
   separados ou subagentes (`<agente>#N`).
7. Critérios de aceite são a **definição de pronto** — não a opinião do agente.

## Ciclo (resumo)

`new` → tech-lead → `triaged` → agente da área → `in_review` (code-reviewer) →
`in_validation` (qa-validator) → `done` → docs-writer.
Reprovações voltam ao autor (máx. 3 loops → tech-lead → usuário).
Detalhes: [ticket-protocol](../docs/ai/ticket-protocol.md).

## Tipos de ticket

| Tipo | Uso |
|---|---|
| `feature` | Funcionalidade nova na plataforma |
| `bug` | Comportamento errado (inclui erro matemático em conteúdo publicado) |
| `content` | Criação ou revisão de conteúdo (nós, trilhas, exercícios) |
| `infra` | CI/CD, deploy, build, ambiente |
| `docs` | Documentação interna |
| `security` | Privacidade, dados de menores, vulnerabilidade |
| `research` | Investigação que termina em recomendação, não em código |
