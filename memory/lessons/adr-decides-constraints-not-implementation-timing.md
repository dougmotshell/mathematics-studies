**Tipo:** erro
**ID:** L-011
**Contexto:** 2026-08-01, `TCK-0003` — ao escrever as consequências do `ADR-0003`, a frase
"a fórmula chega ao navegador já renderizada" fechou o **momento** de renderização do KaTeX
(build × runtime), que `docs/specs/minimum-learning-slice/plan.md` lista explicitamente como
decisão de implementação. `REJECT` do `code-reviewer` (defeito B2).

**Lição:** ao detalhar consequências, é fácil escorregar de "o que a decisão exige" para "como
implementar" — a frase soa natural porque **parece** corolário da stack, mas não é: ilhas
hidratadas podem renderizar em runtime. ADR que decide implementação rouba a decisão do ticket,
contradiz specs paralelas e envelhece mal, porque passa a exigir novo ADR para mudar algo que
nunca precisou de um.

**Como aplicar:** escrever consequência como **resultado exigido e verificável** ("fórmula em
display acessível a leitor de tela, sem custo de JavaScript desproporcional"), não como
mecanismo ("pré-renderizado na build"). Ao revisar o próprio ADR, para cada afirmação
perguntar: isto é *consequência necessária* da decisão, ou uma das várias maneiras de
atendê-la? Se for a segunda, mover para a lista do que o ADR **não** decide. Regra vale também
para a memória de área — `memory/context/<área>.md` não pode endurecer o que o ADR deixou
aberto.

**Adendo — 2026-08-01, `TCK-0011` (reincidência):** o mesmo padrão voltou no `ADR-0007`, que
fixou `prebuild` como lugar do portão de validação do acervo — item que
`docs/specs/minimum-learning-slice/plan.md:140` atribui explicitamente ao ticket. A frase
delatora tem forma fixa: **"é isso que faz X ser Y, e não Z"**. Ela aparece como *justificativa
de apoio* de um item legítimo (o conteúdo do `package.json`), não como item da lista de
decisões — por isso passa pela triagem feita antes de redigir e só é pega numa segunda leitura
do texto pronto. Agravante detectável sozinho: o **ADR gêmeo**, escrito na mesma entrega,
chamava a mesma consequência de "hipótese, não fato". Dois documentos da mesma entrega
discordando sobre o mesmo fato é sintoma, não coincidência — antes do handoff, comparar as
consequências gêmeas dos ADRs irmãos, frase a frase.
