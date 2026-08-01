# Log — TCK-0011

> Append-only. Formatos em `docs/ai/ticket-protocol.md`.

## [001] ACTION — 2026-08-01 16:00 — tech-lead
- Ação: criação do ticket a partir da ACTION A-4 do `qa-validator#4` (`TCK-0003/log.md`
  `[015]`), confirmada antes pelo `code-reviewer` em `[014]` ("Pendências e riscos"). Trecho
  de origem copiado verbatim.
- Motivo: o `ADR-0003` foi aceito e destravou a frente de plataforma, mas o desenho parou no
  nível de Contexto e o pipeline de CI/CD segue marcado `PROPOSTO` sem nenhum ADR que o
  cubra — enquanto `.github/workflows/ai-surface-audit.yml` já roda. Desenho e realidade em
  desacordo é o que produz decisão implícita na hora de implementar.
- Resultado: ok — `tickets/TCK-0011-container-architecture-and-cicd/` criado.
- Lição: n/a — não resolve `REJECT`.

## [002] ACTION — 2026-08-01 16:03 — tech-lead
- Ação: triagem. Status `new` → `triaged`. **Sem `HANDOFF`** (L-005).
- **Agrupamento (justificativa em uma linha):** o diagrama de Container e a decisão de CI/CD
  são a mesma pergunta vista de dois lados — a caixa "build → host" só para de ser um
  retângulo vago quando alguém decide onde o CI roda e o que ele executa —, têm o mesmo dono
  e o mesmo prazo (antes do primeiro ticket de implementação), e separá-los faria o diagrama
  nascer já com um `PROPOSTO` órfão, que é justamente o defeito que ele vem consertar.
- **Tipo:** `infra`. É desenho e decisão de build/deploy/ambientes. **Desvio de cadeia
  justificado:** a cadeia padrão de `infra` é `devops-engineer`, mas o entregável aqui é
  **arquitetura e ADR** — área exclusiva do `platform-architect` (AGENTS.md §10). O
  `devops-engineer` entra no ticket **seguinte**, para implementar o que o ADR-0006 decidir.
- **Prioridade P3 · tamanho M.** P3 porque nada em curso depende disto: a Fase 1 é de
  conteúdo, e a aplicação não existe (`find . -name package.json` → vazio). O prazo é
  **relativo, não temporal**: fechar antes do primeiro ticket de implementação da Fase 2.
  Rebaixar para P3 é decisão consciente — trabalhar arquitetura antes do conteúdo inverteria a
  ordem deliberada do `docs/product/roadmap.md` ("o contrato de conteúdo vem antes da
  aplicação").
- **Owner: `platform-architect`.** Arquitetura, dados, deploy e ADRs.
- **Cadeia:** `tech-lead` → `platform-architect` → `code-reviewer` → `qa-validator`. O aceite
  do ADR-0006 **não** faz parte do `done`: aceitar é ato do usuário, como foi o `ADR-0003`
  (que precisou de ticket próprio, TCK-0003). O ticket entrega o ADR `proposed` com
  recomendação — assim ele fecha sem depender de resposta humana, e a pergunta ao usuário fica
  registrada em "Perguntas em aberto".
- **Restrições passadas ao executor:**
  1. **L-011 e L-013 são o risco central deste ticket:** o TCK-0003 gastou dois loops porque
     um rótulo de Mermaid decidia o que o texto dizia não decidir. Diagrama é normativo
     (`docs/DOC-STANDARDS.md`) — cada caixa tem de ser resultado decidido ou `PROPOSTO` com
     ADR nomeado.
  2. O container tem de caber no `ADR-0003` já aceito: independência do contrato de dados
     (`:157-174`) e portabilidade do host estático (`:151-155`). Contradizer o ADR aceito é
     defeito bloqueante, não sugestão.
  3. **Custo zero com fonte** (critério 6): limite do plano gratuito citado com URL e data —
     afirmação de gratuidade sem fonte é o tipo de coisa que envelhece em silêncio.
  4. Não criar nem alterar `.github/workflows/` (critério 9) e não escolher biblioteca de UI,
     de teste ou estratégia de service worker.
  5. Telemetria e backend continuam fora: exigem ADR próprio (`ADR-0003:143-145`).
- **Aderência ao plano:** Fase 2 do roadmap ("Leitor de conteúdo") pressupõe build, deploy e
  PWA; este ticket é o pré-requisito documental dela, não uma antecipação de implementação.
  Dentro do plano.
- **Requisitos inegociáveis conferidos:** offline/PWA entra como elemento obrigatório do
  diagrama; custo zero vira critério com evidência; privacidade fica protegida por proibição
  explícita de introduzir telemetria; bilinguismo aparece como rotas por idioma. a11y e
  correção matemática não são acionados, com o porquê registrado no ticket.
- **Dependências:** nenhuma dura. Se o `TCK-0008` ainda não tiver rodado, atenção: parte da
  superfície de IA ainda descreve a stack como indecidida e pode induzir o executor a
  hesitar — o `ADR-0003` está `accepted` desde 2026-08-01.
- Resultado: ok — `status: triaged`, `owner: platform-architect`. Aguardando ordem de execução.
- Lição: n/a — não resolve `REJECT`.
