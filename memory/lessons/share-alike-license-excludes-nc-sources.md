**Tipo:** sucesso
**ID:** L-009
**Contexto:** TCK-0004, 2026-08-01. Ao registrar o `ADR-0005` (conteúdo sob CC BY-SA 4.0,
código sob MIT), a consequência que mais muda o trabalho não foi a de saída (o que terceiros
podem fazer com o acervo), e sim a de **entrada**: a licença que escolhemos define o filtro de
quais fontes externas podem virar matéria-prima. Como CC BY-SA 4.0 não admite cláusula
não-comercial, as três referências já registradas no nó piloto (OpenStax ×2 e *Livro Aberto de
Matemática*, todas CC BY-NC-SA — ver L-006) passaram, no mesmo dia, de "melhores fontes
encontradas" a "apenas leitura externa".
**Lição:** licença do projeto é regra de produção, não item burocrático de rodapé. Uma licença
share-alike sem NC é **incompatível com fontes NC**: incorporar material NC obrigaria o
derivado a ser NC, contradizendo o que declaramos. E regra normativa que mora só no ADR não é
aplicada — ela precisa aparecer onde o praticante já lê (padrão de conteúdo + checklist de
publicação + memória operacional da área).
**Como aplicar:** antes de usar uma fonte, rodar duas perguntas nesta ordem — (1) permite
derivados? (2) tem cláusula NC? Só CC BY, CC BY-SA, CC0 e domínio público podem ser adaptados,
com atribuição, e o derivado sai sob CC BY-SA 4.0. Tudo com **NC** ou **ND**, e tudo sem
licença declarada, é **citação apenas**: link, autor, ano, idioma e licença em
`references.json`, sem copiar nem traduzir trecho, exemplo, figura ou sequência didática.
Mnemônico: **"NC = leitura, não matéria-prima"**. Árvore de decisão em
`docs/content/content-standards.md`; escopo e atribuição em `LICENSE-CONTENT`. Ao escrever ADR
de licença, incluir sempre a tabela das fontes **reais** já no repositório — hipótese não
resolve dúvida de ninguém.

**Adendo de 2026-08-01 (REJECT B1 do TCK-0004, loop 1/3).** A primeira entrega desta lição a
violou: a regra ficou no ADR, no padrão de conteúdo e na memória, mas **não** nas fontes que as
12 ferramentas carregam sozinhas — `AGENTS.md` ainda dizia "preferência por CC BY" e
`.github/instructions/content.instructions.md` (`applyTo: content/**`) nem mencionava
compatibilidade. Regra normativa nova só está propagada quando percorre esta lista:
(1) `AGENTS.md` — fonte única, lida nativamente; (2) `.github/instructions/*.instructions.md`
do escopo afetado **e** `core.instructions.md`; (3) o documento do praticante em `docs/` e o
checklist correspondente; (4) `memory/context/<área>.md`; (5) o agent em `.claude/agents/` que
executa a tarefa; (6) `prompts/bootstrap-session.md` e `CONTRIBUTING.md` quando a regra vale
para quem chega de fora; (7) `python3 scripts/sync-ai-adapters.py` + as duas auditorias. Parar
antes do item 2 é o mesmo defeito que reprovou o `TCK-0003` no mesmo dia.
