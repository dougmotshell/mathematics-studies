# Memória do agente `product-analyst`

> Memória persistente deste agente, mantida por ele próprio ao final de tarefas
> significativas. Índice geral: `memory/MEMORY.md` · lições: `memory/LESSONS.md` ·
> contexto da área: `memory/context/`.

## Papel

Refina pedidos em requisitos claros e critérios de aceite verificáveis, confrontando-os com a visão do produto, o roadmap e as specs. Usar quando um ticket chega ambíguo ou quando é preciso decidir o que entra na menor fatia entregável.

## Notas persistentes

- **Requisito nasce do contrato de dados, não da imaginação.** Ler `meta.json` e
  `exercises.json` do nó piloto antes de escrever RF: os campos reais (`options[].feedback`,
  `answer`/`tolerance`, `hints[]`, `solution`, `status: "draft"`) geram critérios
  falsificáveis com ids concretos (`qe-001`…`qe-005`). Critério que cita dado real não vira
  intenção vaga.
- **Enquanto `ADR-0003` estiver `proposed`**, todo requisito é comportamento + contrato de
  dados. O que depender de stack vai para uma lista explícita "a definir no aceite do ADR"
  (renderização, forma da URL bilíngue, cache/service worker, build, ferramentas de teste,
  números de performance) — assim a spec não trava nem antecipa a decisão.
- **Armadilhas do acervo já detectadas:** vírgula decimal pt-BR × ponto en-US na entrada
  numérica; `prerequisites: []` não pode virar seção vazia; `unit: null`; gabarito visível no
  payload por não haver backend; `status: "draft"` exige rótulo em vez de esconder o nó.
- **Paridade sem fallback** (`L-001`) e **slug como URL pública** (`L-003`) entram como RNF em
  toda fatia que toque `content/` — não como observação solta.

## Últimas execuções

| Data | Ticket/Tarefa | Resultado | Lição relacionada |
|---|---|---|---|
| 2026-08-01 | TCK-0002 / dev-loop `minimum-learning-slice`, etapa `plan` | Requisito da fatia mínima refinado: escopo, RF-1…RF-18, RNF-1…RNF-11, 13 estados de tela, CA-1…CA-16 e entrega do `docs-writer` em `.dev-loop/minimum-learning-slice/requirements.md`; handoff `[005]` para `docs-writer` | L-001, L-003, L-005 |
