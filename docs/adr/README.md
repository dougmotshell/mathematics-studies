# Decisões arquiteturais (ADRs)

Registro numerado e imutável das decisões do projeto. Formato: `ADR-NNNN-short-title.md`,
criado a partir de [`adr-template.md`](adr-template.md) com a skill `/create-adr`.

**Status possíveis:** `proposed` · `accepted` · `deprecated` · `superseded by ADR-MMMM`.
Um ADR nunca é reescrito para mudar a decisão — cria-se um novo que o substitui.

**Emenda editorial (convenção).** A imutabilidade tem por objeto a **decisão**, não a redação.
Quando um ADR posterior torna **falsa uma ilustração** de um ADR já aceito — rótulo de
diagrama, exemplo, número citado de passagem —, corrige-se a ilustração e declara-se a correção
numa linha **Emenda editorial (data, TCK-NNNN)** no cabeçalho, dizendo o que exibia, o que
passou a exibir e que nenhuma decisão mudou. Duas regras: (a) a emenda só vale para o que o ADR
**não** decide — se a frase falsa for a decisão, o caminho é `superseded`; (b) manter a
ilustração errada com uma nota dizendo o contrário é **pior**, porque diagrama é normativo
(`docs/DOC-STANDARDS.md`) e o leitor obedece ao rótulo. Precedente: `ADR-0003` (TCK-0016).

| ADR | Título | Status | Data |
|---|---|---|---|
| [ADR-0001](ADR-0001-content-taxonomy.md) | Taxonomia de conteúdo por estágio, área e tópico | accepted | 2026-08-01 |
| [ADR-0002](ADR-0002-bilingual-content.md) | Bilinguismo obrigatório pt-BR/en-US | accepted | 2026-08-01 |
| [ADR-0003](ADR-0003-platform-stack.md) | Stack da plataforma web/PWA | accepted | 2026-08-01 |
| [ADR-0004](ADR-0004-ticket-driven-agent-workflow.md) | Desenvolvimento orientado a tickets com agentes | accepted | 2026-08-01 |
| [ADR-0005](ADR-0005-project-license.md) | Licença do projeto: CC BY-SA 4.0 (conteúdo) e MIT (código) | accepted | 2026-08-01 |
| [ADR-0006](ADR-0006-continuous-integration-and-publication.md) | Integração contínua, previews e publicação | accepted | 2026-08-01 |
| [ADR-0007](ADR-0007-application-skeleton.md) | Esqueleto da aplicação: gerador concreto, diretórios e leitura do acervo | accepted | 2026-08-01 |

> `ADR-0003` foi aceito em 2026-08-01: a frente de plataforma está destravada. Backend,
> conta, login e telemetria identificável continuam **fora** do escopo decidido — cada um
> exige ADR próprio.
>
> `ADR-0006` e `ADR-0007` foram aceitos em 2026-08-01 (TCK-0016): pipeline, previews por PR,
> deploy no push em `main`, projeto Astro na raiz e URL `/pt-br/` · `/en-us/` deixam de ser
> hipótese. O aceite **não** fecha o que esses ADRs decidiram não decidir — biblioteca de UI,
> ferramenta de teste, camada offline, momento em que a matemática vira HTML e o **lugar** do
> portão de validação do acervo continuam sendo decisão do ticket.
