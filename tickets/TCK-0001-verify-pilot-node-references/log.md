# Log — TCK-0001

> Auditoria append-only. Formatos em `docs/ai/ticket-protocol.md`.
> Corrigir registro anterior = nova entrada `CORRECTION`, nunca edição.

## [001] ACTION — 2026-08-01 — setup do repositório
- Ação: ticket criado ao final do bootstrap da superfície de IA, registrando pendência
  identificada durante a criação do nó piloto `high-school/algebra/quadratic-equations`.
- Motivo: as referências do nó foram registradas sem verificação de URL e licença na
  própria página da fonte, contrariando AGENTS.md §9.6.
- Resultado: ok — status `new`, owner `tech-lead`. Aguarda triagem.

## [002] ACTION — 2026-08-01 — tech-lead
- Ação: triagem executada. Classificação `content`, tamanho **P**, prioridade mantida em
  **P2**, owner definido como `researcher`. Status `new` → `triaged`.
- Motivo: os 5 critérios de aceite já são verificáveis (URL responde, licença confere,
  `covers` confere, referência pt-BR presente, `audit-content.sh` verde) — não é preciso
  passar pelo `product-analyst`. O trabalho é de fonte externa, licença e idioma: escopo
  exclusivo do `researcher`. Verificado nesta triagem que há acesso à rede no ambiente
  (`curl` na primeira URL do `references.json` retornou HTTP 200), logo o critério 1 é
  executável hoje e o ticket **não** é `blocked`.
