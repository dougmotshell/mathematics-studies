// Workflow: auditoria da superfície de IA nos quatro CLIs.
// Verifica paridade, coerência semântica dos adapters e saúde da memória.
export const meta = {
  name: 'ai-surface-audit',
  description: 'Audita paridade e coerência da superfície de IA (Claude, Copilot, Gemini, Codex)',
  whenToUse: 'Após adicionar/alterar agents, skills ou adapters, ou periodicamente',
  phases: [
    { title: 'Scan', detail: 'auditoria determinística' },
    { title: 'Audit', detail: 'coerência semântica e higiene da memória' },
    { title: 'Verify', detail: 'verificação adversarial dos achados' },
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
        required: ['file', 'issue', 'suggestion'],
        properties: {
          file: { type: 'string' },
          issue: { type: 'string' },
          suggestion: { type: 'string' },
        },
      },
    },
  },
}

const VERDICT_SCHEMA = {
  type: 'object',
  required: ['isReal', 'reason'],
  properties: { isReal: { type: 'boolean' }, reason: { type: 'string' } },
}

phase('Scan')
const scan = await agent(
  'No repositório atual, execute `bash scripts/audit-ai-surface.sh` e ' +
    '`python3 scripts/sync-slash-commands.py --check`. Devolva a saída completa e um resumo ' +
    'do que está faltando ou desatualizado. Não corrija nada.',
  { label: 'scan:surface', phase: 'Scan' }
)

const DIMENSIONS = [
  {
    key: 'semantics',
    prompt:
      'Compare cada agent de .claude/agents/ com seu chatmode em .github/chatmodes/ e seu ' +
      'command em .gemini/commands/agent/. Aponte divergências SEMÂNTICAS: papel, escopo ' +
      'exclusivo, limites ou protocolo de memória que existem em um adapter e não no outro. ' +
      'Ignore diferenças puramente de formato.',
  },
  {
    key: 'instructions',
    prompt:
      'Verifique se AGENTS.md, CLAUDE.md, GEMINI.md, .codex/README.md e ' +
      '.github/copilot-instructions.md estão consistentes entre si: listas de agents/skills ' +
      'que citam itens inexistentes, capacidades presentes em um adaptador e ausentes noutro, ' +
      'e regras contraditórias. Compare com o conteúdo real de .claude/agents/ e ' +
      '.claude/skills/.',
  },
  {
    key: 'memory',
    prompt:
      'Audite a higiene da memória: memory/MEMORY.md e memory/LESSONS.md listam todos os ' +
      'arquivos reais e nenhum inexistente? Cada agent tem memory/agents/<name>.md? As lições ' +
      'seguem o formato (Tipo, ID, Contexto com data absoluta, Lição, Como aplicar)? Há lições ' +
      'duplicadas ou que são apenas resumo de tarefa em vez de regra aplicável?',
  },
  {
    key: 'links',
    prompt:
      'Verifique links markdown relativos quebrados em AGENTS.md, CLAUDE.md, GEMINI.md, ' +
      'README.md, CONTRIBUTING.md, docs/, memory/, tickets/, .github/ e .claude/. ' +
      'Reporte cada link cujo alvo não existe.',
  },
]

const results = await pipeline(
  DIMENSIONS,
  (d) =>
    agent(
      `${d.prompt}\n\nRepositório: diretório de trabalho atual.\n` +
        `Saída da auditoria determinística já executada:\n${scan}`,
      { label: `audit:${d.key}`, phase: 'Audit', schema: FINDINGS_SCHEMA }
    ),
  (review, d) =>
    parallel(
      (review?.findings ?? []).map((f) => () =>
        agent(
          `Tente REFUTAR este achado no repositório atual. Arquivo: ${f.file}. ` +
            `Problema alegado: ${f.issue}. Leia os arquivos envolvidos e confirme se o ` +
            `problema realmente existe. Em caso de dúvida, isReal=false.`,
          { label: `verify:${d.key}`, phase: 'Verify', schema: VERDICT_SCHEMA }
        ).then((v) => ({ ...f, dimension: d.key, verdict: v }))
      )
    )
)

const confirmed = results.filter(Boolean).flat().filter(Boolean).filter((f) => f.verdict?.isReal)
log(`${confirmed.length} achados confirmados na superfície de IA`)
return { confirmed }
