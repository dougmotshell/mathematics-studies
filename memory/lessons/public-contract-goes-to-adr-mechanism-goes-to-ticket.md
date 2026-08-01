**Tipo:** sucesso
**ID:** L-020
**Contexto:** 2026-08-01, `TCK-0011` — ao especificar o esqueleto da aplicação era preciso
fechar decisões que a spec da fatia mínima deixou em aberto (forma da URL bilíngue, onde mora
o projeto, como `content/` é lido) **sem** reincidir em L-011, que proíbe o ADR de decidir
implementação (momento de renderização do KaTeX, estratégia de cache, biblioteca de UI). Os
dois riscos são opostos: decidir demais rouba o ticket; decidir de menos deixa o ticket
inventando contrato público no meio de um trabalho de interface.

**Lição:** o discriminador não é "arquitetura × implementação" (vago demais para arbitrar na
hora), é **permanência observável de fora**:

- **Vai para ADR** o que alguém de fora observa e que custa caro desfazer: URL pública, formato
  de dado, fronteira entre acervo e aplicação, custo, elegibilidade de plano gratuito.
- **Fica com o ticket** o que se troca sem que nada externo perceba: biblioteca dentro da ilha,
  ferramenta de teste, mecanismo de cache, momento em que a fórmula vira HTML.

O teste operacional é uma pergunta só: *se eu trocar isto daqui a seis meses, quem quebra?* Se
a resposta for "um link de terceiro, um arquivo do acervo, a fatura ou outro ADR", é ADR. Se
for "só o nosso próprio código", é ticket.

**Como aplicar:** ao escrever ADR de esqueleto ou de plataforma, listar as decisões candidatas
e passar cada uma pela pergunta acima **antes** de redigir; as que ficarem de fora entram
explicitamente numa lista do que o ADR **não** decide, com o marcador que o diagrama vai usar
(`EM ABERTO (ticket)`), para não voltarem como afirmação implícita num rótulo de Mermaid
(L-011, L-013). Corolário: decisão que passou no teste e continua `proposed` **bloqueia** o
ticket que depende dela — isso tem de ser declarado no handoff, não descoberto pelo executor.

**Adendo — 2026-08-01, mesmo dia da criação (`TCK-0011`, `[006] REJECT`):** a régua estava
certa e mesmo assim o ADR decidiu mecanismo. Causa: apliquei-a como **filtro da lista de
decisões candidatas**, antes de redigir, e não como **passe de revisão sobre o texto pronto**.
O que escapa do filtro é o que não estava na lista — a decisão indevida entra depois, como
justificativa de apoio de outro item, dentro de um rótulo de Mermaid ou de uma linha de
`scripts` do manifesto. Foi assim que `prebuild` virou decisão de ADR sem nunca ter sido
proposto como decisão. **Como aplicar (segundo passe, obrigatório):** com o documento pronto,
percorrer cada afirmação — prosa, rótulo de diagrama e tabela — e perguntar de novo "se eu
trocar isto em seis meses, quem quebra?". O ganho é maior justamente nos trechos que não foram
escritos *como* decisão. Foi o revisor, usando a minha própria régua no meu texto pronto, que
achou o defeito que eu não achei.
