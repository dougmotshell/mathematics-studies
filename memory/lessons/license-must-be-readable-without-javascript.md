**Tipo:** sucesso
**ID:** L-007
**Contexto:** TCK-0001, 2026-08-01. Na busca por uma referência gratuita em pt-BR, as
candidatas caíram por motivo de **verificabilidade**, não de qualidade: Portal da
Matemática OBMEP não declara licença alguma; PhET (pt_BR), M³/Unicamp e Khan Academy
pt-BR são SPAs renderizadas por JavaScript, cujo HTML não contém a licença
(`support.khanacademy.org` ainda devolveu `HTTP 403`); `umlivroaberto.com` está com
certificado SSL expirado. A fonte aceita — Livro Aberto de Matemática (IMPA/OBMEP) — foi
aceita porque a licença está em texto puro na página oficial do projeto **e** no colofão
do PDF do capítulo.
**Lição:** o gargalo para citar OER em pt-BR raramente é achar material bom; é achar
material cuja licença seja **legível e citável**. Fonte cuja licença só existe em página
renderizada por JS fica, na prática, "não reutilizável até prova em contrário" — e não se
deve preencher o campo `license` por reputação da instituição.
**Como aplicar:** ao avaliar uma fonte, tentar nesta ordem: (1) `grep` de
`creativecommons.org/licenses/...` no HTML bruto; (2) página institucional de licença/
"sobre" em HTML estático; (3) colofão do PDF (`pdftotext`, e `pdftoppm` + leitura da
imagem quando o selo for figura). Se nenhuma funcionar, descartar e registrar a tentativa
no log — sem licença explícita, não entra. Havendo **divergência** entre duas declarações
da mesma obra (site vs. selo do PDF), registrar a leitura **mais restritiva** e escrever a
divergência no próprio campo `license`.
