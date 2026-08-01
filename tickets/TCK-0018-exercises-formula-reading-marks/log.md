# Log — TCK-0018

> Append-only. Formatos em `docs/ai/ticket-protocol.md`.

## [001] ACTION — 2026-08-01 19:30 — tech-lead
- Ação: criação do ticket pela **divisão do TCK-0007**, decidida e justificada em
  `tickets/TCK-0007-pilot-node-rigor-and-a11y-fixes/log.md` `[003]` (b) e (c). Recebe as 14
  ocorrências de `exercises.json` do inventário `TCK-0006/log.md` `[007]` §2; o TCK-0007 fica
  com as 8 de `theory.*.md`.
- Motivo: dois critérios de recorte apontaram para o mesmo lado. **Área:** `exercises.json` é
  artefato do `exercise-designer` (`AGENTS.md` §10) — mantê-lo no TCK-0007 obrigaria o
  `content-author` a editar a área de outro agente. **Tamanho:** 22 pontos com paridade
  obrigatória em 3 arquivos não cabem em um ticket `M`; divididos por artefato, cada metade
  cabe. Os diffs são disjuntos, então os dois podem correr em paralelo sem conflito.
- Resultado: ok — `tickets/TCK-0018-exercises-formula-reading-marks/` criado. Nenhum arquivo de
  `content/` tocado (`git status --short content/` → vazio).
- Lição: n/a — não resolve `REJECT`.

## [002] ACTION — 2026-08-01 19:32 — tech-lead
- Ação: triagem. Status `new` → `triaged`. **Sem `HANDOFF`** (L-005).
- **Tipo `content`** — toca só `content/`. **Tamanho M**: 1 arquivo, 14 pontos, 2 idiomas,
  revisão tripla. **Owner `exercise-designer`**: exercícios e feedback diagnóstico são a área
  exclusiva dele, e `[007]` §4 já inscreveu a norma no agent e na skill `/new-exercise-set`.
- **Prioridade P1, com o prazo relativo explícito:** *antes de o nó piloto sair de `draft`* —
  por causa de **uma** das 14 ocorrências, não das 14.
- **Cadeia:** `tech-lead` → `exercise-designer` → (`math-reviewer` ‖ `a11y-ux-reviewer` ‖
  `i18n-steward`, em paralelo) → `qa-validator`. Divisão de critérios: 1 e 4 →
  `math-reviewer`; 1, 2 e 3 → `a11y-ux-reviewer`; 5 e 6 → `i18n-steward`; 7–10 → `qa-validator`.
  Nenhum revisor escreve a redação que vai julgar.

### Por que o `math-reviewer` é obrigatório num ticket de acessibilidade

Sem a ocorrência 224/225, esta cadeia teria só `a11y-ux-reviewer` + `i18n-steward` — é
marcação verbal, não matemática. Ela muda isso: `$x^2 + 6x + 9 = (x+3)^2 = 0$` está
**matematicamente correto** e nenhuma conta a verificar existe; o defeito é que a leitura
linear ("x mais três ao quadrado") descreve tanto $(x+3)^2$ quanto $x + 3^2$ — **polinômios
diferentes**. O teste de aceite ("das palavras sozinhas sai **um** polinômio, e é $(x+3)^2$")
é juízo matemático, não tipográfico: quem decide se o objeto ficou determinado é o
`math-reviewer`. Daí a **assinatura dupla** do critério 1 — os dois revisores reconstroem às
cegas e registram a reconstrução, porque um pode achar a marcação inequívoca e o outro achá-la
impronunciável, e as duas coisas reprovam.

**Como classifiquei o item** (a pergunta que a cadeia do TCK-0006 me fez): **defeito de
acessibilidade com teste matemático**, não correção matemática. Chamar de erro matemático
mandaria o executor procurar uma conta errada que não existe; chamar de estilo inline o
rebaixaria a melhoria estética, e ele é o único ponto do lote de 22 em que a leitura errada
**troca o objeto**, não a fluidez.

### Mudança de critério de outro agente, registrada em vez de silenciosa

O `qa-validator#3` do TCK-0005 (`[011]`, pendência 4) classificou as fórmulas inline como
**"não condiciona `draft`"**. Mantenho para 13 das 14 e **reverto para a 224/225**. O
julgamento original é de antes de `[007]` §2 — a ocorrência era desconhecida naquele momento
(escapou do `grep '(-[0-9a-z]*)\^'`, que codificava "parênteses **com sinal negativo**"). Com
o fato novo, ela cai na mesma classe da pendência 3, que aquele mesmo QA declarou
condicionante: conteúdo didático inacessível não é melhoria. Registro a mudança aqui e no
"Contexto" do ticket; não altero o `[011]` de lá (append-only, e ticket `done` não reabre).

### Restrições passadas ao executor

1. **Não começar antes do TCK-0006 entregue** — a norma e os dois gatilhos vêm de lá.
2. **Varredura por predicado da classe, nunca pelos exemplos** (critério 3, adendo da L-021).
   Teste que o executor deve aplicar ao próprio padrão antes de usá-lo: *ele acha alguma
   ocorrência que eu ainda não vi?* Se só reencontra a lista, o padrão foi escrito da lista.
3. **Não tocar a matemática** (critério 4): gabarito, `answer`, `tolerance`, `verified`, `id` e
   o conteúdo dentro de `$…$` ficam como estão. Este ticket acrescenta palavras, não muda
   expressões — e a prova é um diff de campos, não uma promessa.
4. Os dois idiomas no mesmo ciclo (ADR-0002 / L-001); a marcação en-US sai da coluna en-US da
   tabela normativa, não de tradução literal da pt-BR.
5. Não mudar `status`, não renomear slug (L-003), não encostar em `theory.*.md`.
6. As 3 referências do nó são CC BY-NC-SA: citáveis, nada incorporado (L-009).

- **Aderência ao plano:** Fase 1 do roadmap — provar o formato com conteúdo real. O nó piloto
  é o modelo declarado em `meta.json` (`"notes"`), e exercício é o objeto que mais será copiado.
- **Requisitos inegociáveis conferidos:** bilinguismo (5, 6), acessibilidade (1, 2, 3),
  correção matemática (1, 4), gratuidade (só texto), URLs preservadas (8); offline e
  privacidade não aplicáveis, com o porquê no ticket.
- **Dependências:** depende do TCK-0006. **Independente do TCK-0007** (arquivos disjuntos) e
  do TCK-0017 (ferramenta, não conteúdo) — embora o critério 9 fique mais forte depois do
  TCK-0017, já que hoje o exit 0 do auditor vale menos do que parece.
- Resultado: ok — `status: triaged`, `owner: exercise-designer`. Aguardando ordem de execução.
- Lição: n/a — não resolve `REJECT`.
