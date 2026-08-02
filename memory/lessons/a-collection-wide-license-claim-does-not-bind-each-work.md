**Tipo:** correção
**ID:** L-023
**Contexto:** TCK-0010, 2026-08-01 — *Livro Aberto de Matemática* (IMPA/OBMEP). A página oficial
do projeto (`https://livroaberto.uniriotec.br/sobre/`) declara, para a coleção inteira, "uma
licença Creative Commons do tipo BY-NC-SA". Ao auditar os **28 capítulos** do Ensino Médio
(versão do aluno) um a um, o selo do colofão mostrou **CC BY-SA em 15 deles** e **CC BY-NC-SA em
13**. Os PDFs auditados são a distribuição oficial corrente — o próprio site do IMPA
(`umlivroaberto.impa.br`) linka exatamente esses arquivos. Generaliza a L-006, que já dizia que
a licença varia por livro dentro de um mesmo projeto.

**Lição:** declaração de licença "do projeto" não vincula cada obra, e a granularidade do
desvio pode ser menor do que a obra: aqui variou **por capítulo dentro da mesma coleção**. Duas
consequências práticas. (1) Auditar por amostra de um artefato é insuficiente — foi a checagem
capítulo a capítulo que revelou a variação; conferir só o *Função Quadrática* teria produzido a
conclusão errada nos dois sentidos possíveis. (2) Divergência entre nível de agregação
(projeto × obra × capítulo) **não se resolve escolhendo o mais específico**: um selo sem versão
e sem URI da CC, sem nenhum texto de licença ao lado, não é concessão mais confiável do que a
frase da página oficial — é apenas outra evidência fraca. O desfecho legítimo é "indeterminado",
não "provavelmente o mais permissivo".

**Como aplicar:**
1. Antes de classificar uma coleção como adaptável, **enumerar os artefatos e conferir todos**,
   não uma amostra. Quando são muitos, automatizar e **validar o automatismo contra leitura
   direta** de uma amostra grande (no TCK-0010: classificador de selo validado 16/16 contra
   leitura visual) — automatismo não validado é palpite com barra de progresso.
2. Registrar a licença **por artefato**, com o nível de agregação explícito ("este capítulo",
   não "esta coleção").
3. Tratar como **evidência incompleta** todo selo CC sem número de versão e sem link para o
   deed: sem versão não dá para afirmar compatibilidade com CC BY-SA 4.0.
4. Quando o material declara **prazo** ("a partir de <data> passa a ser CC BY-SA" — caso do
   livro de Frações, 2026-09-01), anotar a data e **reabrir a verificação depois dela**; a
   resposta pode mudar sem que ninguém avise.
5. Fontes divergentes e igualmente fracas → leitura mais restritiva (L-007) **e** pergunta ao
   detentor. Não promover plausibilidade a conclusão.
