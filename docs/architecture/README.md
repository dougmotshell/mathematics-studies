# Arquitetura

Diagramas C4 em Mermaid, um arquivo por nível/escopo. Criar/atualizar com `/c4-diagram`,
seguindo [`../DOC-STANDARDS.md`](../DOC-STANDARDS.md).

| Documento | Nível | Estado |
|---|---|---|
| [c4-context.md](c4-context.md) | Context | Decidido, exceto CI/CD e previews por branch (marcados como propostos) — stack aceita em ADR-0003, 2026-08-01 |

> Regra permanente: elemento ainda não decidido em ADR aceito é marcado como **proposto** no
> diagrama — não desenhar hipótese como se fosse fato. Com o `ADR-0003` aceito, a aplicação
> deixou de ser hipótese; falta o nível **Container** (site estático, ilhas de
> interatividade, IndexedDB), ainda não desenhado.
