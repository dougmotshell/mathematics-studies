**Tipo:** correção
**ID:** L-006
**Contexto:** TCK-0001, 2026-08-01. O `references.json` do nó piloto
`high-school/algebra/quadratic-equations` declarava `CC BY 4.0` para dois livros do
OpenStax, escrito de memória. Ao acessar as páginas, ambos declaram
`creativecommons.org/licenses/by-nc-sa/4.0` — "Algebra and Trigonometry 2e" e
"Intermediate Algebra 2e" são **CC BY-NC-SA 4.0**.
**Lição:** "OpenStax é CC BY" é falso como regra: a licença varia **por livro** (e por
edição). Licença anotada de memória é chute, e o erro é caro — CC BY-NC-SA proíbe uso
comercial e obriga share-alike em qualquer adaptação, o que muda o que a plataforma pode
fazer com o material.
**Como aplicar:** nenhuma licença entra em `references.json` sem ter sido lida na própria
página, item a item. Verificação rápida e reprodutível:
`curl -sSL <url> | grep -o 'creativecommons.org/licenses/[a-z-]*/[0-9.]*'` (o OpenStax
embute o bloco `"license":{...}` no HTML). Divergência entre o que se lembrava e o que a
página diz → vale a página.
