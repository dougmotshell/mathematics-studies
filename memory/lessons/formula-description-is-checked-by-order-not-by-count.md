**Tipo:** sucesso
**ID:** L-012
**Contexto:** 2026-08-01, TCK-0005 — completar as descrições textuais (`*Leitura:*` /
`*Reading:*`) das 8 fórmulas em display do nó piloto `quadratic-equations`, que tinha só 3
descritas nos dois idiomas.

**Lição:** contar descrições não prova acessibilidade da matemática. Um arquivo pode ter
8 fórmulas e 8 descrições e ainda assim deixar uma fórmula muda (duas descrições coladas na
mesma fórmula, uma órfã em outra seção). O que a regra de `AGENTS.md` §9.2 exige é
**proximidade e correspondência um-para-um**, e isso só se verifica olhando a **ordem** das
ocorrências, não o total. Do mesmo modo, "descrever" não é nomear: `a fórmula de Bhaskara`
não permite reconstruir o LaTeX; ler a estrutura na ordem escrita permite. E, como a
descrição é texto novo colado numa fórmula existente, ela é um vetor silencioso de afirmação
matemática nova — o autor da descrição não pode ser quem valida o rigor dela.

**Como aplicar:**

1. Verificar com `grep -n '^\$\$\|^\*Leitura:\*\|^\*Reading:\*' <arquivo>` e conferir que a
   saída **alterna estritamente** fórmula → descrição. Contagem (`grep -c`) é o segundo
   check, nunca o único.
2. Provar que só houve acréscimo de texto: `git diff -U0 -- content/ | grep -E '^-[^-]'`
   vazio. Citar essa evidência no `log.md` — é o que fecha o critério "LaTeX intocado" sem
   depender da palavra do autor.
3. Ler a estrutura da esquerda para a direita, na ordem escrita, com agrupamento explícito
   (`abre/fecha parênteses`, `tudo dividido por`), relações (`igual a`, `maior/menor que`),
   implicação (`o que implica` para `\Longrightarrow`) e índice (`x índice 1` /
   `x subscript 1`). Números por extenso. Nada de interpretar, justificar ou "melhorar".
4. Mandar a descrição para o `math-reviewer` mesmo quando ela "só lê" a fórmula — erro de
   escopo de sinal (`-\frac{b}{a}` lido como `menos b, dividido por a`) e de agrupamento de
   numerador são silenciosos e passam em qualquer auditoria automática.
5. `scripts/audit-content.sh` **não** checa descrição de fórmula: auditoria verde não é
   evidência para esse critério.
