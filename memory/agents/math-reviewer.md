# Memória do agente `math-reviewer`

> Memória persistente deste agente, mantida por ele próprio ao final de tarefas
> significativas. Índice geral: `memory/MEMORY.md` · lições: `memory/LESSONS.md` ·
> contexto da área: `memory/context/`.

## Papel

Revisa rigor matemático — definições, enunciados, demonstrações, contra-exemplos, hipóteses omitidas e gabaritos de exercícios. Usar antes de publicar qualquer conteúdo e sempre que houver dúvida sobre a corretude de uma afirmação.

## Notas persistentes

- **Leitura adversarial de descrição de fórmula** (o método que pega o erro silencioso):
  reconstruir o LaTeX **a partir do texto isolado**, sem olhar a fórmula, e só então comparar.
  Divergência de sinal, agrupamento, ordem de operações ou escopo é defeito; diferença apenas
  de espaçamento (`\qquad`, `\quad`, `\;`) ou de pontuação do parágrafo, não.
- **Nem toda ambiguidade é defeito.** Antes de reprovar, testar se o parse hostil muda o
  **valor**: "menos b dividido por a" admite `-(b/a)` e `(-b)/a`, iguais para `a \neq 0` —
  logo é escolha tipográfica, não erro. Reprovar ambiguidade que não altera resultado gasta
  loop do ticket e não protege ninguém.
- **Hipótese omitida costuma ser mal-formação, não falsidade** — por isso nenhuma verificação
  numérica a detecta (não existe contra-exemplo para exibir). Pergunta operacional: *para
  quais parâmetros admissíveis o lado direito deixa de denotar algo?* (L-014).
- **Defeito fora do diff não vira `REJECT`** do ticket que não o tem em escopo: vira achado
  com severidade + encaminhamento ao `tech-lead` para ticket próprio, e uma condição explícita
  ("corrigir antes de o nó sair de `draft`"). Aprovar o ticket e registrar o achado são coisas
  independentes.
- **Ambiente:** SymPy **não** instalado (`memory/context/content.md`). Verificação em Python
  puro com `fractions.Fraction` (aritmética exata) resolve álgebra elementar: discriminante,
  raízes, substituição de volta, unicidade do conjunto-solução. Declarar a limitação quando a
  afirmação for simbólica geral (L-002).
- **Verificar também a unicidade**, não só a corretude: em "para quais `k`…", conferir que não
  há terceiro valor; em múltipla escolha, que nenhum distrator é uma segunda resposta correta.
- **Alocar `L-NNN` no momento de escrever**, relendo `memory/LESSONS.md` — em revisões
  paralelas outro agente registra lição no intervalo (aconteceu no TCK-0005: L-013 colidiu,
  virou L-014 via `CORRECTION`).
- **Escopo em revisão paralela:** paridade é do `i18n-steward` e qualidade de escuta é do
  `a11y-ux-reviewer`. Meu veredito cobre corretude, reconstrutibilidade e "nenhuma afirmação
  matemática nova" — não opinar no resto.

## Últimas execuções

| Data | Ticket/Tarefa | Resultado | Lição relacionada |
|---|---|---|---|
| 2026-08-01 | TCK-0005 — descrições textuais das 8 fórmulas do nó piloto `quadratic-equations` | **APROVADO** (rigor): 10/10 descrições reconstroem o LaTeX; aritmética conferida em Python exato; LaTeX intocado (0 remoções no diff). Achado herdado — enunciado do teorema sem `\Delta \ge 0` julgado **imprecisão didática `menor`**, não erro: não há contra-exemplo, e a tabela de sinais está na mesma sentença. Não bloqueia; encaminhado ao `tech-lead` para ticket próprio, a corrigir antes de o nó sair de `draft`. | L-014 (nova), L-012, L-002 |
