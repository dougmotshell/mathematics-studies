---
name: a11y-audit
description: Audita acessibilidade da plataforma e do conteúdo — WCAG 2.2 AA, matemática acessível a leitor de tela, navegação por teclado, contraste, foco e alternativas textuais. Usar antes de publicar interface ou conteúdo visual.
---

# Auditar acessibilidade

Acessibilidade é requisito do projeto, não acabamento (AGENTS.md §1).

## 1. Conteúdo (sempre possível, sem browser)

- [ ] Toda equação em **display** tem leitura textual **integral** associada (parágrafo
      `*Leitura:*` / `*Reading:*`, `aria-label` ou descrição no `alt`), conferida por
      **posição** e não por contagem: a alternância bloco → descrição não pode ter órfão
      (`L-012`)
- [ ] Toda fórmula **inline** marcada como *exige* pelo **teste de marcação de agrupamento**
      (`docs/content/accessibility.md`) tem o agrupamento dito em palavras. Varrer **as duas
      partes**: (a) argumento composto — `\frac`, `\dfrac`, `\sqrt`, `^{…}` com mais de um
      símbolo; (b) base elevada ambígua — `grep -nF ')^'` e sinal **unário** antes de base
      elevada (`$-x^2$`, que **não** tem argumento composto). Em `theory.<lang>.md`,
      `exercises.json` e `assessments.json`, nos dois idiomas, fora de `$$…$$`
- [ ] Nenhuma fórmula existe **apenas** como imagem
- [ ] Imagens e gráficos têm `alt` que descreve o **conteúdo matemático**, não o arquivo
- [ ] Tabelas têm cabeçalho semântico e são compreensíveis linearmente
- [ ] Não há informação transmitida **só por cor** (ex.: "a curva vermelha")
- [ ] Linguagem clara, frases curtas, instruções antes da tarefa
- [ ] Idioma declarado corretamente por documento (`lang`)

## 2. Interface (quando há aplicação rodando)

Com o MCP `chrome-devtools` disponível, navegue até a página e verifique:

- [ ] Operação completa por **teclado** (Tab/Shift+Tab/Enter/Espaço/setas), sem armadilha de
      foco
- [ ] **Foco visível** em todos os elementos interativos
- [ ] Ordem de foco lógica; landmarks e headings hierárquicos
- [ ] **Contraste** ≥ 4.5:1 (texto) e ≥ 3:1 (componentes/gráficos)
- [ ] Alvos de toque ≥ 24×24 px (WCAG 2.2 – 2.5.8)
- [ ] Erros de formulário anunciados e associados ao campo
- [ ] `prefers-reduced-motion` respeitado; nada pisca > 3×/s
- [ ] Zoom até 200% sem perda de conteúdo ou scroll horizontal
- [ ] KaTeX emitindo MathML/`aria` utilizável por leitor de tela

Rode também o audit automatizado (Lighthouse/axe) e trate o resultado como **piso**, nunca
como prova de acessibilidade.

## 3. Público específico

Há crianças e pessoas neurodivergentes no público: sem dependência de tempo para responder,
sem animação intrusiva, feedback não punitivo, possibilidade de repetir a instrução.

## 4. Saída

Por achado: **local**, **critério WCAG** (ex.: 2.4.7 Focus Visible), **impacto (para quem)**,
**severidade** (`bloqueante | importante | menor`) e **correção sugerida**. Declarar
explicitamente o que **não** foi verificado (ex.: "sem browser disponível; interface não
testada").
