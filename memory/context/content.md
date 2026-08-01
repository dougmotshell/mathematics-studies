# Contexto operacional — content

> Documento **vivo**: pegadinhas do ambiente, estado atual e decisões operacionais em vigor
> na área. Lido por todo agente antes de trabalhar; atualizado (com data) ao final de
> qualquer ticket que mude esse conhecimento. Conhecimento generalizável sobre **erros** vai
> para `memory/lessons/`, não para cá.

**Última atualização:** 2026-08-01

## Estado atual

- **TCK-0001 fechado em 2026-08-01 (`done`, validado pelo `qa-validator`):** as 3 referências
  do nó piloto estão **verificadas na fonte** — URL (HTTP 200, sem redirecionamento), licença
  lida na própria página e `covers` conferido no material. O acervo do nó cobre os dois
  idiomas (2 en-US + 1 pt-BR) com custo zero. O nó **continua `draft`**: sair de draft ainda
  depende de `math-reviewer` e `i18n-steward`.
- **TCK-0005 fechado em 2026-08-01 (`done`, validado pelo `qa-validator#3`):** o nó piloto tem
  agora **8/8 fórmulas em display com descrição textual** (`*Leitura:*` / `*Reading:*`) nos dois
  idiomas — era 3/8. Só texto foi acrescentado; o LaTeX é byte a byte o do commit `21f6ef1`.
  O nó **continua `draft`**. Quatro pendências, todas preexistentes e fora do diff,
  **condicionam a saída de `draft`**: (1) hipótese `\Delta \ge 0` ausente do enunciado do
  teorema, do Resumo e da linha de soma e produto (L-014); (2) a descrição preexistente de
  `theory.pt-BR.md:53` / `en-US.md:52` lê só a primeira metade do bloco, deixando
  `\Delta = b^2-4ac` mudo; (3) a tabela "Erros comuns" contrasta duas frações cujo único
  diferencial é o agrupamento, e o contraste some na leitura linear; (4) registrar em
  `docs/content/accessibility.md` a tabela de convenções de leitura de fórmula e, no glossário
  de `docs/content/i18n.md`, `subscrito (índice) | subscript`.
- Um nó piloto criado: `content/high-school/algebra/quadratic-equations` (`status: draft`).
  Ele serve de **referência de formato** para novos nós — teoria bilíngue com as sete seções,
  5 exercícios com feedback diagnóstico, `references.json` com licença.
- `bash scripts/audit-content.sh` passa sem erros nem avisos com esse nó.

## Pegadinhas conhecidas

- **SymPy não está instalado no ambiente** (`ModuleNotFoundError: No module named 'sympy'`).
  Para `/math-verify`, a alternativa usada é verificação aritmética/numérica em Python puro
  (discriminante, raízes, substituição de volta na equação) — suficiente para álgebra
  elementar, insuficiente para identidades simbólicas gerais. Se a verificação simbólica for
  necessária, instalar SymPy antes ou declarar a limitação no relatório.
- **Descrição de fórmula se verifica por ordem, não por contagem** (L-012), e
  `grep -c '^\$\$'` pode contar um fechamento como bloco: cruzar com
  `grep -o '\$\$' <arquivo> | wc -l` (total = 2 × blocos). `scripts/audit-content.sh` **não**
  checa descrição de fórmula — só presença e não-vazio dos `theory.<lang>.md`
  (`check_theory`, `scripts/audit-content.py:149-157`).
- **Verificação numérica não é demonstração**: para afirmações gerais, declarar isso
  explicitamente (lição L-002).

## Decisões operacionais em vigor

- **Convenções de leitura de fórmula em vigor de fato desde o TCK-0005** (decididas na prática
  pelo nó piloto e aprovadas por `a11y-ux-reviewer` e `i18n-steward`, **ainda não escritas em
  `docs/`**): subscrito `x_1` → "x índice 1" / "x subscript 1"; numerador composto → "tudo
  dividido por" / "all divided by"; numerador de um token → "b dividido por a" / "b divided by
  a"; parênteses sempre falados ("abre/fecha" / "open/close"); `\cdot` → "vezes"/"times" e
  justaposição mantida; `\Longrightarrow` → "o que implica" / "which implies"; relação
  encadeada `= 1 > 0` → "igual a um, que é maior que zero"; números por extenso. Copiar do nó
  piloto ao criar nó novo, e ler a **estrutura** na ordem escrita — nunca nomear a fórmula nem
  interpretar.
- Antes de fixar qualquer gabarito, resolver o exercício de forma independente **e**
  substituir a resposta na equação original — a substituição pega quase todo erro de sinal.
- Referências externas só entram em `references.json` com autor, ano, URL, idioma e licença.
  **URL precisa ser verificada de fato** (acesso e licença na própria página) antes de o nó
  sair de `draft` — ver TCK-0001.
- **Licença do conteúdo: CC BY-SA 4.0** (`ADR-0005`, decidida em 2026-08-01; código sob MIT).
  Consequência operacional — **"NC = leitura, não matéria-prima"**: fonte **CC BY**,
  **CC BY-SA**, **CC0** ou de **domínio público** pode ser adaptada (com atribuição; o
  resultado sai sob CC BY-SA 4.0); fonte **CC BY-NC** ou **CC BY-NC-SA** **não** pode ser
  incorporada nem traduzida para dentro de `theory.<lang>.md` / `exercises.json` — só citada
  como leitura externa em `references.json`. Árvore de decisão em
  `docs/content/content-standards.md`.
- **`audit-content.sh` não verifica referência de verdade:** `check_references`
  (`scripts/audit-content.py:264-283`) só checa *presença* de
  `author/year/url/language/license` — não faz requisição de rede, não valida `covers` e não
  valida o formato da licença. Auditoria verde **não** significa fonte verificada; a
  verificação de URL e licença continua sendo trabalho manual do `researcher`, com evidência
  no ticket. Não existe schema de `references.json` em `docs/content/` (2026-08-01).
- **Dívidas abertas no `references.json` do nó piloto** (aceitas em TCK-0001, não bloqueantes;
  sugerido um ticket único de schema + validação): o campo `covers` carrega rastro de
  auditoria e, no item 1, **duplica a informação de licença** (duas fontes de verdade para o
  mesmo fato — envelhece em silêncio); o `license` do item pt-BR mistura identificador e nota
  longa (separar em `license` + `licenseNotes`); a URL pt-BR aponta para `blob/master/` no
  GitHub, que se move com a branch (usar permalink por SHA). As alternativas oficiais do
  Livro Aberto seguem fora do ar: `umlivroaberto.org/BookCloud/…` → HTTP 403 e
  `umlivroaberto.com` → falha de conexão/TLS (reconferido em 2026-08-01).
- **Licença que só existe como imagem:** o selo CC do colofão de um PDF é verificável com
  `pdftoppm -f <p> -l <p> -png` e leitura da imagem. Foi assim que a divergência do *Livro
  Aberto* (site: BY-NC-SA · selo: BY-SA, sem NC) foi confirmada — vale a mais restritiva
  (L-007), com a divergência escrita no campo `license`.
- **Todas as três referências do nó piloto são CC BY-NC-SA** (OpenStax ×2 e *Livro Aberto de
  Matemática*, IMPA/OBMEP — verificadas em 2026-08-01, lições L-006 e L-007). Elas continuam
  válidas como leitura externa; o texto do nó tem de permanecer autoral. Ao buscar fonte para
  um nó novo, contar com esse filtro: boa parte do material didático aberto em pt-BR é NC.
