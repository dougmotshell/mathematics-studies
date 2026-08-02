# Log — TCK-0010

> Append-only. Formatos em `docs/ai/ticket-protocol.md`.

## [001] ACTION — 2026-08-01 15:55 — tech-lead
- Ação: criação do ticket a partir da pendência 2 do `docs-writer#2` (`TCK-0004/log.md`
  `[009]`, também em `[006]`) e da divergência confirmada de forma independente por
  `researcher` e `qa-validator` no TCK-0001 (`[004]`, `[007]`). Trechos verbatim no ticket.
- Motivo: a divergência é real e verificada duas vezes (página do projeto: BY-NC-SA; selo do
  colofão do PDF: BY-SA, sem NC e sem versão). Enquanto ela existir, vale a leitura mais
  restritiva e o projeto segue **sem nenhuma** fonte pt-BR adaptável.
- Resultado: ok — `tickets/TCK-0010-clarify-livro-aberto-license/` criado.
- Lição: n/a — não resolve `REJECT`.

## [002] ACTION — 2026-08-01 15:57 — tech-lead
- Ação: triagem. Status `new` → `triaged`. **Sem `HANDOFF`** (L-005).
- **Agrupamento (justificativa em uma linha):** fica **separado** do TCK-0009 (schema)
  porque tem outro dono, outro tipo e outro modo de falhar — pode terminar em
  `blocked: human-input` esperando resposta de terceiro, e arrastar o contrato de dados para
  essa espera seria bloquear trabalho pronto por causa de um e-mail.
- **Tipo:** `research`. Cadeia curta do protocolo: `tech-lead` → `researcher` → `tech-lead`.
  **Extensão declarada:** se a conclusão alterar arquivos (critérios 4 e 5), segue
  `code-reviewer` → `qa-validator` antes do `done`; se terminar em relatório + pergunta ao
  usuário, volta a mim e vira `blocked: human-input`. Registro a bifurcação agora para o
  executor não improvisar cadeia.
- **Prioridade P2 · tamanho P.** Não bloqueia nada em curso: a leitura restritiva já está
  registrada e é segura. Está acima de P3 pelo retorno assimétrico — se a resposta for BY-SA,
  o projeto ganha um livro didático completo de ensino médio em pt-BR como matéria-prima
  legítima, e o custo de produção autoral da Fase 1 muda de patamar. Aposta barata, prêmio
  alto.
- **Owner: `researcher`** — fontes gratuitas, licenças e literatura didática são sua área
  exclusiva; foi quem levantou as três referências do nó piloto no TCK-0001.
- **Restrições passadas ao executor:**
  1. **Nada de adaptar antes da conclusão.** Enquanto o resultado não for (a), a obra é
     `citable-only` (`AGENTS.md` §9.7, L-009). Critério 6 é bloqueante.
  2. **Verificar por obra, não por projeto** (L-006): licença de coleção pode variar entre
     volumes; concluir a partir de um único PDF é o erro já registrado.
  3. Toda declaração vale por **citação literal + URL + HTTP code + data** — selo gráfico
     conta como evidência, mas registrar como foi lido (no TCK-0001 foi `pdftoppm` sobre o
     colofão, porque o selo é imagem; L-007).
  4. Se as fontes públicas não fecharem a questão, **não inventar contato nem enviar nada**:
     entregar a pergunta objetiva e o canal verificado, e parar em `blocked: human-input`.
  5. Nenhuma edição em `theory.*.md` ou `exercises.json`, qualquer que seja a conclusão.
- **Aderência ao plano:** Fase 1 do roadmap depende de fontes gratuitas com licença
  registrada; `ADR-0005` já fixou a regra de compatibilidade. Este ticket não altera decisão,
  apura fato. Dentro do plano.
- **Requisitos inegociáveis conferidos:** gratuidade (critério 7 exige acesso público
  anônimo), bilinguismo (o objetivo é justamente destravar fonte em pt-BR); a11y, offline e
  privacidade não aplicáveis, com o porquê no ticket.
- **Dependências:** nenhuma. Interage com o `TCK-0009` apenas no formato do registro — se o
  schema já estiver entregue, a conclusão vira valor de `usage`; se não, vira nota no campo
  `license`/`licenseNotes` no formato vigente. O executor usa o formato do dia, sem esperar.
