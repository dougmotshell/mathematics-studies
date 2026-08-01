# ADR-0004 — Desenvolvimento orientado a tickets com agentes de IA

- **Status:** accepted
- **Data:** 2026-08-01
- **Decisores:** Douglas Silva
- **Relacionados:** `docs/ai/ticket-protocol.md`, `tickets/README.md`

## Contexto

O projeto é conduzido majoritariamente por agentes de IA em diferentes CLIs (Claude Code,
Codex, Copilot, Gemini), com sessões efêmeras e independentes. Sem um contrato de trabalho
compartilhado, cada sessão recomeça do zero, não há trilha de auditoria, os mesmos erros se
repetem e ninguém sabe dizer o que está pronto de verdade.

Modelo de referência: o sistema de agentes + tickets do repositório `lernema`, cuja prática
(ticket como unidade de trabalho, `log.md` append-only, papéis com escopo exclusivo, loop
implementação → review → QA, memória persistente) já se mostrou eficaz.

## Alternativas consideradas

### A. Tickets versionados no repositório com log append-only (escolhida)
- **Prós:** estado e histórico legíveis por qualquer CLI, sem serviço externo; auditoria
  completa; retomável por outra ferramenta; custo zero.
- **Contras:** disciplina manual de registro; ruído de arquivos no repositório.

### B. Issues do GitHub como unidade de trabalho
- **Prós:** ferramenta pronta, notificações, integração com PRs.
- **Contras:** exige rede e autenticação em toda sessão; contexto fora do working tree;
  agentes sem acesso ao serviço ficam cegos.

### C. Sem tickets — tarefas conduzidas na conversa
- **Prós:** zero cerimônia.
- **Contras:** nada sobrevive ao fim da sessão; sem critérios de aceite, "pronto" vira
  opinião; erros se repetem.

## Decisão

Todo desenvolvimento, manutenção, correção de bug e produção de conteúdo de porte passa por um
ticket em `tickets/TCK-NNNN-<slug>/`, com `ticket.md` (pedido, critérios de aceite, status) e
`log.md` (auditoria append-only). Os agentes têm **escopo exclusivo**, trocam trabalho por
**handoff registrado** e o ciclo roda em loop até `done` — validado exclusivamente pelo
`qa-validator` contra os critérios de aceite. Limite de 3 loops no mesmo par antes de escalar.
Contrato completo em `docs/ai/ticket-protocol.md`.

## Consequências

**Positivas**
- Qualquer CLI retoma um ticket no meio sabendo exatamente o estado.
- "Pronto" passa a ser definido pelos critérios de aceite, não pela opinião do agente.
- Erros viram lições citáveis (`L-NNN`); repetir erro com lição registrada é bloqueante.
- Trabalho paralelo explícito, com subagentes numerados.

**Negativas / custos assumidos**
- Overhead de registro em cada etapa; tarefas triviais ficam mais caras (mitigado pelo
  `/dev-loop`, que atende tarefas pontuais sem ticket).
- Volume de arquivos Markdown cresce com o histórico.

**O que fica mais difícil depois desta decisão**
- Fazer alterações "rápidas" fora do fluxo sem perder rastreabilidade.

## Impacto

- **Processo/agentes:** define os papéis, o ciclo de vida e os formatos de log.
- **Plataforma/conteúdo:** commits passam a referenciar `TCK-NNNN:`.

## Como reverter

Reversível: bastaria parar de criar tickets. O histórico existente permanece legível.
