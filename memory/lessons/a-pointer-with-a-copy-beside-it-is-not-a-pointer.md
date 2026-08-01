**Tipo:** correção
**ID:** L-024
**Contexto:** 2026-08-01, `TCK-0007` `[003]` (a). O critério 5 do ticket referenciava a fonte
certa — "cada ocorrência listada no critério 7 do **TCK-0006**" — e, entre parênteses,
resumia a lista: "(`\dfrac` do Resumo, 143-144 / 140-141; as 10 `\frac` de `exercises.json`)".
Quando a cadeia do TCK-0006 refez o inventário pelo método certo, ele passou de 18 para **22
pontos** e mudou de distribuição. O ponteiro continuou correto; o parêntese ficou errado e
passou a **contradizer** o que ele apontava. Nenhuma verificação automática acusa isso: as
duas frases estão no mesmo critério e nenhuma é falsa isoladamente.

**Lição:** ponteiro com cópia ao lado não é ponteiro — é **duas fontes**, e a que o leitor
obedece é a que está ao alcance dos olhos, não a que exige abrir outro arquivo. Vale para
critério de aceite que resume a lista que referencia, para documento que "só relembra" o número
de um ADR, e para ferramenta que reimplementa a regra de outra em vez de chamá-la (mesma
classe, escala diferente: `TCK-0017`, `audit-content.py` × `validate-content.py`). Enquanto as
duas cópias concordam, a duplicação parece inofensiva; ela só cobra o preço quando a fonte
muda, e aí cobra em silêncio.

**Como aplicar:** ao escrever um critério, uma restrição ou um checklist que dependa de uma
lista mantida em outro lugar, **nomear o local com precisão de âncora** (arquivo + entrada +
seção, ex.: `TCK-0006/log.md` `[007]` §2) e **não enumerar itens ao lado** — nem "para
facilitar". Se o leitor precisa de um exemplo, marque-o como exemplo (`ex.:`), nunca como
recorte do conjunto. Se a lista **precisa** estar nos dois lugares, o segundo diz de onde veio
e qual entrada do log a substitui, e a entrega que muda a fonte varre os ponteiros
(`grep -rn "TCK-NNNN" tickets/ docs/`). Teste de uma linha: *se a fonte dobrar de tamanho
amanhã, este texto fica errado ou só fica incompleto?* Se fica **errado**, é cópia disfarçada
de ponteiro. Complementa [[fixing-the-cited-line-is-not-fixing-the-defect-class]] (varrer a
classe, não a lista citada).
