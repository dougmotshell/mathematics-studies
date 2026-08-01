# `src/islands/` — interatividade, com fronteira explícita

Reservado pelo `ADR-0007` §6. Regras que valem para toda ilha:

- uma ilha por unidade interativa; o alternador de idioma **não** é ilha (é link entre
  rotas estáticas);
- a ilha recebe **dados já validados como propriedade**, serializados na build, e
  **não faz requisição de rede** — é o que a torna utilizável offline;
- página de teoria sem exercício não carrega ilha nenhuma;
- recurso que exija hidratar a página inteira está mal desenhado e volta para redesenho
  (`ADR-0003`).

Vazio de propósito: a primeira ilha é o player de exercícios (tasks 7–8 de
`docs/specs/minimum-learning-slice/`).
