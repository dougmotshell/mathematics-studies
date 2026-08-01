// Workflow: auditoria da taxonomia e do currículo.
// Procura lacunas de cobertura, ciclos e inconsistências de progressão no acervo.
export const meta = {
  name: 'curriculum-audit',
  description: 'Audita a taxonomia: lacunas, pré-requisitos, progressão e duplicação',
  whenToUse: 'Ao revisar a organização do acervo ou planejar o que produzir a seguir',
  phases: [
    { title: 'Scan', detail: 'levantamento mecânico do acervo' },
    { title: 'Audit', detail: 'um auditor por dimensão curricular' },
    { title: 'Synthesize', detail: 'plano priorizado de correções e lacunas' },
  ],
}

const FINDINGS_SCHEMA = {
  type: 'object',
  required: ['findings'],
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        required: ['node', 'issue', 'suggestion'],
        properties: {
          node: { type: 'string', description: 'id do nó ou "taxonomia" quando geral' },
          issue: { type: 'string' },
          suggestion: { type: 'string' },
          priority: { type: 'string', enum: ['alta', 'média', 'baixa'] },
        },
      },
    },
  },
}

phase('Scan')
const scan = await agent(
  'No repositório atual (raiz do diretório de trabalho), execute ' +
    '`bash scripts/audit-content.sh` e liste a estrutura de content/ ' +
    '(estágios, áreas e nós existentes, com difficulty e status de cada meta.json). ' +
    'Devolva um resumo textual objetivo: quantos nós por estágio/área, quais estão ' +
    'published, e a saída de erros/avisos do script. Não corrija nada.',
  { label: 'scan:content', phase: 'Scan' }
)

const DIMENSIONS = [
  {
    key: 'coverage',
    prompt:
      'Analise a cobertura curricular do acervo. Para cada estágio presente, identifique ' +
      'assuntos fundamentais AUSENTES que um aluno daquele nível precisaria — priorizando o ' +
      'que bloqueia a progressão para o estágio seguinte. Consulte docs/content/taxonomy.md.',
  },
  {
    key: 'progression',
    prompt:
      'Analise a progressão: saltos de dificuldade entre nós encadeados, pré-requisitos ' +
      'inflados (dependências desnecessárias que bloqueiam o aluno), nós órfãos (sem caminho ' +
      'de entrada) e becos sem saída (sem continuação declarada).',
  },
  {
    key: 'duplication',
    prompt:
      'Procure duplicação e sobreposição: o mesmo assunto tratado em nós diferentes sem ' +
      'abordagem distinta declarada nem referência cruzada (ADR-0001 proíbe cópia entre ' +
      'estágios). Aponte também tópicos que deveriam ser um subtópico de outro.',
  },
]

const results = await parallel(
  DIMENSIONS.map((d) => () =>
    agent(
      `${d.prompt}\n\nContexto do levantamento já realizado:\n${scan}\n\n` +
        'Trabalhe sobre o repositório atual. Reporte achados concretos, citando ids de nós.',
      { label: `audit:${d.key}`, phase: 'Audit', schema: FINDINGS_SCHEMA }
    )
  )
)

const findings = results.filter(Boolean).flatMap((r) => r.findings ?? [])
log(`${findings.length} achados curriculares`)

phase('Synthesize')
const plan = await agent(
  'Você é o curriculum-architect (.claude/agents/curriculum-architect.md). ' +
    'A partir dos achados abaixo, produza um plano priorizado em pt-BR: (1) correções ' +
    'estruturais urgentes; (2) lacunas de conteúdo a produzir, na ordem que destrava mais ' +
    'progressão; (3) reorganizações que exigiriam ADR. Inclua um diagrama Mermaid do grafo ' +
    'de pré-requisitos afetado. Seja concreto: cada item com o id do nó e a ação exata.\n\n' +
    JSON.stringify(findings, null, 2),
  { label: 'synthesize:plan', phase: 'Synthesize' }
)

return { findings, plan }
