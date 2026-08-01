**Tipo:** correção
**ID:** L-014
**Contexto:** 2026-08-01, TCK-0005 — revisão de rigor do nó piloto
`content/high-school/algebra/quadratic-equations`. O enunciado do teorema da fórmula geral
(`theory.pt-BR.md:48` / `theory.en-US.md:47`) afirma "Se $a \neq 0$, as soluções reais … são
dadas por $x = \frac{-b \pm \sqrt{\Delta}}{2a}$" **sem** condicionar a $\Delta \ge 0$; a
ressalva só aparece na oração seguinte, na tabela de sinais. O mesmo padrão se repete no
Resumo (linha 143/140) e, em grau menor, na linha de soma e produto das raízes (144/141).

**Lição:** hipótese de **existência** faz parte do enunciado, não do parágrafo seguinte.
Quando a hipótese fica de fora, o resultado não costuma ser uma afirmação *falsa* — é uma
afirmação **mal-formada** para parte do domínio (aqui, $\sqrt{\Delta}$ não denota nada em
$\mathbb{R}$ quando $\Delta < 0$), e é por isso que o defeito passa despercebido: não existe
contra-exemplo para exibir, então nenhuma verificação numérica o pega. O critério certo não é
"a frase é falsa?", e sim "**existe valor admissível dos parâmetros para o qual o enunciado
não define o que afirma?**". Se existe, falta hipótese.

Duas consequências práticas que este caso deixou claras:

- **Proximidade não é hipótese.** "A ressalva vem logo depois" resolve para o leitor que lê a
  seção inteira em ordem; não resolve para quem chega pelo Resumo, por busca, por um card de
  revisão ou por leitor de tela navegando por títulos. Enunciado é unidade auto-contida.
- **Rigor omitido em nó-modelo é dívida multiplicada.** O custo de condicionar o enunciado é
  uma oração; o custo de corrigir depois é N nós que copiaram o formato.

**Como aplicar:**

1. Ao revisar qualquer enunciado com raiz, divisão, logaritmo, inversa, limite ou soma
   infinita, perguntar **antes de tudo**: para quais parâmetros a expressão do lado direito
   deixa de existir? Essa resposta é a hipótese que precisa estar na sentença
   (`\Delta \ge 0`, denominador $\neq 0$, argumento $> 0$, convergência…).
2. Preferir a forma bipartida, que não custa rigor nem didática:
   "Se `<hipótese>`, então `<conclusão>`; se `<hipótese falha>`, então `<o que ocorre>`."
   No caso quadrático: "Se $a \neq 0$ e $\Delta \ge 0$, as soluções reais são …; se
   $\Delta < 0$, não há solução real (há duas em $\mathbb{C}$)."
3. Achado desse tipo **não autoriza o revisor a reescrever** o enunciado dentro de um ticket
   que não o tem no escopo: vira defeito registrado no `log.md` com severidade e
   encaminhamento ao `tech-lead` para ticket próprio. Um ticket que só acrescenta texto
   continua aprovável com o achado em aberto — mas a correção **precede a saída de
   `status: "draft"`** do nó.
4. Todo achado assim dispara a varredura de `AGENTS.md` §6: repetir a busca no **resumo** e
   nos **exercícios** do mesmo nó (onde a compressão reintroduz a omissão) e nos nós irmãos
   (`find content -name meta.json`), antes de fechar o registro.
