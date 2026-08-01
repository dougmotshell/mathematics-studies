# Arquitetura

Diagramas C4 em Mermaid, um arquivo por nível/escopo. Criar/atualizar com `/c4-diagram`,
seguindo [`../DOC-STANDARDS.md`](../DOC-STANDARDS.md).

| Documento | Nível | Estado |
|---|---|---|
| [c4-context.md](c4-context.md) | Context | Decidido, exceto CI/CD e previews por branch (`ADR-0006`, `proposed`) — stack aceita em ADR-0003, 2026-08-01 |
| [c4-container.md](c4-container.md) | Container | Decidido pelo ADR-0003; automação de build/deploy `PROPOSTO` (`ADR-0006`) e esqueleto concreto `PROPOSTO` (`ADR-0007`) — nada implementado |

> Regra permanente: elemento ainda não decidido é marcado no diagrama — não desenhar hipótese
> como se fosse fato, e o marcador tem de citar a fonte pendente. Três marcadores em uso:
> **sem marcador** = sustentado por ADR aceito ou spec aprovada, com a fonte citada no próprio
> rótulo; `PROPOSTO (ADR-NNNN)` = depende de aceite; `EM ABERTO (ticket)` = ninguém decide por
> ADR, de propósito, e a escolha é do ticket de implementação (biblioteca de UI, ferramenta de
> teste, mecanismo da camada offline, momento em que a matemática vira HTML, **lugar** do
> portão de validação do acervo). Marcador em um contêiner vale para as relações que decorrem
> dele; relação que afirme algo além do contêiner precisa de marcador próprio.
>
> Marcar **de menos** e **de mais** são o mesmo defeito (L-013): rotular como hipótese algo que
> um ADR aceito já exige engana tanto quanto omitir o marcador de um mecanismo em aberto.
>
> Falta o nível **Component**, que só faz sentido depois que houver aplicação.