- Resultado: ok — `status: triaged`, `owner: researcher`. Aguardando ordem de execução.
- Lição: n/a — não resolve `REJECT`.

## [003] HANDOFF — 2026-08-01 16:30
- De: tech-lead → Para: researcher
- Status novo: in_progress
- O que foi feito: triagem concluída em `[002]` (tipo `research`, P2/P, owner `researcher`,
  cadeia `tech-lead` → `researcher` → `tech-lead` com bifurcação declarada). Entrada
  registrada retroativamente pelo `researcher` ao assumir a execução — o `[002]` foi fechado
  sem `HANDOFF` (L-005) e a ordem de execução chegou depois.
- Artefatos: `tickets/TCK-0010-clarify-livro-aberto-license/ticket.md` (`status: triaged` →
  `in_progress`).
- Como validar: `sed -n '1,12p' tickets/TCK-0010-clarify-livro-aberto-license/ticket.md`
  mostra `status: in_progress`, `owner: researcher`.
- Pendências e riscos: nenhuma verificação de licença feita ainda neste ticket. Risco
  conhecido: as fontes públicas podem continuar divergentes, caso em que o desfecho é
  `blocked: human-input` (critério 3c), não uma conclusão por inferência.
- Critérios de aceite: [ ] 1 · [ ] 2 · [ ] 3 · [ ] 4 · [ ] 5 · [ ] 6 · [ ] 7 · [ ] 8 —
  nenhum atendido na abertura da execução.

## [004] ACTION — 2026-08-01 16:55 — researcher
- Ação: levantamento de evidência sobre a licença do *Livro Aberto de Matemática*. Todas as
  consultas em **2026-08-01**, por acesso anônimo, sem login e sem pagamento (critério 7).
  Ambiente: `curl`, `poppler` (`pdftotext`, `pdfimages`, `pdftoppm`), API pública do GitHub.
- Motivo: decidir entre (a) BY-SA → `adaptable`, (b) BY-NC-SA → `citable-only`, (c)
  indeterminado nas fontes públicas (critério 3).

### Fonte (a) — página do projeto (UNIRIO)
`https://livroaberto.uniriotec.br/sobre/` — **HTTP 200**, 39.594 bytes, HTML estático (sem JS).
Citação literal: *"O projeto Livro Aberto de Matemática adotou uma licença Creative Commons do
tipo BY-NC-SA, ou seja, todo uso que for feito do material deve mencionar os autores, não são
permitidos usos comerciais e todo material derivado também deve adotar licença equivalente."*
O selo da própria página (`.../uploads/sites/57/2023/05/licenca.png`, HTTP 200, 380×133, lido
como imagem) mostra **CC BY NC SA** — coerente com o texto. **Sem versão e sem link para o deed
da CC**: nenhuma ocorrência de `creativecommons.org/licenses/` no HTML.

### Fonte (b) — colofão dos PDFs (Ensino Médio)
No PDF já referenciado no nó piloto (*Função Quadrática*, aluno, v1.1 de 26/07/2021 —
`raw.githubusercontent.com/livro-aberto/tex-design-development/master/Cap%C3%ADtulos%20prontos%20-%20Aluno/Fun%C3%A7%C3%A3o%20Quadr%C3%A1tica.pdf`,
**HTTP 200**, 4.265.038 bytes, 85 págs), o colofão é a **página 3**. O rótulo textual é apenas
`Licença:` — **sem nenhum texto de licença ao lado**. O valor é uma imagem (447×157), extraída
com `pdfimages -f 3 -l 3 -png` e lida como imagem: **CC BY SA** (dois ícones: BY e SA; sem o
ícone NC do cifrão cortado). Reproduz o achado do TCK-0001 por caminho independente.
**Nenhum PDF da coleção contém URI da CC**: varredura de todos os 28 capítulos (inclusive
descomprimindo os streams `Flate`) atrás de `creativecommons.org` → **zero ocorrências**. Logo
a licença dos PDFs não tem versão nem link — só o selo gráfico.