- Aderência ao plano: pertence à **Fase 1** do `docs/product/roadmap.md` ("validar
  `references.json` contra a realidade"; `audit-content.sh` verde). Não depende do
  `ADR-0003` — o contrato de `content/` é independente da stack (ADR-0003, seção Impacto).
- Requisitos transversais checados: bilinguismo (critério 4 exige fonte pt-BR — L-001 vale
  também para o acervo de referências); custo zero (só fontes gratuitas, licença registrada);
  a11y/offline/privacidade não aplicáveis; slugs do nó não são tocados (L-003).
- Plano de execução (6 passos):
  1. `researcher`: acessar cada URL de `references.json`, confirmar que a página é a obra
     esperada e registrar o status HTTP e a data da consulta.
  2. `researcher`: conferir a licença **na própria página** da fonte (OpenStax declara a
     licença no rodapé/página de direitos) e corrigir o campo `license` se divergir.
  3. `researcher`: conferir `covers` contra o sumário real do material; reescrever o que
     estiver impreciso.
  4. `researcher`: `/research-sweep` para achar ao menos uma fonte gratuita em **pt-BR**
     (candidatos a investigar: acervos públicos brasileiros com licença explícita) e
     adicioná-la com autor, ano, URL, idioma e licença.
  5. `researcher`: rodar `bash scripts/audit-content.sh` e anexar a saída.
  6. Cadeia de revisão: `code-reviewer` (diff de `references.json`, licenças e formato) →
     `qa-validator` (critérios 1–5 com evidência; único que marca `done`).
- Restrições: não alterar teoria, exercícios nem `meta.json` do nó; o nó permanece
  `status: "draft"` (sair de draft depende também de `math-reviewer` e `i18n-steward`, fora
  do escopo deste ticket); nenhuma fonte sem licença explícita entra no arquivo.
- Resultado: ok — `triaged`. **HANDOFF ainda não registrado**: pelo protocolo, handoff
  significa execução imediata (`docs/ai/ticket-protocol.md`, regra 1) e o pedido em curso do
  usuário era diagnóstico do backlog, não execução. Para acionar: `/ticket-loop TCK-0001`.


## [003] HANDOFF — 2026-08-01 12:28
- De: tech-lead → Para: researcher
- Status novo: in_progress
- O que foi feito: usuário autorizou a execução ("faça tudo que for necessário"); o
  `/ticket-loop` foi acionado sobre a triagem registrada em [002].
- Artefatos: nenhum ainda — plano de 6 passos em [002].
- Como validar: `bash scripts/audit-content.sh` ao final; URLs conferidas com evidência de
  status HTTP e licença lida na própria página.
- Pendências e riscos: fonte gratuita em pt-BR com licença explícita é o item mais incerto;
  se nenhuma for encontrada com licença clara, registrar o impasse em vez de inventar.
- Critérios de aceite: [ ] 1–5 restantes.

## [004] ACTION — 2026-08-01 12:40 — researcher
- Ação: executados os passos 1–5 do plano de [002] sobre
  `content/high-school/algebra/quadratic-equations/references.json`. Data de consulta de
  todas as fontes: **2026-08-01**.
- Motivo: cumprir AGENTS.md §9.6 (URL, licença e cobertura verificadas na própria página).
- Resultado: ok — arquivo passou de 2 para 3 itens; duas licenças corrigidas.

  **Item 1 — OpenStax, Algebra and Trigonometry 2e §2.5**
  - URL `https://openstax.org/books/algebra-and-trigonometry-2e/pages/2-5-quadratic-equations`
    → `HTTP 200`, 0 redirecionamentos; página é de fato a seção 2.5 do livro (título
    `2.5 Quadratic Equations` no HTML).
  - Lido na página: objetivos "Solve quadratic equations by factoring / by the square root
    property / by completing the square / by using the quadratic formula" e as subseções
    Zero-Product Property, Square Root Property, Completing the Square, Quadratic Formula,
    The Discriminant, Using the Pythagorean Theorem, `2.5 Section Exercises`.
    `"publish_date":"2021-12-21"` → ano 2021 confirmado.
  - **Licença CORRIGIDA**: estava `CC BY 4.0`; a página declara
    `"license":{"url":"http://creativecommons.org/licenses/by-nc-sa/4.0/","name":"Creative
    Commons Attribution-NonCommercial-ShareAlike License"}` e o rodapé repete
    "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY NC-SA) license".
    Registrado `CC BY-NC-SA 4.0`.
  - `covers` reescrito: faltavam a propriedade da raiz quadrada e as aplicações do teorema
    de Pitágoras.

  **Item 2 — OpenStax, Intermediate Algebra 2e §9.3**
  - URL `https://openstax.org/books/intermediate-algebra-2e/pages/9-3-solve-quadratic-equations-using-the-quadratic-formula`
    → `HTTP 200`, 0 redirecionamentos; título `9.3 Solve Quadratic Equations Using the
    Quadratic Formula`. `"publish_date":"2020-05-06"` → ano 2020 confirmado.
  - Lido na página: dedução explícita ("we will derive and use a formula…", completamento
    de quadrado sobre a forma padrão), objetivos "Solve quadratic equations using the
    Quadratic Formula / Use the discriminant to predict the number and type of solutions /
    Identify the most appropriate method to use to solve a quadratic equation" e
    `Section 9.3 Exercises`.
  - **Licença CORRIGIDA**: estava `CC BY 4.0`; a página declara o mesmo bloco
    `by-nc-sa/4.0` → registrado `CC BY-NC-SA 4.0`.
  - `covers` reescrito: incluídos "tipo" das soluções (não só número) e a escolha do método.

  **Item 3 — NOVO, pt-BR: Livro Aberto de Matemática (IMPA/OBMEP), cap. "Função Quadrática"**
  - URL `https://github.com/livro-aberto/tex-design-development/blob/master/Capítulos%20prontos%20-%20Aluno/Função%20Quadrática.pdf`
    → `HTTP 200`; PDF de 85 páginas baixado e inspecionado (colofão + texto).
  - Autoria/ano lidos no colofão do próprio PDF: autores Luiz Amorim e Bruno Vianna
    (Colégio Pedro II), revisão Cydara Ripoll e Letícia Rangel, coordenação Fabio Simas e
    Augusto Teixeira, editora IMPA-OS, realização OBMEP, "2021 / versão 1.1 de 26 de julho
    de 2021".
  - Licença: a página oficial do projeto (`https://livroaberto.uniriotec.br/sobre/`,
    `HTTP 200`) declara textualmente "O projeto Livro Aberto de Matemática adotou uma
    licença Creative Commons do tipo BY-NC-SA (…) usos para fins educacionais são
    permitidos gratuitamente". **Divergência registrada:** o selo no colofão do PDF exibe
    apenas os ícones CC + BY + SA (sem NC). Adotada a leitura **mais restritiva**
    (`CC BY-NC-SA`), com a divergência escrita no próprio campo `license`. A versão da
    licença não é declarada em nenhum dos dois lugares — não foi inventada.
  - Cobertura conferida no PDF: é capítulo sobre a *função* quadrática; a parte útil para
    este nó está em "Organizando: interseção com os eixos coordenados" (p. 47-49), com a
    fórmula resolutiva, Δ = b² − 4ac e os três casos de sinal de Δ. Isso está dito
    explicitamente em `covers`, conforme a instrução de preferir licença clara mesmo com
    cobertura mais ampla.
  - Candidatas **descartadas** (evidência): Portal da Matemática OBMEP
    (`portaldaobmep.impa.br`, HTTP 200, **sem** qualquer declaração de licença no rodapé);
    `umlivroaberto.com` (certificado SSL expirado, não acessível); PhET pt_BR e M³/Unicamp
    (páginas 100% renderizadas por JS — licença não legível na página, só "Alguns direitos
    reservados"); Khan Academy pt-BR (TOS renderizado por JS e artigo de suporte com
    `HTTP 403` — licença não verificável hoje); Wikilivros
    "Matemática elementar/Equações algébricas" (licença CC BY-SA 4.0 confirmada via
    `siteinfo/rightsinfo`, mas a lista de exercícios traz **gabaritos errados** — p. ex.
    `9x² + 6x + 1 = 0` marcado como "x ∉ ℝ" quando Δ = 0 e x = −1/3; e `−4x² − 4x − 1 = 0`
    com resposta "0,5" no lugar de −0,5 — incompatível com o pilar de correção matemática).

  **Passo 5 — auditoria**
  ```
  $ bash scripts/audit-content.sh
  Resumo: 1 nós · 0 erros · 0 avisos
  exit=0
  ```
- Lição: n/a — não houve REJECT; a lição de interesse geral (licença OpenStax varia por
  livro: CC BY 4.0 **ou** CC BY-NC-SA 4.0) foi registrada em `memory/lessons/`.

## [005] HANDOFF — 2026-08-01 12:42
- De: researcher → Para: code-reviewer
- Status novo: in_review
- O que foi feito: as 2 URLs OpenStax foram acessadas (HTTP 200, sem redirecionamento) e
  conferidas contra o sumário real da seção; as duas licenças estavam **erradas**
  (`CC BY 4.0` → `CC BY-NC-SA 4.0`, lido no rodapé de cada página); os dois `covers` foram
  reescritos; foi acrescentada uma terceira referência, gratuita e em **pt-BR** (Livro
  Aberto de Matemática, IMPA/OBMEP, 2021), com licença CC BY-NC-SA verificada na página
  oficial do projeto e autoria lida no colofão do PDF.
- Artefatos: `content/high-school/algebra/quadratic-equations/references.json` (único
  arquivo alterado; teoria, exercícios e `meta.json` intocados — nó segue `draft`).
  Sem commit (o orquestrador commita).
- Como validar:
  1. `bash scripts/audit-content.sh` → esperado `1 nós · 0 erros · 0 avisos`.
  2. `curl -sSI -o /dev/null -w "%{http_code}\n" -L <url>` para cada um dos 3 itens → 200.
  3. Licença OpenStax: `curl -sSL <url> | grep -o 'creativecommons.org/licenses/[a-z-]*/[0-9.]*'`
     → `creativecommons.org/licenses/by-nc-sa/4.0`.
  4. Licença pt-BR: abrir `https://livroaberto.uniriotec.br/sobre/` (frase "licença Creative
     Commons do tipo BY-NC-SA") e a p. 3 do PDF (colofão com autoria, ano e selo CC).
- Pendências e riscos:
  1. **Impacto da correção de licença**: CC BY-NC-SA proíbe uso comercial e exige
     share-alike. Se algum dia se adaptar texto do OpenStax, a obra derivada herda NC-SA —
     e a plataforma precisa ser não comercial. Sugiro que o `tech-lead` avalie se isso
     merece ADR. Fora do escopo deste ticket.
  2. A licença do Livro Aberto **não tem versão declarada** e há divergência entre site
     (BY-NC-SA) e selo do PDF (BY-SA); adotei a leitura mais restritiva e deixei isso
     escrito no campo `license`. Se o `code-reviewer` preferir texto mais curto no campo,
     é ajuste de forma.
  3. A URL pt-BR aponta para um PDF no GitHub do projeto porque o link oficial do capítulo
     (Overleaf) responde `HTTP 403` e `umlivroaberto.com` está com certificado expirado.
     Risco de o caminho no repositório mudar (branch `master`).
  4. Nenhuma referência pt-BR *exclusivamente* sobre equações do 2º grau com licença
     explícita foi encontrada — o acervo aberto brasileiro é escasso (ver candidatas
     descartadas em [004]).
- Critérios de aceite:
  - [x] 1. Cada URL acessada, HTTP 200, página é a obra/seção esperada (evidência em [004]).
  - [x] 2. Licença corresponde à declarada na própria página — duas divergências corrigidas.
  - [x] 3. `covers` reescrito conforme o sumário real de cada fonte.
  - [x] 4. Referência gratuita em pt-BR adicionada com autor, ano, URL, idioma e licença.
  - [x] 5. `bash scripts/audit-content.sh` sem erros (`1 nós · 0 erros · 0 avisos`).

## [006] HANDOFF — 2026-08-01 12:58
- De: code-reviewer → Para: qa-validator
- Status novo: in_validation
- O que foi feito: revisão independente do diff (nenhum artefato deste ticket foi produzido
  por este agente). **Todas as afirmações de licença de [004] foram reverificadas na fonte**,
  não aceitas do log. Resultado: **APROVADO**, 0 defeitos bloqueantes, 3 sugestões
  não bloqueantes registradas abaixo.
- Artefatos revisados: `content/high-school/algebra/quadratic-equations/references.json`
  (2 → 3 itens), `memory/lessons/openstax-license-varies-by-book.md` (L-006),
  `memory/lessons/license-must-be-readable-without-javascript.md` (L-007),
  `memory/LESSONS.md`, `memory/MEMORY.md`, `memory/agents/researcher.md`.
- Como validar (comandos executados nesta revisão e saída resumida):
  1. Licença OpenStax (item 1 e 2), lida na própria página, não do log:
     `curl -sSL <url> | grep -o '"license":{[^}]*}'` →
     `{"url":"http://creativecommons.org/licenses/by-nc-sa/4.0/","name":"Creative Commons
     Attribution-NonCommercial-ShareAlike License"}` nas **duas** URLs.
     Confirma a correção `CC BY 4.0` → `CC BY-NC-SA 4.0` (critério 2).
  2. URLs (critério 1): `curl -sS -o /dev/null -L -w "%{http_code} %{num_redirects}"` →
     `200 0` nos 3 itens; `<title>` bate com a obra:
     `2.5 Quadratic Equations - Algebra and Trigonometry 2e | OpenStax`;
     `9.3 Solve Quadratic Equations Using the Quadratic Formula - Intermediate Algebra 2e`;
     `tex-design-development/Capítulos prontos - Aluno/Função Quadrática.pdf at master`.
     Anos conferidos no HTML: `"publish_date":"2021-12-21"` e `"publish_date":"2020-05-06"`
     → 2021 e 2020, como registrado.
  3. `covers` (critério 3) conferido por ocorrência no HTML: item 1 tem
     `Square Root Property`, `Zero-Product`, `Completing the Square`, `The Discriminant`,
     `Pythagorean`, `Section Exercises`; item 2 tem `derive and use`,
     `number and type of solutions`, `most appropriate method`, `Section 9.3 Exercises`.
  4. Fonte pt-BR (critério 4): PDF baixado do raw do GitHub (`pdfinfo` → 85 páginas,
     `CreationDate: Tue Jul 27 12:24:39 2021`). Colofão extraído com `pdftotext -f 3 -l 3`
     confirma título, "2021 / versão 1.1 de 26 de julho de 2021", editora IMPA-OS,
     realização OBMEP, produção Associação Livro Aberto, coordenação Fabio Simas e Augusto
     Teixeira, autores Luiz Amorim e Bruno Vianna (Colégio Pedro II).
     **Divergência de licença confirmada como real:** `curl` em
     `https://livroaberto.uniriotec.br/sobre/` (HTTP 200, HTML estático) devolve em texto
     puro "adotou uma licença Creative Commons do tipo BY-NC-SA (…) não são permitidos usos
     comerciais"; o selo do colofão, renderizado com `pdftoppm -f 3 -l 3 -png` e lido como
     imagem, mostra **CC + BY + SA, sem NC**. A leitura mais restritiva adotada pelo
     `researcher` está correta e a divergência está declarada no campo `license`.
     Cobertura conferida: a seção "ORGANIZANDO INTERSEÇÃO COM OS EIXOS COORDENADOS" está nas
     páginas impressas **47, 48 e 49** (páginas 51-53 do PDF), com a fórmula resolutiva,
     `∆ = b2 − 4ac`, os Casos 1/2/3 do sinal de ∆ e a observação de que o nome "fórmula de
     Báskara" é atribuição equivocada no Brasil — exatamente o que `covers` afirma.
  5. Critério 5: `bash scripts/audit-content.sh` → `Resumo: 1 nós · 0 erros · 0 avisos`,
     `exit=0`.
  6. Formato e escopo: JSON válido (`json.load` ok); os 3 itens têm exatamente o mesmo
     conjunto de chaves (`author, covers, language, license, title, url, year`);
     `git diff --stat -- content/` mostra **um único arquivo** alterado (`references.json`),
     logo teoria, exercícios e `meta.json` estão intactos e o nó segue `status: "draft"`.
  7. Lições: L-006 e L-007 seguem o formato de `memory/lessons/README.md`
     (`Tipo/ID/Contexto/Lição/Como aplicar`); `grep '^\*\*ID:\*\*' memory/lessons/` mostra
     L-001…L-008 sem colisão; L-006 (`correção`) está na seção "Correção" e L-007
     (`sucesso`) na seção "Sucesso" de `memory/LESSONS.md`; ambas indexadas em `MEMORY.md`.
- Licença NC × licença do projeto (verificação específica desta revisão): a decisão de
  2026-08-01 (conteúdo CC BY-SA 4.0 · código MIT, TCK-0004) **não é violada**. As três
  fontes NC/NC-SA aparecem apenas como leitura externa em `references.json`; não há no nó
  nenhum sinal de adaptação de material NC — `grep -ri 'openstax|adaptado|based on'` no nó
  só encontra ocorrências dentro do próprio `references.json`, a teoria segue o template do
  projeto (objetivo → pré-requisitos → intuição → definição formal → exemplos → erros
  comuns → resumo) e os 5 exercícios são autorais. Citar fonte NC é permitido; incorporar
  não. **Sem defeito.**
- Sugestões (NÃO bloqueiam a validação; decidir no ticket de licença ou em follow-up):
  1. `references.json:28` — o campo `license` do item 3 mistura identificador e nota longa
     ("CC BY-NC-SA (versão não declarada; leitura mais restritiva — …)"). Como
     `audit-content.sh` só checa presença, isso passa hoje, mas o campo deixa de ser
     legível por máquina. Sugiro `license` = `"CC BY-NC-SA"` e mover a divergência para um
     campo próprio (ex.: `licenseNotes`) quando o schema de `references.json` for definido.
  2. `references.json:11,20,29` — `covers` carrega rastro de auditoria ("Verificado em
     2026-08-01; licença lida no rodapé…"). `covers` tende a ser texto exibido ao aluno;
     a proveniência da verificação cabe melhor no log do ticket (onde já está).
  3. `references.json:26` — a URL pt-BR aponta para `blob/master/…`, que se move com a
     branch. Confirmei que as alternativas oficiais estão fora do ar
     (`umlivroaberto.org/BookCloud/…` → HTTP 403; `umlivroaberto.com` → certificado SSL
     expirado), então a escolha é justificada; ainda assim, um permalink por SHA de commit
     do GitHub seria mais estável.
- Pendências e riscos: as 4 pendências de [005] continuam válidas e são de escopo maior que
  este ticket; a de nº 1 (impacto de CC BY-NC-SA) está coberta pelo TCK-0004.
- Critérios de aceite (visão do review; a decisão de `done` é do `qa-validator`):
  - [x] 1. 3 URLs → HTTP 200, 0 redirecionamentos, título/obra conferidos.
  - [x] 2. Licenças reverificadas na fonte por este revisor; correção para CC BY-NC-SA 4.0
        procede; divergência da fonte pt-BR é real e está declarada.
  - [x] 3. `covers` conferido item a item contra o material.
  - [x] 4. Fonte pt-BR gratuita com autor, ano, URL, idioma e licença (colofão conferido).
  - [x] 5. `audit-content.sh` → 1 nós · 0 erros · 0 avisos.

## [007] HANDOFF — 2026-08-01 13:10
- De: qa-validator → Para: tech-lead
- Status novo: done
- O que foi feito: validação independente dos critérios 1–5. Nenhuma evidência foi copiada
  de [004] (produtor `researcher`) ou de [006] (revisor `code-reviewer`) — **todos os
  comandos abaixo foram reexecutados por este agente**, inclusive o download do PDF pt-BR e
  a renderização do selo de licença. Resultado: **APROVADO**, 5/5 critérios com evidência,
  0 defeitos. 3 dívidas aceitas (não bloqueiam) registradas ao final.
- Ambiente da validação: commit `d1ca2e5` (working tree sujo — o artefato deste ticket está
  em `git status` como ` M content/high-school/algebra/quadratic-equations/references.json`,
  sem commit, conforme [005]); `curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0`;
  `pdftotext`/`pdfinfo`/`pdftoppm` (poppler) disponíveis; sem navegador — o artefato é um
  arquivo de dados, não há UI a exercitar neste ticket (ver "Casos hostis" abaixo).

### Evidência por critério

**Critério 1 — cada URL acessada, página esperada, sem 404 nem redirecionamento** ✓
```
$ curl -sS -o page$i.html -L -w "http_code=%{http_code} num_redirects=%{num_redirects} final_url=%{url_effective}\n" <url>
item 1  http_code=200 num_redirects=0 final_url=https://openstax.org/books/algebra-and-trigonometry-2e/pages/2-5-quadratic-equations
item 2  http_code=200 num_redirects=0 final_url=https://openstax.org/books/intermediate-algebra-2e/pages/9-3-solve-quadratic-equations-using-the-quadratic-formula
item 3  http_code=200 num_redirects=0 final_url=https://github.com/livro-aberto/tex-design-development/blob/master/Cap%C3%ADtulos%20prontos%20-%20Aluno/Fun%C3%A7%C3%A3o%20Quadr%C3%A1tica.pdf
$ grep -o '<title>[^<]*</title>' page$i.html
item 1  2.5 Quadratic Equations - Algebra and Trigonometry 2e | OpenStax
item 2  9.3 Solve Quadratic Equations Using the Quadratic Formula - Intermediate Algebra 2e | OpenStax
item 3  tex-design-development/Capítulos prontos - Aluno/Função Quadrática.pdf at master · livro-aberto/…
```
`num_redirects=0` nos três: nenhuma URL cai em outra obra. Título de cada página bate com o
campo `title` do JSON. Ano conferido na própria página: `"publish_date":"2021-12-21"`
(item 1 → `year: 2021`) e `"publish_date":"2020-05-06"` (item 2 → `year: 2020`).

**Critério 2 — licença registrada = licença declarada na própria página** ✓
```
$ grep -o '"license":{[^}]*}' page1.html ; grep -o '"license":{[^}]*}' page2.html
{"url":"http://creativecommons.org/licenses/by-nc-sa/4.0/","name":"Creative Commons Attribution-NonCommercial-ShareAlike License"}   (idêntico nos dois)
$ grep -o 'creativecommons.org/licenses/[a-z-]*/[0-9.]*' page1.html page2.html | sort -u
creativecommons.org/licenses/by-nc-sa/4.0
```
Confere com `"license": "CC BY-NC-SA 4.0"` nos itens 1 e 2 — a correção de `CC BY 4.0`
feita em [004] procede, e reverifiquei na fonte, não no log.

Item 3 (pt-BR), as **duas** declarações conferidas por mim:
```
$ curl -sSL https://livroaberto.uniriotec.br/sobre/   (HTTP 200, HTML estático)
"O projeto Livro Aberto de Matemática adotou uma licença Creative Commons do tipo BY-NC-SA,
 ou seja, todo uso que for feito do material deve mencionar os autores, não são permitidos
 usos comerciais e todo material derivado também deve adotar licença equivalente."
$ grep -o -E 'BY-NC-SA[^<]{0,30}|creativecommons\.org/licenses/[a-z./-]*' sobre.html | sort -u
BY-NC-SA, ou seja, todo uso que for fe        ← nenhuma URL canônica, nenhuma versão declarada
$ pdftoppm -f 3 -l 3 -r 130 -png funcao-quadratica.pdf colofao   (selo lido como imagem)
selo do colofão = CC + BY + SA — sem o ícone NC.
```
**Divergência confirmada como real por mim** (não aceita do log): site diz BY-NC-SA, selo do
PDF diz BY-SA. A leitura mais restritiva adotada está correta (L-007) e a divergência está
declarada no próprio campo `license`. A ausência de versão ("4.0") também é real — não foi
inventada. Sem defeito.

**Critério 3 — `covers` descreve o que a fonte realmente cobre** ✓
Cada alegação de cobertura foi conferida por ocorrência no material, não por leitura do log:
```
$ grep -o -i "<termo>" page1.txt | wc -l      (texto extraído do HTML, tags removidas)
Zero-Product Property 11 · Square Root Property 18 · Completing the Square 11 ·
Quadratic Formula 20 · Discriminant 11 · Pythagorean 5 · Section Exercises 1 ·
"nature of the solutions" 4
$ grep -o -E 'Solve quadratic equations by [a-z ]{3,40}' page1.txt | sort -u
… by completing the square / by factoring / by the square root property / by using the quadratic formula
$ grep -o -i "<termo>" page2.txt | wc -l
derive 2 · completing the square 8 · standard form 20 · discriminant 17 ·
"number and type of solutions" 8 · "most appropriate method" 11 · "Section 9.3 Exercises" 1 · complex 7
$ grep -o -E 'Use the discriminant to [a-z ]{3,50}|Identify the most appropriate [a-z ]{3,60}' page2.txt
Use the discriminant to predict the number and type of solutions of a quad…
Identify the most appropriate method to use to solve a quadratic equation
```
Item 3, conferido no PDF (localização feita por varredura página a página, não pelo log):
```
$ for p in $(seq 1 85); do pdftotext -f $p -l $p … | grep -qi 'EIXOS COORDENADOS' && echo $p; done
PDFpage=51 -> ORGANIZANDO INTERSEÇÃO COM OS EIXOS COORDENADOS
$ pdftotext -f 51 -l 53 funcao-quadratica.pdf -
… números impressos 47, 48 e 49 no rodapé das três páginas (bate com "p. 47-49" do covers);
"a mais comum utilizando a fórmula quadrática, conhecida no Brasil erroneamente por fórmula
 de Báskara: x = (−b ± √∆)/2a", "onde ∆ = b2 − 4ac", "Caso 1 Para ∆ > 0", "Caso 2 Para ∆ = 0",
 "Caso 3 Para ∆ < 0".
$ pdftotext funcao-quadratica.pdf full.txt ; grep -o -i "<termo>" full.txt | wc -l
queda livre 3 · forma canônica 25 · máximo 32 · mínimo 29 · parábola 91
```
Confirma também a ressalva de escopo do `covers` ("cobertura mais ampla que o nó"): o
capítulo é sobre a *função* quadrática, e a parte útil ao nó é a seção citada. **Nenhuma
alegação de cobertura falsa ou não encontrada nos três itens.**

**Critério 4 — ao menos uma referência gratuita em português, com autor, ano, URL, idioma e
licença** ✓
```
$ curl -sSL -o funcao-quadratica.pdf <raw.githubusercontent…>  → raw_http=200 size=4265038
   (download anônimo, sem login, sem paywall)
$ file funcao-quadratica.pdf → PDF document, version 1.7, 85 page(s)
$ pdfinfo → Pages: 85 · CreationDate: Tue Jul 27 12:24:39 2021 -03
$ pdftotext -f 3 -l 3 funcao-quadratica.pdf -    (colofão, lido por mim)
Título: Função Quadrática · Ano/Versão: 2021 / versão 1.1 de 26 de julho de 2021 ·
Editora: IMPA-OS · Realização: OBMEP · Produção: Associação Livro Aberto ·
Coordenação: Fabio Simas e Augusto Teixeira · Autores: Luiz Amorim e Bruno Vianna (Colégio Pedro II)
```
Os cinco campos exigidos estão preenchidos e conferem com o colofão/site. Gratuidade
verificada por download anônimo **e** pela frase do site ("usos para fins educacionais são
permitidos gratuitamente").

**Critério 5 — `bash scripts/audit-content.sh` continua sem erros** ✓
```
$ bash scripts/audit-content.sh
Resumo: 1 nós · 0 erros · 0 avisos
exit=0
```
Nota de honestidade sobre o alcance deste critério: li `scripts/audit-content.py:264-283` —
`check_references` só valida **presença** de `author/year/url/language/license`; não valida
`covers`, não faz requisição de rede e não checa formato de licença. Ou seja, o critério 5
é necessário, não suficiente; a cobertura real de URL/licença vem dos critérios 1–3 acima.

### Requisitos transversais
- **Bilinguismo** ✓ — `Counter(item['language']) → {'en-US': 2, 'pt-BR': 1}`; os dois idiomas
  do produto estão cobertos no acervo do nó, e o item pt-BR não é fallback nem tradução
  automática (é obra brasileira nativa).
- **Custo zero** ✓ — as três fontes foram baixadas anonimamente com HTTP 200, sem login,
  sem paywall; as três têm licença aberta registrada.
- **Escopo preservado** ✓ — `git diff --stat -- content/` →
  `.../quadratic-equations/references.json | 25 +++++--- , 1 file changed`: teoria,
  exercícios e `meta.json` intocados; o nó segue `status: "draft"`, como manda o ticket.
- **Formato** ✓ — `json.load` ok; os 3 itens têm exatamente o mesmo conjunto de chaves
  (`author, covers, language, license, title, url, year`).
- **Casos hostis** — não aplicáveis a este ticket e registrado o porquê: o artefato é um
  arquivo de dados de conteúdo, não há UI, rota ou estado de aplicação a exercitar (a stack
  segue indefinida, `ADR-0003` em `proposed`) e nenhum código consome `references.json` hoje
  (`grep -rn "references.json" --include='*.py' --include='*.sh' --include='*.js'
  --include='*.ts'` só encontra menções em documentação e no próprio audit). Offline, tema,
  zoom, teclado e leitor de tela entram quando houver tela que renderize estas referências —
  deve ser critério do ticket que criar essa tela, não deste.
- **Lições** — nenhuma lição registrada foi violada: L-001 (bilinguismo) atendida, L-003
  (slugs intocados) atendida, L-006/L-007 foram *geradas* por este trabalho e aplicadas
  corretamente. Sem defeito bloqueante por reincidência.

### Ponto de julgamento (decisão do QA sobre as 3 sugestões de [006])

Nenhuma das três reprova. Argumento item a item:

1. **Rastro de auditoria dentro de `covers` (toca o critério 3) → DÍVIDA, não defeito.**
   O critério 3 pergunta se `covers` *descreve o que a fonte realmente cobre*; conferi
   alegação por alegação e **todas são verdadeiras** — não há descrição falsa, faltante ou
   inflada. O rastro ("Verificado em 2026-08-01; licença lida no rodapé…") é texto
   *adicional* e também verdadeiro. Além disso, não existe contrato que ele viole: `covers`
   **não** é campo exigido pelo audit (`audit-content.py:280` só cobra
   `author/year/url/language/license`), **não** tem schema em `docs/content/` (`grep -rn
   '"covers"' docs/ scripts/` → 0 resultados) e **não** tem consumidor no repositório. A
   premissa "é exibido ao aluno" é hipótese sobre uma UI que ainda não existe. Reprovar aqui
   seria inventar critério depois da entrega — mudança de critério é decisão do `tech-lead`,
   não minha.
   **Mas a dívida é real e tem um ponto mais afiado do que o levantado pelo review:** o
   `covers` do item 1 não só carrega proveniência, ele **reafirma a licença** ("uso comercial
   vedado e derivados sob a mesma licença"), duplicando o campo `license`. São duas fontes de
   verdade para o mesmo fato: se a licença do OpenStax mudar ou for corrigida, o `covers`
   envelhece em silêncio — exatamente a classe de erro que originou este ticket. Registrado
   como dívida D-1.
2. **Nota longa dentro do campo `license` (item 3) → DÍVIDA, não defeito.** O critério 2 pede
   correspondência com a licença declarada na fonte, e a correspondência existe e está
   honesta — inclusive a divergência, que eu confirmei ser real. Perder legibilidade por
   máquina só vira problema quando houver schema/parser, que não há. Registrado como D-2.
3. **URL em `blob/master/` → DÍVIDA, não defeito.** O critério 1 é sobre o estado de hoje:
   `200`, `num_redirects=0`, título correto. Verifiquei por conta própria que as
   alternativas oficiais continuam fora do ar — `umlivroaberto.org/BookCloud/…/AF107.html`
   → `403`; `umlivroaberto.com` → `000` (falha de conexão/TLS); só
   `livroaberto.uniriotec.br` → `200`. A escolha do PDF no GitHub é a melhor disponível.
   Registrado como D-3.

### Dívidas aceitas (não bloqueiam `done`; sugestão de ticket novo)
- **D-1** — `references.json`: `covers` dos 3 itens carrega rastro de auditoria e, no item 1,
  duplica a informação de licença. Mover proveniência para o log e deixar `covers` só com
  cobertura.
- **D-2** — `license` do item 3 mistura identificador e nota; separar em `license` +
  `licenseNotes` quando houver schema.
- **D-3** — URL pt-BR em `blob/master/` se move com a branch; trocar por permalink com SHA de
  commit e reconferir periodicamente.
- **ACTION sugerida ao `tech-lead`:** as três se resolvem de uma vez em **um ticket de schema
  para `references.json`** (campos obrigatórios, `covers` sem proveniência, `licenseNotes`,
  política de permalink) + a validação correspondente em `audit-content.py`. Fora do escopo
  deste ticket, que era verificar as fontes, não definir o contrato do arquivo.

### Critérios de aceite — veredito final
- [x] 1. 3 URLs → HTTP 200, 0 redirecionamentos, título/obra/ano conferidos na própria página.
- [x] 2. Licenças reverificadas na fonte por este validador; `CC BY-NC-SA 4.0` procede nos
      itens 1 e 2; divergência do item 3 confirmada real e declarada no campo.
- [x] 3. Toda alegação de `covers` conferida no material (HTML e PDF); nenhuma falsa.
- [x] 4. Fonte pt-BR gratuita adicionada, com autor, ano, URL, idioma e licença conferidos no
      colofão e na página oficial.
- [x] 5. `bash scripts/audit-content.sh` → `1 nós · 0 erros · 0 avisos`, `exit=0`.
- Sem commit e sem push (não solicitados pelo usuário).
