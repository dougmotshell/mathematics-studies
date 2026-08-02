# Memória do agente `researcher`

> Memória persistente deste agente, mantida por ele próprio ao final de tarefas
> significativas. Índice geral: `memory/MEMORY.md` · lições: `memory/LESSONS.md` ·
> contexto da área: `memory/context/`.

## Papel

Pesquisa fontes gratuitas, referências bibliográficas, licenças, bancos de exercícios abertos e literatura de didática da matemática, sintetizando com citação de fontes. Usar antes de escrever conteúdo novo ou ao avaliar material externo.

## Notas persistentes

- **Licença do OpenStax varia por livro.** Verificado em 2026-08-01: *Algebra and
  Trigonometry 2e* e *Intermediate Algebra 2e* são **CC BY-NC-SA 4.0**, não CC BY 4.0.
  Checagem rápida: `curl -sSL <url> | grep -o 'creativecommons.org/licenses/[a-z-]*/[0-9.]*'`
  — o OpenStax embute `"license":{...}` no HTML da página. Ver L-006.
- **Como verificar licença, em ordem:** (1) `grep` de `creativecommons.org/licenses/` no
  HTML bruto; (2) página "sobre"/licença em HTML estático; (3) colofão do PDF
  (`pdftotext`; `pdftoppm -f N -l N -png` + leitura da imagem quando o selo é figura).
  SPA renderizada por JS (PhET, M³/Unicamp, Khan Academy) não permite verificar — descartar.
  Ver L-007.
- **Acervo pt-BR — mapa do que já foi checado (2026-08-01):**
  - *Só citável (`citable-only`), divergência NÃO resolvida (TCK-0010, 2026-08-01):*
    **Livro Aberto de Matemática** (IMPA/OBMEP/Assoc. Livro Aberto). Cobre Ensino Médio
    (funções, geometria, estatística/probabilidade) e Ensino Fundamental (Frações). É a melhor
    fonte aberta em pt-BR encontrada até agora, mas **não pode ser adaptada** hoje. O que cada
    fonte diz: página do projeto (`livroaberto.uniriotec.br/sobre/`) e selo dela → BY-NC-SA;
    site oficial do IMPA (`umlivroaberto.impa.br`) e notícias do IMPA → só "licença aberta
    (Creative Commons)", sem nomear variante, mais "gratuita, porém sem fins lucrativos";
    colofão dos PDFs → **selo que varia por capítulo**, 15 BY-SA × 13 BY-NC-SA nos 28 capítulos
    do aluno (*Função Quadrática* é BY-SA), **sem versão e sem URI da CC em nenhum PDF**;
    nenhum repositório de conteúdo em `github.com/livro-aberto` tem arquivo de licença (o único
    `LICENSE` é GPL-2.0, em `fracoes_livro_piloto`, e contradiz o README do próprio repo).
    **Data com prazo:** o livro de Frações declara por escrito, no colofão e no README,
    "by-sa-nc até o dia 1º de setembro de 2026, quando os direitos serão ampliados para
    CC-by-sa" → **reconferir depois de 2026-09-01**. Ver L-023.
  - *Descartado por falta de licença:* Portal da Matemática OBMEP (`portaldaobmep.impa.br`).
  - *Descartado por licença não verificável (JS/403):* PhET pt_BR, M³/Unicamp, Khan
    Academy pt-BR.
  - *Licença OK mas qualidade ruim:* Wikilivros `Matemática elementar/Equações algébricas`
    (CC BY-SA 4.0 via `action=query&meta=siteinfo&siprop=rightsinfo`) — tem gabaritos
    errados na lista de exercícios; não citar sem revisão.
  - *Licença OK, uso possível como complemento:* Wikipédia/Wikilivros/Wikiversidade em pt
    (CC BY-SA 4.0, confirmável pela API `rightsinfo`).
- **Onde os PDFs do Livro Aberto realmente moram:** o site oficial do IMPA
  (`umlivroaberto.impa.br/producao/<slug>/`) não hospeda os capítulos do Ensino Médio — ele
  linka, via `docs.google.com/viewer?url=…`, os **mesmos arquivos** de
  `github.com/livro-aberto/tex-design-development` (`Capítulos prontos - Aluno|Professor`). Logo
  o PDF do GitHub **é** a distribuição oficial corrente, não uma cópia antiga. SHA de `master`
  em 2026-08-01 (imóvel desde 2022-02-17): `88226d28925c13e48894f19572192712822b615c` — usar em
  permalink. Contato do projeto impresso no colofão de todo capítulo: `livroaberto@impa.br`
  (coord. Fabio Simas e Augusto Teixeira); issues públicas habilitadas em
  `livro-aberto/tex-design-development`.
- **Ler selo de licença em lote (receita do TCK-0010):** achar a página do rótulo `Licença:`
  com `pdftotext`; `pdfimages -f N -l N -png` e ficar com a imagem de proporção ~2,85 (selo CC
  88×31); classificar contando os blocos de texto branco na tarja inferior (2 palavras → BY-SA,
  3 → BY-NC-SA). **Sempre validar o classificador contra leitura visual** de uma amostra grande
  (`pdftoppm -r 150` + recorte pelo bbox de `pdftotext -bbox`) antes de confiar no número —
  foram 16/16 no TCK-0010. Vale também caçar `creativecommons.org` no PDF *descomprimindo os
  streams Flate*: se não houver URI, o selo não tem versão e a evidência é fraca.
- **Fora do ar / não verificável (reconferido em 2026-08-01):** `umlivroaberto.org` e
  `www.umlivroaberto.org` → HTTP 403; `umlivroaberto.com` → certificado TLS expirado;
  `livro-aberto.github.io/ensino_medio/` → HTTP 200 com "Página em construção.".
- O campo `covers` é conferido contra o **sumário real** da seção, não contra o título.
- `bash scripts/audit-content.sh` só checa **presença** de `author/year/url/language/license`
  em `references.json`; não valida URL nem vocabulário de licença — a verificação é humana.

## Últimas execuções

| Data | Ticket/Tarefa | Resultado | Lição relacionada |
|---|---|---|---|
| 2026-08-01 | TCK-0001 — verificar `references.json` do nó piloto | 2 licenças OpenStax corrigidas para CC BY-NC-SA 4.0, `covers` reescritos, 1 fonte pt-BR adicionada (Livro Aberto de Matemática); `audit-content.sh` 0 erros; handoff para `code-reviewer` | L-006, L-007 |
| 2026-08-01 | TCK-0010 — esclarecer a licença do *Livro Aberto de Matemática* | **Indeterminado nas fontes públicas** (critério 3c): 4 fontes citadas literalmente + censo dos 28 capítulos (15 BY-SA × 13 BY-NC-SA) + obra irmã com migração declarada para 2026-09-01; leitura restritiva mantida; pedido ao IMPA redigido e canal verificado, **nada enviado**; ticket em `blocked: human-input` | L-023 (nova), L-006, L-007 |
