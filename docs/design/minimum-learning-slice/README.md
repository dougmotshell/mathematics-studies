# Desenho — Fatia mínima de aprendizagem

Artefatos de UI/UX da spec [`minimum-learning-slice`](../../specs/minimum-learning-slice/spec.md),
produzidos no `TCK-0013`.

| Documento | O que traz |
|---|---|
| [`screen-states.md`](screen-states.md) | Os 13 estados de tela da spec, o fluxo `índice → nó → exercício`, o catálogo bilíngue de textos de interface, ordem de foco e regiões vivas. |

**O que estes documentos não fazem:** não escolhem framework, biblioteca de UI, componente
concreto nem estratégia de build (`ADR-0003` decidiu site estático com ilhas e deixou a camada
de UI em aberto); não alteram `content/`, a spec nem qualquer ADR; não introduzem conta,
login, identificador ou coleta de dado (RNF-7).

**Decisões humanas:** a forma da URL bilíngue foi **decidida** pelo usuário no `TCK-0011`
(prefixo de idioma em minúsculas no caminho, `/pt-br/…`) e está aplicada ao desenho. Continuam
**abertas**, desenhadas como alternativas e não resolvidas: exibir o nó `draft` e rótulo de
rascunho no índice — ver
[a seção correspondente](screen-states.md#12-decisões-humanas--uma-fechada-duas-abertas).
