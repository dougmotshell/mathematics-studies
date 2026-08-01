# Memória do agente `content-author`

> Memória persistente deste agente, mantida por ele próprio ao final de tarefas
> significativas. Índice geral: `memory/MEMORY.md` · lições: `memory/LESSONS.md` ·
> contexto da área: `memory/context/`.

## Papel

Escreve a teoria didática bilíngue (pt-BR + en-US) de um nó de conteúdo, seguindo a estrutura mínima do projeto — objetivo, pré-requisitos, intuição, definição formal, exemplos resolvidos, erros comuns e resumo. Usar para criar ou revisar theory.*.md.

## Notas persistentes

- **Descrição de fórmula em display (`*Leitura:*` / `*Reading:*`) faz parte da entrega, não é
  passe posterior.** O padrão do repositório está fixado em `docs/content/accessibility.md` e
  no nó piloto: parágrafo em itálico imediatamente após o bloco `$$…$$`, começando por
  `*Leitura:*` em pt-BR e `*Reading:*` em en-US.
- **Critério de leitura adotado (TCK-0005):** ler a estrutura da esquerda para a direita, na
  ordem escrita, com agrupamento explícito (`abre/fecha parênteses`, `tudo dividido por`),
  relações (`igual a`, `maior/menor que`), implicação (`o que implica` para `\Longrightarrow`)
  e índice (`x índice 1` / `x subscript 1`). Números por extenso. **Nomear a fórmula não é
  descrever** ("a fórmula de Bhaskara" é descrição ruim).
- Verificação barata de que nenhuma fórmula ficou órfã:
  `grep -n '^\$\$\|^\*Leitura:\*\|^\*Reading:\*' <arquivo>` — a saída tem de alternar
  estritamente fórmula → descrição. Contagem sozinha não prova ordem.
- **Só acrescentar texto se prova com o diff:** `git diff -U0 -- content/ | grep -E '^-[^-]'`
  vazio é a evidência objetiva de que o LaTeX não foi tocado. Vale citar no log.
- Quando encontro problema matemático fora do escopo do ticket, **não conserto** — registro no
  `HANDOFF` como observação e deixo a decisão para o `math-reviewer`/`tech-lead`.
- `bash scripts/audit-content.sh` **não** verifica descrição de fórmula (nem referência de
  verdade). Auditoria verde não substitui a checagem manual acima.

## Últimas execuções

| Data | Ticket/Tarefa | Resultado | Lição relacionada |
|---|---|---|---|
| 2026-08-01 | TCK-0005 — descrições textuais das 8 fórmulas em display do nó piloto | 5 descrições acrescentadas por idioma (3→8/8); diff só de inserções; auditoria 0 erros/0 avisos; handoff para `math-reviewer` | — |
