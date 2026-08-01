# Log — TCK-0009

> Append-only. Formatos em `docs/ai/ticket-protocol.md`.

## [001] ACTION — 2026-08-01 15:48 — tech-lead
- Ação: criação do ticket reunindo as dívidas D-1, D-2 e D-3 do TCK-0001 (`log.md` `[007]`),
  a pendência do campo **adaptável × só citável** do TCK-0004 (`[006]` item 1 e `[009]`
  pendência 1) e a lacuna de validação em `scripts/audit-content.py`. Trechos de origem
  copiados verbatim.
- Motivo: as quatro pendências descrevem **um único artefato sem contrato**. O TCK-0004
  tornou a regra "NC = leitura, não matéria-prima" imperativa (`AGENTS.md` §9.7) e essa regra
  hoje não tem onde se apoiar no dado.
- Resultado: ok — `tickets/TCK-0009-references-schema-and-audit/` criado. `content/` não
  tocado nesta ação.
- Lição: n/a — não resolve `REJECT`.

## [002] ACTION — 2026-08-01 15:51 — tech-lead
- Ação: triagem. Status `new` → `triaged`. **Sem `HANDOFF`** (L-005).
- **Agrupamento (justificativa em uma linha):** as quatro pendências são o mesmo trabalho —
  escrever o contrato de `references.json` e ensiná-lo ao auditor —, e resolvê-las separadas
  faria o mesmo arquivo ser migrado três vezes, com o validador chegando por último e
  reprovando o que já tinha sido "corrigido".
- **Tipo: `feature` (dados/serviços)**, não `content`: o entregável é um **contrato de dados
  + validador determinístico**; o `references.json` do piloto é a primeira migração, não o
  objeto. Cadeia de `feature`(dados) com duas etapas dispensadas, justificadas abaixo.
- **Prioridade P2 · tamanho M.** Não condiciona a saída de `draft` — o checklist de
  `published` cobra "nenhum trecho de fonte NC incorporado" por revisão humana, não pelo
  campo. Mas condiciona o **próximo nó com fontes**, porque a regra §9.7 passou a depender de
  uma distinção que o dado não expressa, e porque o rastro de auditoria dentro de `covers`
  duplica a licença (duas fontes de verdade para o mesmo fato — a classe de erro que originou
  o TCK-0001).
- **Owner: `backend-developer`.** Área exclusiva "dados, pipeline de conteúdo": schema +
  `scripts/audit-content.py` são dele. `product-analyst` **dispensado** (os critérios já são
  verificáveis e o requisito veio pronto de duas cadeias de QA); `platform-architect`
  **dispensado** (a restrição arquitetural relevante já está decidida em `ADR-0003:157-174` e
  entra como critério 9, em vez de virar etapa).
- **Cadeia:** `tech-lead` → `backend-developer` (contrato + validador) → `researcher`
  (migração dos 3 itens: `covers` sem proveniência, `licenseNotes`, `usage`, permalink por
  SHA) → `code-reviewer` → `qa-validator`. A ordem é deliberada: o schema primeiro, a
  migração contra ele depois — o inverso produz migração que o validador reprova.
  Independência: o `researcher` produziu o arquivo original no TCK-0001 e agora o migra
  (produção, não validação); quem valida é `code-reviewer` + `qa-validator`, que não o
  escreveram.
- **Restrições passadas ao executor:**
  1. Não reverificar as fontes — TCK-0001 já aprovou URL, licença e cada alegação de
     `covers`. Refazer é retrabalho; o que muda é a **forma**.
  2. A proveniência retirada de `covers` **não se perde**: vai para o log deste ticket.
  3. Nomes de campo e valores em **en-US** (`AGENTS.md` §2a): `usage: "citable-only"`, não
     `"so-citavel"`.
  4. O validador precisa de **teste negativo por regra** (critério 6): validador que só
     concorda com o arquivo existente não prova nada — foi essa a lacuna apontada pelo QA do
     TCK-0001 ("auditoria verde não significa fonte verificada").
  5. `ADR-0003:157-174` limita o formato: nada de campo que só a aplicação saiba ler.
  6. Enquanto o TCK-0010 não concluir, o *Livro Aberto* é `citable-only` (leitura mais
     restritiva, já registrada em `ADR-0005` e em `content-standards.md`).
- **Aderência ao plano:** Fase 1 do roadmap diz textualmente "validar `meta.json`,
  `exercises.json` e `references.json` contra a realidade; **ajustar os schemas se
  necessário**". Este ticket é esse ajuste — dentro do plano, sem exceção a pedir.
- **Requisitos inegociáveis conferidos:** gratuidade (fontes gratuitas continuam sendo o
  critério de inclusão), bilinguismo (`language` permanece obrigatório e o acervo mantém
  pt-BR + en-US); a11y, offline e privacidade não aplicáveis, com o porquê no ticket.
- **Dependências:** nenhuma dura. `TCK-0010` pode mudar o `usage` do item pt-BR **depois**;
  o schema é o que torna essa mudança um campo, e não uma reescrita de prosa.
- Resultado: ok — `status: triaged`, `owner: backend-developer`. Aguardando ordem de execução.
- Lição: n/a — não resolve `REJECT`.
