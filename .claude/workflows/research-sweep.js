// Workflow: varredura multi-ângulo de fontes gratuitas para um tópico de conteúdo.
// Ângulos independentes → deduplicação → verificação de licença → síntese citável.
export const meta = {
  name: 'research-sweep',
  description: 'Varre fontes gratuitas e literatura didática sobre um tópico, com licença verificada',
  whenToUse: 'Antes de escrever um nó de conteúdo novo ou ao montar references.json',
  phases: [
    { title: 'Sweep', detail: 'um pesquisador por ângulo' },
    { title: 'Verify', detail: 'checagem de licença e acesso gratuito' },
    { title: 'Synthesize', detail: 'síntese didática com fontes' },
  ],
}

const topic = typeof args === 'string' ? args : (args?.topic ?? '')
if (!topic) {
  log('Nenhum tópico informado — passe o assunto em args.')
  return { error: 'tópico não informado' }
}

const SOURCES_SCHEMA = {
  type: 'object',
  required: ['sources'],
  properties: {
    sources: {
      type: 'array',
      items: {
        type: 'object',
        required: ['title', 'url', 'covers'],
        properties: {
          title: { type: 'string' },
          author: { type: 'string' },
          year: { type: 'string' },
          url: { type: 'string' },
          language: { type: 'string' },
          license: { type: 'string', description: 'licença declarada, ou "desconhecida"' },
          covers: { type: 'string', description: 'o que exatamente a fonte cobre' },
        },
      },
    },
  },
}

const LICENSE_SCHEMA = {
  type: 'object',
  required: ['usable', 'license', 'reason'],
  properties: {
    usable: { type: 'boolean', description: 'gratuita e legalmente reutilizável' },
    license: { type: 'string' },
    reason: { type: 'string' },
  },
}

const ANGLES = [
  { key: 'textbooks', prompt: `livros-texto abertos e apostilas gratuitas sobre "${topic}" (ex.: OpenStax, AIM Open Textbook Initiative, materiais de universidades públicas)` },
  { key: 'courses', prompt: `cursos e vídeo-aulas gratuitos sobre "${topic}", em português e em inglês` },
  { key: 'exercises', prompt: `bancos de exercícios e problemas abertos sobre "${topic}", com gabarito` },
  { key: 'pedagogy', prompt: `literatura de educação matemática sobre como "${topic}" é ensinado: sequência típica, erros comuns documentados, representações eficazes` },
  { key: 'ptbr', prompt: `material gratuito em PORTUGUÊS sobre "${topic}" — o acervo em pt-BR costuma ser o mais escasso, procure especificamente` },
]

const swept = await pipeline(
  ANGLES,
  (a) =>
    agent(
      `Você é o researcher (.claude/agents/researcher.md). Procure ${a.prompt}. ` +
        'Para cada fonte, registre título, autor, ano, URL, idioma, licença declarada e o que ' +
        'ela cobre. Nunca inclua material pirateado. Fonte sem licença clara deve vir com ' +
        'license="desconhecida" — não invente.',
      { label: `sweep:${a.key}`, phase: 'Sweep', schema: SOURCES_SCHEMA }
    ),
  (res, a) =>
    parallel(
      (res?.sources ?? []).map((s) => () =>
        agent(
          `Verifique a fonte "${s.title}" (${s.url}). Ela é realmente GRATUITA e ` +
            'legalmente reutilizável? Qual a licença exata declarada na própria página? ' +
            'Se não for possível confirmar acesso gratuito e licença, usable=false.',
          { label: `verify:${a.key}`, phase: 'Verify', schema: LICENSE_SCHEMA }
        ).then((v) => ({ ...s, angle: a.key, check: v }))
      )
    )
)

const all = swept.filter(Boolean).flat().filter(Boolean)
const usable = all.filter((s) => s.check?.usable)
const seen = new Set()
const deduped = usable.filter((s) => {
  const key = (s.url || s.title).toLowerCase()
  if (seen.has(key)) return false
  seen.add(key)
  return true
})

log(`${all.length} fontes encontradas · ${deduped.length} utilizáveis após verificação`)

phase('Synthesize')
const synthesis = await agent(
  `Sintetize, em pt-BR, o que aprendeu sobre como ensinar "${topic}": sequência didática ` +
    'típica, pré-requisitos, erros comuns documentados na literatura, representações que ' +
    'funcionam bem. Cite a fonte de cada afirmação. Ao final, produza o conteúdo pronto de ' +
    'um references.json (campos author, year, url, language, license, covers) apenas com as ' +
    'fontes verificadas abaixo. Diga explicitamente o que NÃO foi encontrado.\n\n' +
    JSON.stringify(deduped, null, 2),
  { label: 'synthesize:research', phase: 'Synthesize' }
)

return { topic, sources: deduped, rejected: all.length - deduped.length, synthesis }
