// Workflow: revisão multidimensional de um nó de conteúdo.
// Fan-out por dimensão (rigor, didática, exercícios, i18n, acessibilidade), verificação
// adversarial de cada achado e síntese com veredito de publicação.
export const meta = {
  name: 'content-review',
  description: 'Revisa um nó de conteúdo em todas as dimensões, com verificação adversarial',
  whenToUse: 'Antes de publicar um nó de content/, ou quando o usuário pedir revisão completa de conteúdo',
  phases: [
    { title: 'Review', detail: 'um revisor por dimensão' },
    { title: 'Verify', detail: 'verificação adversarial de cada achado' },
  ],
}

const target = typeof args === 'string' ? args : (args?.node ?? 'content/')

const FINDINGS_SCHEMA = {
  type: 'object',
  required: ['findings'],
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        required: ['file', 'issue', 'suggestion', 'severity'],
        properties: {
          file: { type: 'string', description: 'caminho relativo do arquivo' },
          excerpt: { type: 'string', description: 'trecho exato do problema' },
          issue: { type: 'string', description: 'problema encontrado (pt-BR)' },
          suggestion: { type: 'string', description: 'correção sugerida (pt-BR)' },
          severity: { type: 'string', enum: ['bloqueante', 'importante', 'menor'] },
        },
      },
    },
  },
}

const VERDICT_SCHEMA = {
  type: 'object',
  required: ['isReal', 'reason'],
  properties: {
    isReal: { type: 'boolean' },
    reason: { type: 'string' },
  },
}

const base =
  `Você está revisando o conteúdo em "${target}" do repositório mathematics-studies ` +
  `(raiz do diretório de trabalho). Leia AGENTS.md e docs/content/ antes de julgar. ` +
  `Reporte apenas problemas concretos, com arquivo e trecho. `

const DIMENSIONS = [
  {
    key: 'rigor',
    prompt:
      base +
      'DIMENSÃO: rigor matemático. Verifique corretude das afirmações, hipóteses omitidas ' +
      '(continuidade, domínio, denominador não nulo, convergência), passos de demonstração ' +
      'que não se sustentam, casos-limite não tratados e gabaritos de exercícios (refaça-os ' +
      'de forma independente). Severidade "bloqueante" para qualquer erro matemático.',
  },
  {
    key: 'didactics',
    prompt:
      base +
      'DIMENSÃO: didática. Verifique a estrutura mínima de docs/content/content-standards.md ' +
      '(objetivo, pré-requisitos, intuição, definição formal, exemplos, erros comuns, resumo), ' +
      'progressão intuição→formalismo, calibragem da linguagem ao estágio do nó e exemplos que ' +
      'cobrem caso típico e não rotineiro.',
  },
  {
    key: 'exercises',
    prompt:
      base +
      'DIMENSÃO: exercícios. Verifique exercises.json contra docs/content/exercise-schema.md: ' +
      'gradiente de dificuldade 1→5, cobertura das skills declaradas em meta.json, feedback ' +
      'DIAGNÓSTICO por alternativa errada (não genérico), distratores plausíveis, ausência de ' +
      'duas alternativas corretas, dicas progressivas e solução passo a passo.',
  },
  {
    key: 'i18n',
    prompt:
      base +
      'DIMENSÃO: paridade pt-BR/en-US. Verifique docs/content/i18n.md: mesmas seções e exemplos ' +
      'nos dois idiomas, campos localizados completos, convenção de decimais por idioma, ' +
      'terminologia do glossário e traduções que alterem o significado matemático.',
  },
  {
    key: 'a11y',
    prompt:
      base +
      'DIMENSÃO: acessibilidade do conteúdo. Verifique docs/content/accessibility.md: descrição ' +
      'textual de toda equação em display, ausência de fórmula apenas como imagem, alt de ' +
      'imagens descrevendo o conteúdo matemático, informação não transmitida só por cor e ' +
      'clareza das instruções.',
  },
]

const results = await pipeline(
  DIMENSIONS,
  (d) => agent(d.prompt, { label: `review:${d.key}`, phase: 'Review', schema: FINDINGS_SCHEMA }),
  (review, d) =>
    parallel(
      (review?.findings ?? []).map((f) => () =>
        agent(
          `Tente REFUTAR este achado de revisão de conteúdo no repositório atual. ` +
            `Arquivo: ${f.file}. Trecho: ${f.excerpt ?? '(não informado)'}. ` +
            `Problema alegado: ${f.issue}. Leia o arquivo e confirme se o problema realmente ` +
            `existe. Para achados matemáticos, refaça o cálculo você mesmo. ` +
            `Em caso de dúvida, isReal=false.`,
          { label: `verify:${d.key}`, phase: 'Verify', schema: VERDICT_SCHEMA }
        ).then((v) => ({ ...f, dimension: d.key, verdict: v }))
      )
    )
)

const confirmed = results.filter(Boolean).flat().filter(Boolean).filter((f) => f.verdict?.isReal)
const blocking = confirmed.filter((f) => f.severity === 'bloqueante')

log(`${confirmed.length} achados confirmados · ${blocking.length} bloqueantes`)

return {
  target,
  confirmed,
  blocking: blocking.length,
  verdict: blocking.length === 0 ? 'pronto para publicar' : 'ajustes necessários',
}
