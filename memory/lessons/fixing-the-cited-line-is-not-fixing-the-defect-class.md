**Tipo:** erro
**ID:** L-013
**Contexto:** 2026-08-01, `TCK-0003`, loop 2/3. Corrigi o defeito B2 ("o ADR fixa o momento de
renderização do KaTeX") nas duas ocorrências **citadas** pelo `code-reviewer` — a consequência
em prosa e a regra 4 de `memory/context/frontend.md` — e escrevi a lição L-011 sobre o assunto.
Na mesma entrega, o rótulo do nó `H` do Mermaid do próprio ADR continuou dizendo "KaTeX
pré-renderizado". Novo `REJECT` (B4), pela mesma frase, no mesmo arquivo.

**Lição:** corrigir as linhas apontadas **não** é corrigir o defeito. O `REJECT` lista
evidências, não o inventário completo; quem produziu é que precisa varrer o artefato inteiro
atrás da **classe** do erro. E a varredura precisa ser textual (`grep` pelo termo do defeito —
aqui bastava `grep -n "renderiz" no arquivo`), porque a releitura humana pula o que não é
prosa: rótulo de diagrama, tabela, front matter, exemplo de código. Segundo agravante: pelo
`docs/DOC-STANDARDS.md` o Mermaid é **parte normativa** do documento — quem lê o diagrama
recebe a restrição errada e não tem como saber qual das duas afirmações vale.

**Como aplicar:** ao resolver um `REJECT`, extrair da descrição do defeito **um termo de
busca** e rodá-lo sobre todos os artefatos da entrega antes do handoff (aqui: `renderiz`;
em L-010: o número do ADR). Só declarar resolvido depois que a busca voltar limpa ou com
ocorrências justificadas uma a uma. Diagrama, tabela e rótulo entram na revisão com o mesmo
peso do texto. Complementa [[adr-decides-constraints-not-implementation-timing]] (o *quê*) e
[[accepting-an-adr-means-updating-the-rules-agents-read]] (varrer da raiz, não de uma lista
escolhida a dedo).

**Adendo — 2026-08-01, `TCK-0011` (reincidência, com uma distinção que importa):** a classe do
defeito de marcação tem **duas direções**, e varrer só uma não é varrer a classe. No
`c4-container.md` encontrei e corrigi um caso de **marcar de mais** (um boundary inteiro
rotulado `PROPOSTO` contendo build que o `ADR-0003` já exige) e, satisfeito com a correção,
entreguei com um caso de **marcar de menos** na mesma malha de relações — uma `Rel` sem
marcador entre duas marcadas. Achar uma ocorrência **aumenta** a chance de haver outra, e a
busca tem de ser pela dimensão (aqui: "toda `Rel` e todo nó do bloco, um a um, cada um com sua
fonte"), não pelo termo do defeito já encontrado. Receita barata que teria pego: listar as
relações do diagrama e escrever ao lado de cada uma a fonte que a sustenta; a que ficar sem
fonte é o defeito.
