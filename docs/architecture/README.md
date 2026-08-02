# Arquitetura

Diagramas C4 em Mermaid, um arquivo por nível/escopo. Criar/atualizar com `/c4-diagram`,
seguindo [`../DOC-STANDARDS.md`](../DOC-STANDARDS.md).

| Documento | Nível | Estado |
|---|---|---|
| [c4-context.md](c4-context.md) | Context | Decidido — ADR-0003 (stack), ADR-0006 (CI/CD, previews, deploy), todos `accepted` em 2026-08-01; sem marcador `PROPOSTO` |
| [c4-container.md](c4-container.md) | Container | Decidido — ADR-0003, ADR-0006 e ADR-0007, `accepted` em 2026-08-01; sem marcador `PROPOSTO`. Restam itens `EM ABERTO (ticket)`; implementação em curso pelo TCK-0015 |

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
