---
name: handoff
description: Registra formalmente a transição de um ticket entre agentes — grava a entrada HANDOFF no log.md, atualiza status e owner no ticket.md e aciona o próximo agente imediatamente. Usar em toda troca de dono dentro de um ticket.
---

# Skill: /handoff

Executa uma transição de dono conforme
[`docs/ai/ticket-protocol.md`](../../../docs/ai/ticket-protocol.md).

## Passos

1. **Localizar** o ticket (`tickets/TCK-NNNN-*/`) e ler `ticket.md` + as últimas entradas do
   `log.md` (para descobrir o próximo `[SEQ]`).
2. **Validar** que a entrega do agente atual está completa o suficiente para a próxima etapa:
   - houve trabalho real (arquivos tocados / decisão registrada)?
   - existe **evidência** do que foi feito (saída de comando, screenshot, hash)?
   - os critérios de aceite atendidos estão marcados?
   Se não, registrar `ACTION` explicando e **não** fazer o handoff.
3. **Append** no `log.md`:

   ```markdown
   ## [SEQ] HANDOFF — AAAA-MM-DD HH:MM
   - De: <agente> → Para: <agente>
   - Status novo: <triaged|in_progress|in_review|in_validation|done|blocked>
   - O que foi feito: <2–5 linhas objetivas>
   - Artefatos: <arquivos, commits, screenshots>
   - Como validar: <comandos/passos exatos>
   - Pendências e riscos: <o que NÃO foi feito>
   - Critérios de aceite: [x] atendidos / [ ] restantes
   ```

4. **Atualizar** `ticket.md`: campos `status:`, `owner:` e `updated:`.
5. **Acionar o próximo agente imediatamente** — handoff registrado significa execução, não
   fila. O usuário só é chamado em `done`, `blocked: human-input` ou escalada por 3 loops.

## Variações

- **REJECT** (reprovação): use o formato `REJECT`, com defeitos numerados, cada um com
  evidência e critério violado, e o número do loop (`n/3`). O dono volta a ser o autor.
- **SPAWN** (subagente): registre antes de o subagente atuar, com motivo e escopo delegado.
- **STOP** (usuário interrompe): status vira `blocked: human-input`; nenhum agente continua
  até novo handoff explícito.
- **CORRECTION**: para consertar um registro anterior — nunca editar entrada existente.

## Regras

- `log.md` é **append-only**; `[SEQ]` incremental sem buracos.
- Evidência > afirmação: "os testes passam" exige a saída do comando.
- Nenhum agente valida artefato produzido pela própria cadeia.
- 3 devoluções no mesmo par → escalar ao `tech-lead`.
- A `ACTION` que resolve um `REJECT` termina com `Lição: L-NNN` ou
  `Lição: n/a — erro pontual`.