### Critério 2 — censo por obra (não extrapolar de um único PDF, L-006)
Baixados os **28 capítulos não-HQ da versão do aluno** (todos HTTP 200). Método: localizar a
página do rótulo `Licença:` (`pdftotext`), extrair as imagens dessa página (`pdfimages`),
isolar a de proporção ~2,85 (o selo) e contar os blocos de texto branco na tarja inferior
("BY SA" vs "BY NC SA"). **Classificador validado contra 16 leituras visuais** dos selos
renderizados (`pdftoppm -r 150` + recorte do bbox de `Licença:`): **16/16 de acordo**.
Resultado — **o selo varia capítulo a capítulo dentro da mesma coleção**:
  - **BY-SA (15/28):** A Natureza da Estatística · Estatística e Probabilidade · Função Afim ·
    **Função Quadrática** · Introdução às Funções · Módulo de Funções · Medidas de Posição e
    Dispersão · Medidas em Geometria Espacial · Probabilidade · Semelhança · Taxa de Variação ·
    Teorema de Tales · Unidades de Medida e Ordens de Grandeza · Vetores no Plano · Vistas
    Ortogonais e Representações em Perspectiva.
  - **BY-NC-SA (13/28):** Análise Combinatória · Áreas de Superfície · Educação Financeira ·
    Função Exponencial · Funções Trigonométricas · Ladrilhamento · Logaritmos e a Função
    Logarítmica · Pensamento Computacional · Projeções Cartográficas · Projetos de Investigação
    com Matemática · Sistemas Lineares e Inequações · Transformações Geométricas · Trigonometria.
  - Versão do **professor** de *Função Quadrática* (HTTP 200, 4.342.682 bytes): selo **BY-SA**,
    idêntico byte a byte ao da versão do aluno (`md5 ae4adaa7ba16baae8adc46059b1edd9b`) —
    aluno e professor concordam entre si.
  - As três únicas ocorrências textuais de "CC-by-sa"/"CC-BY" dentro dos capítulos são
    **crédito de fotografia** (ex.: *"Figura 1.12: … Foto: Hajor CC-by-sa"*), não cláusula de
    licença. Nenhum capítulo do Ensino Médio traz declaração textual de licença.

### Critério 2 — outra obra do projeto: *Frações no Ensino Fundamental (volume 1)*
Aqui há **texto**, não só selo. PDF do aluno (`livro-de-fracoes`, HTTP 200, 25.822.624 bytes,
123 págs, v3.0 de fevereiro de 2021), colofão na p. 3, citação literal:
*"Após o dia 1o de setembro de 2026 esta obra passa a estar licenciada por CC-by-sa."*
A edição de 2017 hospedada no IMPA
(`umlivroaberto.impa.br/wp-content/uploads/2019/10/livro_aluno_completo.pdf`, HTTP 200,
6.825.991 bytes) traz a mesma frase e mais uma: *"Algumas figuras podem possuir licença com
mais direitos do que a vigente para todo o material."* As versões do professor (GitHub e IMPA)
repetem a frase. O **selo** do colofão das Frações é **BY-NC-SA**, coerente com a frase.

