// Workflow: revisão adversarial de um plano de implementação (spec/plan/tasks ou ticket).
// Painel de perspectivas independentes + síntese com veredito.
export const meta = {
  name: 'feature-plan-review',
  description: 'Revisa adversarialmente um plano de implementação por múltiplas perspectivas',
  whenToUse: 'Antes de aprovar uma spec ou iniciar a execução de um ticket de porte',
  phases: [
    { title: 'Review', detail: 'uma perspectiva por revisor' },
    { title: 'Synthesize', detail: 'veredito consolidado' },
  ],
}

const target = typeof args === 'string' ? args : (args?.path ?? 'docs/specs/')

const REVIEW_SCHEMA = {
  type: 'object',
  required: ['findings', 'verdict'],
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        required: ['issue', 'impact', 'suggestion', 'severity'],
        properties: {
          issue: { type: 'string' },
          impact: { type: 'string' },
          suggestion: { type: 'string' },
          severity: { type: 'string', enum: ['bloqueante', 'importante', 'menor'] },
        },
      },
    },
    verdict: { type: 'string', enum: ['aprovada', 'aprovada com ajustes', 'precisa retrabalho'] },
  },
}

const base =
  `Revise criticamente o plano em "${target}" do repositório atual. ` +
  `Leia AGENTS.md, docs/product/vision.md, docs/product/roadmap.md e os ADRs em docs/adr/. ` +
  `Seja cético: seu trabalho é achar o que vai dar errado, não elogiar. `

const LENSES = [
  {
    key: 'acceptance',
    prompt:
      base +
      'PERSPECTIVA: critérios de aceite. Cada critério é verificável e falharia se a ' +
      'implementação estivesse errada? Existe critério vago ("melhor", "intuitivo")? Falta ' +
      'critério para algum comportamento essencial descrito no plano?',
  },
  {
    key: 'requirements',
    prompt:
      base +
      'PERSPECTIVA: requisitos transversais obrigatórios. Bilinguismo pt-BR/en-US, ' +
      'acessibilidade WCAG 2.2 AA (inclusive matemática acessível), funcionamento offline/PWA, ' +
      'custo zero, privacidade de menores (LGPD/COPPA), estabilidade das URLs de content/ e ' +
      'correção matemática verificada. Aponte cada um que foi ignorado sem justificativa.',
  },
  {
    key: 'architecture',
    prompt:
      base +
      'PERSPECTIVA: arquitetura e decisões. O plano decide estrutura sem ADR aceito? Depende ' +
      'de ADR-0003 (stack) que ainda está "proposed"? Acopla o acervo (content/) à aplicação, ' +
      'violando a independência do contrato de dados? Introduz dependência ou serviço com ' +
      'custo recorrente?',
  },
  {
    key: 'risk',
    prompt:
      base +
      'PERSPECTIVA: risco e reversibilidade. O que é irreversível (URL pública, formato de ' +
      'dados, coleta de dados de usuário)? O que pode dar errado e como se detecta cedo? ' +
      'Qual a menor fatia entregável que já teria valor — o plano poderia ser cortado?',
  },
]

const reviews = await parallel(
  LENSES.map((l) => () =>
    agent(l.prompt, { label: `review:${l.key}`, phase: 'Review', schema: REVIEW_SCHEMA })
  )
)

const valid = reviews.filter(Boolean)
const findings = valid.flatMap((r, i) =>
  (r.findings ?? []).map((f) => ({ ...f, lens: LENSES[i]?.key }))
)
const blocking = findings.filter((f) => f.severity === 'bloqueante')
log(`${findings.length} achados · ${blocking.length} bloqueantes`)

phase('Synthesize')
const synthesis = await agent(
  'Consolide as revisões abaixo num parecer único em pt-BR: (1) achados bloqueantes, com a ' +
    'correção exata exigida; (2) achados importantes; (3) menor fatia entregável recomendada; ' +
    '(4) veredito final (aprovada | aprovada com ajustes | precisa retrabalho) com ' +
    'justificativa de uma linha. Não invente achados novos.\n\n' +
    JSON.stringify({ findings, verdicts: valid.map((r) => r.verdict) }, null, 2),
  { label: 'synthesize:verdict', phase: 'Synthesize' }
)

return { target, findings, blocking: blocking.length, synthesis }
