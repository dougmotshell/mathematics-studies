---
id: TCK-0010
title: Esclarecer a licença do Livro Aberto de Matemática (BY-SA ou BY-NC-SA)
type: research
status: triaged
owner: researcher
priority: P2
size: P
created: 2026-08-01
updated: 2026-08-01
related: [TCK-0001, TCK-0004, TCK-0009]
---

# TCK-0010 — Esclarecer a licença do Livro Aberto de Matemática (BY-SA ou BY-NC-SA)

## Pedido original (verbatim)

> **Livro Aberto (S1):** vale abrir trabalho para esclarecer a licença com IMPA/OBMEP; se
> for BY-SA sem NC, o projeto ganha a única fonte pt-BR adaptável conhecida.

— `tickets/TCK-0004-define-project-license/log.md` `[009]`, pendência 2.

> **Divergência confirmada como real por mim** (não aceita do log): site diz BY-NC-SA, selo do
> PDF diz BY-SA. A leitura mais restritiva adotada está correta (L-007) e a divergência está
> declarada no próprio campo `license`. A ausência de versão ("4.0") também é real — não foi
> inventada.

— `tickets/TCK-0001-verify-pilot-node-references/log.md` `[007]`, critério 2.

## Requisito refinado

Quem sofre: todo autor de conteúdo em pt-BR. Hoje **não existe nenhuma fonte gratuita em
pt-BR compatível** com a `CC BY-SA 4.0` do projeto (`memory/context/project-context.md`), o
que empurra 100% do texto em português para produção autoral do zero. O *Livro Aberto de
Matemática* (IMPA/OBMEP) declara duas licenças diferentes em dois lugares oficiais: a página
do projeto diz BY-NC-SA e o selo do colofão do PDF mostra BY-SA, sem NC e sem versão. Se a
correta for BY-SA, o acervo ganha a **única** fonte pt-BR adaptável conhecida — um livro
didático completo de ensino médio.

Resultado esperado: uma conclusão fundamentada e citável sobre a licença, ou a pergunta exata
a fazer ao detentor dos direitos, com o canal identificado.

## Critérios de aceite

Cada critério é observável e falharia se a implementação estivesse errada.

- [ ] 1. Pelo menos **quatro** fontes independentes de declaração de licença são consultadas
      e registradas, cada uma com URL, código HTTP, data de acesso e **citação literal** do
      trecho: (a) `https://livroaberto.uniriotec.br/sobre/`; (b) colofão do PDF do capítulo já
      referenciado no nó piloto; (c) repositório `github.com/livro-aberto/` — arquivo de
      licença, `README` ou equivalente; (d) publicação institucional IMPA/OBMEP sobre o
      projeto. Falha se alguma vier sem citação literal ou sem código HTTP.
- [ ] 2. A verificação cobre **mais de um** capítulo/volume: se a licença variar entre obras
      do mesmo projeto, isso é registrado por obra. Falha se a conclusão for extrapolada de um
      único PDF (é exatamente o erro de L-006, "licença do OpenStax varia por livro").
- [ ] 3. O relatório conclui **uma** das três, explicitamente: (a) **BY-SA** → fonte
      `adaptable`; (b) **BY-NC-SA** → `citable-only`; (c) **indeterminado nas fontes
      públicas** → nesse caso lista o que exatamente falta, a pergunta objetiva a enviar e o
      canal identificado (endereço/formulário verificado, com URL), e o ticket vai a
      `blocked: human-input` — enviar mensagem a terceiros é ato do usuário, não do agente.
- [ ] 4. Se (a) ou (b): a conclusão é propagada com a mesma redação para os três lugares que
      hoje registram a divergência — `content/.../references.json` (campo `license` /
      `licenseNotes` / `usage`, no formato vigente na data), a nota do
      `docs/adr/ADR-0005-project-license.md` e a seção de compatibilidade de
      `docs/content/content-standards.md`. Teste: `grep -rn "BY-NC-SA" docs/ content/` não
      deixa nenhuma afirmação contraditória sobre esta obra.
- [ ] 5. Se (a) **BY-SA**: o log registra o que muda no custo de produção autoral e a lição
      correspondente é criada, porque `memory/context/project-context.md` afirma hoje que
      nenhuma fonte pt-BR compatível existe — afirmação que passaria a ser falsa.
- [ ] 6. **Nenhum trecho da obra é incorporado** a `theory.*.md` ou `exercises.json` neste
      ticket, qualquer que seja a conclusão: adaptar é trabalho de outro ticket, com
      atribuição no formato de `LICENSE-CONTENT`. Teste: `git diff --stat -- content/` não
      mostra alteração em teoria nem em exercícios.
- [ ] 7. Custo zero e acesso público: toda verificação por acesso anônimo, sem login e sem
      pagamento (evidência: `http_code` e tamanho do download). Falha se alguma conclusão
      depender de fonte inacessível a quem repetir a verificação.
- [ ] 8. A conclusão é reprodutível: um terceiro consegue refazer a verificação apenas com os
      comandos e URLs do log.

### Requisitos transversais (marcar todos)

- [x] Bilinguismo pt-BR + en-US — o ticket existe justamente para viabilizar fonte em pt-BR;
      o acervo do nó já cobre os dois idiomas
- [ ] Acessibilidade WCAG 2.2 AA · [x] não aplicável — pesquisa documental
- [ ] Funciona offline / PWA · [x] não aplicável
- [x] Custo zero mantido — critério 7
- [ ] Privacidade e dados de menores (LGPD/COPPA) · [x] não aplicável
- [x] URLs de `content/` preservadas — nenhum caminho de conteúdo é tocado
- [ ] Correção matemática verificada · [x] não aplicável

## Fora de escopo

- Adaptar, traduzir ou copiar qualquer trecho da obra — mesmo que a conclusão seja BY-SA.
- Procurar outras fontes pt-BR compatíveis (varredura ampla): vira `/research-sweep` próprio
  se este ticket concluir que a lacuna continua.
- Alterar o `schema` de `references.json` — é o TCK-0009.

## Contexto e referências

- Origem: `TCK-0004/log.md` `[009]` pendência 2 (e `[006]` pendência 2);
  `TCK-0001/log.md` `[004]` e `[007]` (divergência confirmada por dois agentes independentes).
- ADRs aplicáveis: **`ADR-0005`** (conteúdo sob CC BY-SA 4.0 → NC é incompatível como
  matéria-prima) e a nota sobre esta obra registrada nele.
- Regra normativa: `AGENTS.md` §9.6–9.7; fluxograma de `docs/content/content-standards.md`.
- Arquivos-alvo prováveis: `content/high-school/algebra/quadratic-equations/references.json`,
  `docs/adr/ADR-0005-project-license.md` (nota), `docs/content/content-standards.md`,
  `memory/context/project-context.md`.
- Lições relevantes: **L-006** (licença varia por obra dentro do mesmo projeto — verificar por
  obra, nunca por editora); **L-007** (a licença tem de ser legível sem JavaScript, e o selo
  gráfico do colofão foi lido como imagem no TCK-0001); **L-009** (share-alike exclui NC).
- Ambiente: há acesso à rede (verificado em 2026-08-01, `curl` HTTP 200); `poppler`
  (`pdftotext`, `pdfinfo`, `pdftoppm`) disponível — foi assim que o selo do colofão foi lido.

## Perguntas em aberto

- Se as fontes públicas não bastarem, o contato com IMPA/OBMEP depende do usuário. A pergunta
  a ser enviada é entregável deste ticket (critério 3c), não pré-requisito dele.

## Resultado final

<preenchido pelo qa-validator ao marcar `done`>
