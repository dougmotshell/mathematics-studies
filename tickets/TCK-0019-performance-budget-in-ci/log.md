# Log — TCK-0019

> Auditoria append-only. Formatos em `docs/ai/ticket-protocol.md`.

## [001] ACTION — 2026-08-01 18:40 — tech-lead
- Ação: ticket criado após o usuário ativar Analytics e Speed Insights no painel da Vercel e,
  diante das opções, escolher medir performance no CI em vez de instrumentar as páginas.
- Medição que informou a decisão: ligar no painel **não coleta** em site estático. Endpoint
  `/_vercel/speed-insights/script.js` responde 200, mas o HTML publicado (2.190 e 2.246
  bytes) não tem nenhum `<script>` — a coleta exigiria instalar o pacote e adicionar o
  componente, o que não foi feito.
- Resultado: ok — status `new`, owner `tech-lead`.

## [002] ACTION — 2026-08-01 18:40 — tech-lead
- Ação: triagem. Tipo `infra`, P2, tamanho M, owner `devops-engineer` (CI é escopo dele).
- Motivo da prioridade P2: não bloqueia ticket algum; fecha uma lacuna real (RNF-8 exigido e
  não medido) sem urgência.
- Cadeia: `devops-engineer` → `code-reviewer` → `qa-validator`.
- Restrições: zero coleta de visitante; nenhuma dependência de produção; nenhum JS no site;
  nada sai da máquina de CI.
- Resultado: ok — `triaged`.

## [003] HANDOFF — 2026-08-01 18:40
- De: tech-lead → Para: devops-engineer
- Status novo: in_progress
- O que foi feito: decisão do usuário registrada e recortada em ticket com critérios.
- Artefatos: `tickets/TCK-0019-performance-budget-in-ci/ticket.md`.
- Como validar: critérios 1–9, com regressão sintética estourando o orçamento.
- Pendências e riscos: o portão de terceiros do TCK-0015 é sensível — a ferramenta não pode
  acrescentar recurso ao `dist/`; e ferramenta de performance costuma oferecer upload de
  relatório ligado por padrão, o que violaria o critério 4.
- Critérios de aceite: [ ] 1–9 restantes.
