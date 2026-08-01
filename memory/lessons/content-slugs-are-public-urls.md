**Tipo:** sucesso
**ID:** L-003
**Contexto:** 2026-08-01, desenho da taxonomia de conteúdo (`ADR-0001`).

**Lição:** decidir desde o primeiro nó que o caminho `content/<stage>/<area>/<topic>` é um
**contrato público** (URL indexada, link compartilhado por professores, favorito de aluno)
evita a migração dolorosa que acontece quando a organização "provisória" precisa mudar depois
de o conteúdo já circular.

**Como aplicar:** escolher slugs en-US descritivos e atemporais na criação do nó (nada de
`part-1`, `new`, `v2`). Renomear exige ADR + redirect permanente. Reorganização de estrutura é
decisão arquitetural, não faxina: passa pelo `curriculum-architect` e por
`/create-adr`. Ver [[bilingual-content-is-not-translated-later]].
