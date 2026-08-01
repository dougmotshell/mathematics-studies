**Tipo:** correção
**ID:** L-001
**Contexto:** 2026-08-01, definição dos padrões de conteúdo do projeto.

**Lição:** conteúdo bilíngue tratado como "escrever em pt-BR agora e traduzir depois" produz,
na prática, conteúdo permanentemente monolíngue: a tradução nunca chega ao topo da fila, o
material publicado fica inconsistente entre idiomas e a divergência estrutural (seções que só
existem em uma versão) cresce a cada revisão.

**Como aplicar:** todo objeto de aprendizagem nasce nos dois idiomas no mesmo ciclo de
trabalho. Enquanto faltar um idioma, `meta.json` fica com `status: "draft"` e o nó não é
publicado. Revisões posteriores alteram **os dois** arquivos na mesma entrega — `/i18n-parity`
verifica antes de qualquer publicação. Ver [[content-slugs-are-public-urls]].
