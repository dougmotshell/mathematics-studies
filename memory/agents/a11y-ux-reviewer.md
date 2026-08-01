# Memória do agente `a11y-ux-reviewer`

> Memória persistente deste agente, mantida por ele próprio ao final de tarefas
> significativas. Índice geral: `memory/MEMORY.md` · lições: `memory/LESSONS.md` ·
> contexto da área: `memory/context/`.

## Papel

Revisa acessibilidade (WCAG 2.2 AA, matemática acessível a leitor de tela, teclado, contraste) e UX de aprendizagem (carga cognitiva, feedback, navegação, progresso). Usar antes de publicar interface ou conteúdo com forte componente visual.

## Notas persistentes

### Como revisar descrição de fórmula (método que funcionou no TCK-0005)

1. **Ordem antes de contagem** (L-012): `grep -n '^\$\$\|^\*Leitura:\*'` e conferir
   alternância estrita. Contagem igual não prova correspondência.
2. **Teste adversarial de reconstrução**: ler só a descrição, escrever o LaTeX que ela
   induz, comparar com o bloco. Fazer isso descrição a descrição e registrar o LaTeX
   reconstruído no log — é a única evidência verificável do critério "dá para reconstruir".
3. **Ambiguidade só é defeito quando as duas leituras produzem expressões diferentes.**
   "menos b dividido por a" para $-\frac{b}{a}$ parece o defeito clássico de agrupamento,
   mas $-(b/a) = (-b)/a$: mesma expressão, zero risco. Já "menos b mais ou menos raiz de
   delta dividido por dois a" sem o "tudo" é defeito real, porque
   $\frac{-b\pm\sqrt\Delta}{2a} \neq -b \pm \frac{\sqrt\Delta}{2a}$. Testar a divergência
   antes de acusar — acusar ambiguidade inócua queima crédito da revisão.
4. **Onde a ambiguidade costuma estar de verdade**: escopo de expoente sobre negativo
   ($(-5)^2$), fim do numerador, fim do radicando, cadeia de relações (`= 1 > 0`), direção
   da implicação, e subscrito não verbalizado.
5. **Carga auditiva**: julgar por âncoras, não por comprimento. Descrição longa com
   separadores por elo (";", "tudo dividido por", "o que implica") é aceitável; descrição
   curta sem marcador de agrupamento não é.
6. `scripts/audit-content.sh` **não** checa descrição de fórmula — auditoria verde não é
   evidência aqui.

### Convenções de leitura decididas por mim (TCK-0005) — pendentes de registro em `docs/content/accessibility.md`

- Subscrito: **"x índice 1"** (pt-BR) / **"x subscript 1"** (en-US) — aprovado. Ressalva
  obrigatória junto: radical de índice n lê-se "raiz de índice n de …", nunca "índice n"
  solto, senão "índice" colide entre subscrito e índice de radical.
- Fração: numerador composto → "tudo dividido por" / "all divided by"; numerador de um token
  → "dividido por" / "divided by".
- Parênteses sempre falados; `\cdot` → "vezes"/"times" e justaposição mantida justaposta;
  `\Longrightarrow` → "o que implica" / "which implies"; relação encadeada com "que é" /
  "which is"; números por extenso.
- Regra geral nova: **quando o ponto matemático é o agrupamento, o texto ao redor precisa
  dizê-lo em palavras** — a fórmula sozinha, lida linearmente, apaga o contraste.

### Limites do ambiente

- Sem MCP `chrome-devtools` neste repositório até 2026-08-01: só a parte 1 do `/a11y-audit`
  (conteúdo) é verificável. MathML do KaTeX, locução real, foco, contraste, zoom e alvos de
  toque **não** foram verificados nenhuma vez ainda. Declarar isso sempre no log.
- Risco de arquitetura já identificado e não resolvido: com KaTeX emitindo MathML, o usuário
  de leitor de tela ouve a fórmula **e** a descrição `*Leitura:*` — duplicação a cada bloco.
  Solução é de renderização (`aria-describedby`, divulgação progressiva ou suprimir uma das
  leituras) e depende de ADR-0003 (`proposed`). Levantar antes do primeiro render.

### Disciplina de escopo em revisão paralela

- Em revisões simultâneas sobre o mesmo artefato (TCK-0005: `math-reviewer` ‖ `i18n-steward`
  ‖ este agente), escrever só a própria entrada de log, não renumerar as outras, não opinar
  sobre rigor nem paridade, e não editar `docs/` — recomendação vira item para ticket
  próprio.
- Achado em linha **não tocada** pela entrega = ticket próprio, nunca `REJECT` da entrega.
  Separar isso explicitamente no log evita devolução injusta e não perde o achado.

## Lição a promover para `memory/lessons/`

`accessible-formula-reading-is-verified-by-reconstruction` — o teste de uma descrição de
fórmula é reconstruir o LaTeX de ouvido, e ambiguidade só é defeito quando as duas leituras
divergem como expressão. Não registrada em `memory/lessons/` na hora por causa das duas
revisões paralelas em curso (colisão nos índices `LESSONS.md`/`MEMORY.md`); encaminhada ao
`retrospective-curator` no fechamento do TCK-0005.

## Últimas execuções

| Data | Ticket/Tarefa | Resultado | Lição relacionada |
|---|---|---|---|
| 2026-08-01 | TCK-0005 — revisão de a11y das 10 descrições novas do nó piloto (critério 3) | APROVADO; convenção de subscrito aprovada; 5 achados para ticket próprio | aplicada L-012 |
