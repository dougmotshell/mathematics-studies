---
id: TCK-0019
title: Medir o orçamento de performance no CI, sem coleta de visitante
type: infra
status: in_progress
owner: devops-engineer
priority: P2
size: M
created: 2026-08-01
updated: 2026-08-01
related: [TCK-0015, ADR-0003, ADR-0006]
---

# TCK-0019 — Medir o orçamento de performance no CI, sem coleta de visitante

## Pedido original (verbatim)

> Ativei o Analytics e Speed Insights na Vercel

> siga com a segunda alternativa

Decisão do usuário (2026-08-01): medir performance por **Lighthouse no CI**, em vez de
instrumentar Speed Insights nas páginas.

## Requisito refinado

O `RNF-8` da spec exige orçamento de performance, e a task 11 o registra como critério do
`/pwa-audit` — mas nada o mede hoje. As duas formas de medir têm custos diferentes:
instrumentar Speed Insights daria dado de campo ao preço do primeiro JavaScript do site,
de coleta a partir do navegador do visitante (público que inclui menores) e de um ADR de
privacidade; medir no CI dá dado de laboratório, com **zero coleta**, e mantém o site em
zero JS.

O usuário escolheu a segunda. Este ticket a implementa.

Estado medido em 2026-08-01: Speed Insights está **ligado no painel da Vercel e inerte** —
`/_vercel/speed-insights/script.js` responde 200, mas nenhuma página carrega o script, e o
HTML publicado tem 2.190 e 2.246 bytes sem nenhum `<script>`.

## Critérios de aceite

- [ ] 1. O CI mede Lighthouse contra o site **construído** (`dist/`), em PR e em push na
      `main`, sem depender de URL pública nem de deploy concluído.
- [ ] 2. Existe orçamento declarado em arquivo versionado, com **valor e justificativa** por
      métrica — no mínimo LCP, CLS, TBT e peso total transferido. Números escolhidos para o
      público-alvo (dispositivo modesto, rede lenta), não os padrões da ferramenta.
- [ ] 3. O CI **falha** quando o orçamento é estourado, e a saída diz qual métrica, qual
      valor medido e qual o limite. Provado com uma regressão sintética.
- [ ] 4. **Zero dado sai da máquina de CI**: nenhum upload de relatório, nenhum servidor
      externo, nenhuma conta. Se a ferramenta oferecer armazenamento remoto, ele fica
      explicitamente desligado e isso é verificado.
- [ ] 5. Nenhum JavaScript é acrescentado ao site publicado — `dist/` continua sem
      `<script>`, e o portão de terceiros do TCK-0015 continua verde.
- [ ] 6. Toda dependência nova é **de desenvolvimento** (`devDependencies`), nunca de
      produção; `dependencies` continua com `astro` apenas.
- [ ] 7. A medição é reprodutível localmente pelo mesmo comando que o CI usa — não há
      caminho só-CI que ninguém consegue rodar na mão.
- [ ] 8. O resultado é legível sem abrir artefato: as métricas medidas aparecem no log do
      passo, não só num relatório anexado.
- [ ] 9. `bash scripts/audit-ai-surface.sh`, `bash scripts/audit-content.sh` e
      `bash scripts/validate-content.sh` sem erros; `npm run build` continua exit 0.

### Requisitos transversais (marcar todos)

- [ ] Bilinguismo pt-BR + en-US · [x] não aplicável (ferramenta de CI)
- [x] Acessibilidade WCAG 2.2 AA — se a ferramenta já mede a11y, reportar é barato; **não**
      transformar em portão neste ticket (é o `/a11y-audit`, task 12)
- [x] Funciona offline / PWA — o orçamento é insumo do `/pwa-audit`
- [x] Custo zero mantido — nada pago, nada com conta
- [x] Privacidade e dados de menores (LGPD/COPPA) — **é o motivo desta escolha**: nenhum
      dado de visitante é coletado
- [ ] URLs de `content/` preservadas · [x] não aplicável
- [ ] Correção matemática verificada · [x] não aplicável

## Fora de escopo

- Instrumentar Speed Insights ou Web Analytics — decisão do usuário foi não instrumentar.
  Se um dia mudar, exige ADR de privacidade (`ADR-0003`, `ADR-0006`).
- Desligar as opções no painel da Vercel — ato do usuário, fora do repositório.
- Otimizar performance. Este ticket **mede**; corrigir o que a medição acusar é ticket
  próprio.
- Auditoria de acessibilidade como portão — task 12.
- Alterar `content/`, `docs/adr/`, `docs/specs/` ou o desenho das telas.

## Contexto e referências

- `docs/specs/minimum-learning-slice/spec.md` — RNF-8; `tasks.md` task 11
- `docs/adr/ADR-0006-continuous-integration-and-publication.md` (`accepted`) — o pipeline
- `docs/adr/ADR-0003-platform-stack.md` (`accepted`) — sem telemetria identificável
- `.github/workflows/ai-surface-audit.yml` — onde o passo entra
- `package.json`, `astro.config.mjs`, `vercel.json` — TCK-0015
- Site em produção: `https://mathematics-studies.vercel.app` (3 páginas, zero JS)

## Perguntas em aberto

- Nenhuma. Os números do orçamento são decisão técnica deste ticket, com justificativa.

## Resultado final

<preenchido pelo qa-validator ao marcar `done`>
