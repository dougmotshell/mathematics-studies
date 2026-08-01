# Acessibilidade do conteúdo e da plataforma

Meta: **WCAG 2.2 nível AA** como piso, com atenção extra à acessibilidade da **matemática**.
Acessibilidade é requisito de entrada, não correção posterior.

## Matemática acessível

| Regra | Por quê |
|---|---|
| Fórmula sempre em **KaTeX**, nunca só imagem | Imagem é opaca para leitor de tela, zoom e busca |
| Toda equação em **display** tem descrição textual próxima | Leitor de tela lê a descrição; quem tem dificuldade de leitura simbólica se apoia nela |
| Notação não óbvia declarada na primeira ocorrência | Evita interpretação errada na leitura linear |
| Passo a passo em lista, não em imagem única | Permite navegação item a item |
| Gráficos com `alt` descrevendo o **conteúdo matemático** | "Parábola com vértice em $(2,-1)$, concavidade para cima" — não "gráfico 3" |
| Tabelas com cabeçalho semântico | Leitura linear compreensível |

Exemplo de descrição aceitável para uma equação em display:

> $$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$
> *Leitura:* x é igual a menos b, mais ou menos a raiz quadrada de b ao quadrado menos quatro
> a c, tudo dividido por dois a.

## Interface

- **Teclado**: toda ação possível sem mouse; ordem de foco lógica; sem armadilha de foco.
- **Foco visível** em todos os elementos interativos.
- **Contraste**: ≥ 4.5:1 para texto; ≥ 3:1 para componentes e elementos gráficos.
- **Alvos de toque** ≥ 24×24 px (WCAG 2.2 – 2.5.8).
- **Zoom** até 200% sem perda de conteúdo nem scroll horizontal do corpo da página.
- **Sem informação só por cor** (nunca "a curva vermelha" como única referência).
- **Erros de formulário** anunciados e associados ao campo.
- `prefers-reduced-motion` respeitado; nada pisca mais de 3×/s.
- Idioma declarado por documento (`lang`) e trocado corretamente na alternância pt-BR/en-US.

## Público específico

O acervo atende crianças e pessoas neurodivergentes. Portanto:

- instruções curtas, antes da tarefa, em linguagem clara;
- **sem dependência de tempo** para responder;
- feedback **não punitivo** — erro é informação, não derrota;
- possibilidade de repetir a instrução e de pausar;
- sem animação intrusiva, som automático ou elemento que roube o foco.

## Verificação

| Camada | Como |
|---|---|
| Conteúdo | `/a11y-audit` (parte 1) — descrições, `alt`, cor, clareza |
| Interface | `/a11y-audit` (parte 2) com MCP `chrome-devtools`; Lighthouse/axe como piso |
| Regressão | `qa-validator` inclui navegação por teclado e leitura de fórmulas nos casos hostis |

Ferramenta automatizada detecta uma fração dos problemas: aprovação no Lighthouse **não** é
prova de acessibilidade. Sempre declarar o que não foi verificado.