### Fonte (c) — repositórios oficiais no GitHub (`github.com/livro-aberto`)
API pública, HTTP 200. Nove repositórios. **Nenhum repositório de conteúdo tem arquivo de
licença**: `tex-design-development` (onde estão os PDFs do Ensino Médio) → `license: None`,
sem `LICENSE`/`COPYING` na raiz; `ensino_medio`, `livro-de-fracoes`, `atividades-livro-aberto`,
`livroabertoem` → idem. O único com `LICENSE` é `fracoes_livro_piloto`, e o arquivo é a
**GNU GPL v2** (18.047 bytes) — licença de *software*, incompatível com a declaração CC do
próprio README, o que a torna inútil como declaração sobre o conteúdo.
O `README.md` de `fracoes_livro_piloto` e o de `livro-de-fracoes` (idênticos, HTTP 200) dizem
literalmente: *"A este material está atribuída a licença Creative Commons by-sa-nc até o dia 1º
de setembro de 2026, quando os direitos serão ampliados para CC-by-sa."* — isto é, **BY-NC-SA
hoje, BY-SA a partir de 2026-09-01**, e vale para as **Frações**, não para o Ensino Médio.
Há ainda `fracoes_livro_piloto/BY-SA.md` (HTTP 200, 854 bytes), documento **interno de
argumentação** intitulado *"Vantagens da licença BY-SA, sem NC"* (*"com NC, não podemos
incorporar forks"*, *"com NC, não temos ajuda de empresas não-parceiras"*). É prova de que a
migração foi deliberada dentro do projeto — **não é concessão de licença** e não deve ser lido
como tal.

### Fonte (d) — publicações institucionais IMPA/OBMEP
- `https://impa.br/en_US/noticias/livro-aberto-de-matematica-disponibiliza-novos-conteudos-digitais/`
  (05/07/2024, HTTP 200): *"…produzir coleções para a Educação Básica de forma colaborativa e
  com licença aberta (Creative Commons)"* e *"Os livros podem ser usados por professores e
  alunos de forma gratuita, porém sem fins lucrativos."* — **não nomeia a variante**, mas a
  segunda frase descreve NC.
- `https://impa.br/en_US/noticias/projeto-do-impa-propoe-livro-didatico-aberto-e-colaborativo/`
  (HTTP 200) e `https://impa.br/notices/livro-aberto-de-matematica-e-tema-de-minicursos/`
  (12/09/2018, HTTP 200): só *"licença aberta (Creative Commons)"*. Nenhuma das três páginas
  contém `creativecommons.org/licenses/`.
- **Site oficial atual do projeto, hospedado pelo IMPA**: `https://umlivroaberto.impa.br/`
  (HTTP 200). Diz apenas *"Materiais didáticos com licença Creative-Commons para a Educação
  Básica"*; `/o-projeto/` e `/producoes/` falam em *"licença aberta"* sem nomear a variante;
  **zero** ocorrências de `creativecommons.org/licenses/` em todas as páginas baixadas.
  **Achado relevante:** as páginas `/producao/funcoes/`, `/producao/geometria/`,
  `/producao/estatistica-e-probabilidade/`, `/producao/analise-combinatoria/` e
  `/producao/a-matematica-nas-ciencias-sociais-e-da-natureza/` (todas HTTP 200) apontam, via
  `docs.google.com/viewer?url=…`, exatamente para os **mesmos PDFs do GitHub** que auditei —
  inclusive o de *Função Quadrática*. Ou seja, os PDFs com selo BY-SA **são a distribuição
  oficial corrente**, não uma versão antiga esquecida.

### Fontes não verificáveis (registrar em vez de adivinhar — L-007)
- `https://umlivroaberto.org/` e `https://www.umlivroaberto.org/` → **HTTP 403**.
- `https://umlivroaberto.com/` (URL impressa no colofão de 2017) → falha de TLS,
  *"SSL certificate problem: certificate has expired"*.
- `https://livro-aberto.github.io/ensino_medio/` (indicado pelo README de `ensino_medio` como
  local das versões mais atuais) → HTTP 200 com o corpo inteiro
  `<html><body><p>Página em construção.</p></body></html>`.
- `https://umlivroaberto.impa.br/producoes/ensino-medio/` lista capítulos, mas a licença **não
  aparece em lugar nenhum** do HTML servido.

### Conclusão — critério 3, alternativa (c): INDETERMINADO nas fontes públicas
Não é possível concluir (a) nem (b) para o capítulo *Função Quadrática* sem inferência. O que
as fontes efetivamente dizem, sem interpretação:
1. As duas páginas oficiais (UNIRIO e IMPA) e a nota institucional do IMPA descrevem **NC**,
   de forma **genérica para o projeto inteiro**, sem citar obra nem versão.
2. O PDF da obra — que é a distribuição oficial corrente, linkada pelo próprio site do IMPA —
   traz selo **BY-SA**, sem NC, **sem versão e sem URI**, e **nenhum texto** de licença.
3. O selo **varia entre capítulos da mesma coleção** (15 BY-SA × 13 BY-NC-SA). Isso derruba a
   hipótese de que a página do projeto descreve corretamente a coleção toda, mas **não** decide
   se os 15 selos BY-SA são escolha deliberada por capítulo ou erro de diagramação — as duas
   explicações são compatíveis com toda a evidência levantada.
4. Numa obra irmã (Frações) o projeto declarou **por escrito** BY-NC-SA com migração para
   **BY-SA em 2026-09-01**, e há documento interno defendendo largar o NC. Isso torna a
   hipótese BY-SA plausível — **plausível não é verificado** e não altera a leitura.
Portanto, permanece **a leitura mais restritiva (L-007): `CC BY-NC-SA`, `citable-only`**. O
`references.json` do nó piloto **não muda de valor**; critérios 4 e 5 não se aplicam (ficam
como "não aplicável nesta conclusão", não como pendência).
- Resultado: ok. Critérios 1, 2, 3(c), 6, 7 e 8 atendidos; 4 e 5 não aplicáveis. Nenhum arquivo
  de `content/` tocado (`git diff --stat -- content/` vazio). Reprodutível: todas as URLs,
  códigos HTTP e comandos estão acima.
- Lição: n/a — não resolve `REJECT`.

## [005] HANDOFF — 2026-08-01 17:05
- De: researcher → Para: tech-lead
- Status novo: **blocked: human-input**
- O que foi feito: as quatro fontes exigidas foram consultadas e citadas literalmente em
  `[004]`, mais um censo dos 28 capítulos do Ensino Médio e da obra irmã (Frações). A
  divergência **não se resolve nas fontes públicas** e ficou maior do que se sabia: o selo varia
  entre capítulos da mesma coleção (15 BY-SA × 13 BY-NC-SA), nenhum PDF traz versão ou URI da
  CC, e nenhum repositório de conteúdo tem arquivo de licença. Só o detentor pode fechar a
  questão. Conclusão registrada: **alternativa (c)**; vale a leitura restritiva (L-007).
- Artefatos: `tickets/TCK-0010-clarify-livro-aberto-license/log.md` `[004]` (evidência) e este
  `[005]`. **Nenhum arquivo de `content/`, `docs/` ou `memory/` de conteúdo foi alterado.**
- Como validar: `bash scripts/audit-content.sh` → sem erros; `git diff --stat -- content/`
  vazio; as URLs e comandos de `[004]` reproduzem cada afirmação.
- Pendências e riscos: a decisão depende de resposta de terceiro. **Risco com prazo:** a obra
  irmã declara migração para CC BY-SA em **2026-09-01** (31 dias); se a mesma data valer para o
  Ensino Médio, a resposta pode mudar sozinha em setembro — motivo a mais para perguntar agora e
  para reavaliar depois dessa data, independentemente da resposta.

### Canal de contato verificado (nada foi enviado)
1. **`livroaberto@impa.br`** — primário. Impresso no colofão (p. 3) de **todos** os capítulos
   conferidos, ao lado de *"Coordenação: Fabio Simas e Augusto Teixeira"*. É o único endereço
   específico do projeto encontrado em fonte primária.
2. **Issues públicas** do repositório que hospeda os PDFs:
   `https://github.com/livro-aberto/tex-design-development/issues` — issues habilitadas
   (`has_issues: true`, 13 abertas, API pública). Vantagem: a resposta fica pública e citável.
3. **`faleconosco@impa.br`** — institucional do IMPA, só como fallback.

### Texto do pedido, pronto para o usuário enviar (não enviado)
> **Assunto:** Esclarecimento sobre a licença dos capítulos do Livro Aberto de Matemática
> (Ensino Médio)
>
> Prezados Fabio Simas e Augusto Teixeira,
>
> Sou responsável por um projeto educacional gratuito e sem fins lucrativos que está montando
> uma plataforma aberta de estudos de matemática, bilíngue (português e inglês). Todo o
> conteúdo que publicamos sai sob **CC BY-SA 4.0**, e por isso precisamos distinguir com
> precisão o material que podemos apenas **citar como leitura** daquele que podemos **adaptar**
> com a devida atribuição.
>
> Encontramos declarações diferentes sobre a licença do Livro Aberto de Matemática e gostaríamos
> de confirmar com vocês qual é a correta:
>
> 1. A página do projeto (https://livroaberto.uniriotec.br/sobre/) afirma que "o projeto Livro
>    Aberto de Matemática adotou uma licença Creative Commons do tipo BY-NC-SA".
> 2. Nos PDFs dos capítulos do Ensino Médio distribuídos em
>    https://github.com/livro-aberto/tex-design-development (os mesmos linkados em
>    umlivroaberto.impa.br), o selo do colofão **varia de um capítulo para outro**: em 15 dos
>    28 capítulos da versão do aluno ele mostra **CC BY-SA**, sem o ícone NC — entre eles
>    *Função Quadrática*, *Função Afim*, *Teorema de Tales* e *Probabilidade*; nos outros 13
>    mostra **CC BY-NC-SA**.
> 3. O livro *Frações no Ensino Fundamental* diz, no colofão: "Após o dia 1º de setembro de
>    2026 esta obra passa a estar licenciada por CC-by-sa".
>
> Nossas perguntas são objetivas:
>
> a) Qual licença vale hoje para os capítulos do **Ensino Médio** — BY-NC-SA para todos, ou
>    BY-SA para aqueles cujo colofão traz o selo sem NC?
> b) Qual é a **versão** da licença (2.5, 3.0 ou 4.0)? Os PDFs trazem o selo sem número de
>    versão e sem link para o texto da licença.
> c) A migração para CC BY-SA anunciada para **1º de setembro de 2026** vale também para os
>    capítulos do Ensino Médio, ou só para o livro de Frações?
> d) Havendo permissão de adaptação, qual é a forma de atribuição que vocês preferem?
>
> Se for útil, podemos enviar a lista completa dos 28 capítulos com o selo que consta em cada
> um. Não usaremos o material como base de texto adaptado enquanto não houver confirmação de
> vocês — hoje ele consta na nossa lista de referências apenas como leitura externa, com
> crédito aos autores.
>
> Agradeço desde já pela atenção e pelo trabalho de vocês.
>
> Atenciosamente,
> <nome do usuário> — <projeto / URL pública, se houver>

