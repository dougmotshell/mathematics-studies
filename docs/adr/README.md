# Decisões arquiteturais (ADRs)

Registro numerado e imutável das decisões do projeto. Formato: `ADR-NNNN-short-title.md`,
criado a partir de [`adr-template.md`](adr-template.md) com a skill `/create-adr`.

**Status possíveis:** `proposed` · `accepted` · `deprecated` · `superseded by ADR-MMMM`.
Um ADR nunca é reescrito para mudar a decisão — cria-se um novo que o substitui.

| ADR | Título | Status | Data |
|---|---|---|---|
| [ADR-0001](ADR-0001-content-taxonomy.md) | Taxonomia de conteúdo por estágio, área e tópico | accepted | 2026-08-01 |
| [ADR-0002](ADR-0002-bilingual-content.md) | Bilinguismo obrigatório pt-BR/en-US | accepted | 2026-08-01 |
| [ADR-0003](ADR-0003-platform-stack.md) | Stack da plataforma web/PWA | accepted | 2026-08-01 |
| [ADR-0004](ADR-0004-ticket-driven-agent-workflow.md) | Desenvolvimento orientado a tickets com agentes | accepted | 2026-08-01 |
| [ADR-0005](ADR-0005-project-license.md) | Licença do projeto: CC BY-SA 4.0 (conteúdo) e MIT (código) | accepted | 2026-08-01 |
| [ADR-0006](ADR-0006-continuous-integration-and-publication.md) | Integração contínua, previews e publicação | proposed | 2026-08-01 |
| [ADR-0007](ADR-0007-application-skeleton.md) | Esqueleto da aplicação: gerador concreto, diretórios e leitura do acervo | proposed | 2026-08-01 |

> `ADR-0003` foi aceito em 2026-08-01: a frente de plataforma está destravada. Backend,
> conta, login e telemetria identificável continuam **fora** do escopo decidido — cada um
> exige ADR próprio.
