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
  - *Aceito:* **Livro Aberto de Matemática** (IMPA/OBMEP/Assoc. Livro Aberto) — licença
    CC BY-NC-SA declarada em `https://livroaberto.uniriotec.br/sobre/`; capítulos em PDF
    acessíveis no GitHub `livro-aberto/tex-design-development` (pasta
    `Capítulos prontos - Aluno`, também há versão "Professor"). Cobre Ensino Médio:
    funções, geometria, estatística/probabilidade. Melhor fonte aberta em pt-BR encontrada
    até agora. Atenção: site do capítulo no Overleaf dá 403 e `umlivroaberto.com` está com
    certificado expirado — usar o PDF do GitHub.
  - *Descartado por falta de licença:* Portal da Matemática OBMEP (`portaldaobmep.impa.br`).
  - *Descartado por licença não verificável (JS/403):* PhET pt_BR, M³/Unicamp, Khan
    Academy pt-BR.
  - *Licença OK mas qualidade ruim:* Wikilivros `Matemática elementar/Equações algébricas`
    (CC BY-SA 4.0 via `action=query&meta=siteinfo&siprop=rightsinfo`) — tem gabaritos
    errados na lista de exercícios; não citar sem revisão.
  - *Licença OK, uso possível como complemento:* Wikipédia/Wikilivros/Wikiversidade em pt
    (CC BY-SA 4.0, confirmável pela API `rightsinfo`).
- O campo `covers` é conferido contra o **sumário real** da seção, não contra o título.
- `bash scripts/audit-content.sh` só checa **presença** de `author/year/url/language/license`
  em `references.json`; não valida URL nem vocabulário de licença — a verificação é humana.

## Últimas execuções

| Data | Ticket/Tarefa | Resultado | Lição relacionada |
|---|---|---|---|
| 2026-08-01 | TCK-0001 — verificar `references.json` do nó piloto | 2 licenças OpenStax corrigidas para CC BY-NC-SA 4.0, `covers` reescritos, 1 fonte pt-BR adicionada (Livro Aberto de Matemática); `audit-content.sh` 0 erros; handoff para `code-reviewer` | L-006, L-007 |