### Perguntas objetivas que só o usuário pode responder
1. **Autoriza o envio?** Mandar mensagem para fora do repositório é ato do usuário; nenhum
   agente o fará. Se sim, por qual canal — e-mail (`livroaberto@impa.br`) ou issue pública no
   GitHub (resposta citável, mas o pedido fica público)?
2. **Como nos identificamos?** O texto tem dois campos em branco (`<nome do usuário>` e
   `<projeto / URL pública>`); o `mathematics-studies` ainda não tem URL pública para citar.
3. **Esperamos 2026-09-01?** Se a resposta não vier, vale reabrir este ticket depois dessa data
   para reconferir os colofões (a obra irmã migra para BY-SA nesse dia)?

### Proposta de atualização do `references.json` — NÃO executada
Fica para ticket próprio ou handoff ao dono de `content/` (o TCK-0009 muda o schema; o formato
final depende dele). No nó `content/high-school/algebra/quadratic-equations/references.json`,
item 3, o **valor não muda** — `CC BY-NC-SA` segue valendo — mas a nota deveria passar a dizer o
que hoje ela não diz:
- `license`: `"CC BY-NC-SA (versão não declarada)"`;
- `licenseNotes`: divergência **não resolvida** entre a página do projeto (BY-NC-SA, texto e
  selo) e o colofão do PDF (selo BY-SA, sem versão e sem URI); o selo **varia entre capítulos**
  da mesma coleção (15 BY-SA × 13 BY-NC-SA na versão do aluno); nenhum repositório de conteúdo
  tem arquivo de licença; obra irmã (Frações) declara migração para CC BY-SA em 2026-09-01;
  verificado em 2026-08-01 (TCK-0010);
- `usage`: `"citable-only"`;
- URL: trocar `blob/master/` pelo permalink por SHA
  `88226d28925c13e48894f19572192712822b615c` (dívida já registrada no TCK-0001; `master` não se
  move desde 2022-02-17, mas continua sendo referência instável).
- Critérios de aceite: [x] 1 · [x] 2 · [x] 3 (alternativa **c**) · [–] 4 (n/a: não houve
  conclusão (a) nem (b)) · [–] 5 (n/a: não houve conclusão BY-SA) · [x] 6 · [x] 7 · [x] 8.
