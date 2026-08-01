# Memória do agente `i18n-steward`

> Memória persistente deste agente, mantida por ele próprio ao final de tarefas
> significativas. Índice geral: `memory/MEMORY.md` · lições: `memory/LESSONS.md` ·
> contexto da área: `memory/context/`.

## Papel

Garante paridade e qualidade das versões pt-BR e en-US de todo conteúdo e da interface — mesmas seções, mesma matemática, convenções locais corretas (vírgula/ponto decimal, nomes de teoremas, terminologia). Usar antes de publicar e em auditorias de idioma.

## Notas persistentes

- **Paridade de descrição de fórmula se verifica por posição, não por contagem.** Contar
  `*Leitura:*` = contar `*Reading:*` não prova paridade: prova só que os totais batem. O que
  prova é `grep -n '^\$\$\|^\*Leitura:\*'` nos dois arquivos e conferir a **alternância
  estrita** fórmula → descrição em cada um — assim se pega a fórmula descrita em um idioma e
  não no outro, que é o defeito real. Complementa a L-012, que trata do mesmo grep pela ótica
  do autor.
- **Afirmação de convenção numérica se confere por comando.** Quando o autor declara "não há
  decimal, a regra vírgula × ponto não se aplica", rodar
  `grep -E '[0-9]+[.,][0-9]+'` sobre as descrições. É barato e é exatamente o tipo de
  afirmação que passa despercebida quando aceita de palavra.
- **Comparar o LaTeX entre os dois idiomas, não só contra o HEAD.** Extrair os blocos `$$…$$`
  dos dois arquivos e compará-los par a par (script curto em Python) revela divergência que o
  `git diff` não mostra, porque cada arquivo pode estar "correto" em relação a si mesmo.
  Divergência legítima existe: prosa dentro do LaTeX (`\text{ou}` × `\text{or}`) **deve**
  ser localizada; símbolo e estrutura, nunca.
- **Nome de resultado por idioma (Girard × Vieta):** o par consolidado neste repositório é
  "relações de Girard" (pt-BR) × "Vieta's formulas" (en-US). Conferir com
  `grep -i vieta theory.pt-BR.md` e `grep -i girard theory.en-US.md` — os dois devem sair
  vazios. Descrição de fórmula que **não** nomeia o resultado é preferível: evita duplicar o
  ponto de manutenção do par de nomes.
- **Subscrito — parecer emitido em 2026-08-01 (TCK-0005):** par `x índice 1` (pt-BR) ×
  `x subscript 1` (en-US) aprovado como equivalente. `subscript` é a forma consagrada em
  en-US; `índice` é a corrente em pt-BR escolar. Evitar os decalques *index* (en-US) e
  "subscrito" (pt-BR, aceitável mas menos idiomático). **Ressalva:** "índice" é sobrecarregado
  em pt-BR — é também o índice do radical ($\sqrt[n]{\,}$); quando o acervo descrever radicais
  de índice n, o glossário vai precisar da desambiguação.
  **Pendente:** linha `subscrito (índice) | subscript` em `docs/content/i18n.md` + lição de
  terminologia. Não escrita ainda de propósito: no momento do parecer o TCK-0005 estava
  `in_review` com duas revisões paralelas em curso, e `docs/` estava sob edição de outro
  agente. Fixar convenção antes de o ticket fechar seria codificar decisão que ainda pode ser
  devolvida. Retomar quando o TCK-0005 chegar a `done`.
- **Distinguir defeito de paridade de preferência de registro.** "open/close parenthesis" ×
  "left/right parenthesis" (MathSpeak) é escolha de leitura, dona do `a11y-ux-reviewer`, não
  minha: trocar só o en-US **não** quebra a paridade, porque "abre/fecha parênteses" continua
  correto em pt-BR. Reportar como observação, nunca como `REJECT`. O mesmo vale para escolha
  simétrica nos dois idiomas (algarismo `1` em "x índice 1"/"x subscript 1"): simétrico não é
  defeito meu — mas, se mudar, tem de mudar nos dois arquivos ao mesmo tempo.

## Últimas execuções

| Data | Ticket/Tarefa | Resultado | Lição relacionada |
|---|---|---|---|
| 2026-08-01 | TCK-0005 — paridade das 8 descrições de fórmula do nó piloto `quadratic-equations` (critério 4) | **APROVADO**, log `[007]`; 5 pares novos equivalentes, cobertura simétrica por posição, sem decimal acionando a regra vírgula × ponto, Girard/Vieta sem mistura; convenção de subscrito aprovada com ressalva de sobrecarga de "índice" | L-012 (relacionada) |
