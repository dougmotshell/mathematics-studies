# Memória do agente `ui-ux-designer`

> Memória persistente deste agente, mantida por ele próprio ao final de tarefas
> significativas. Índice geral: `memory/MEMORY.md` · lições: `memory/LESSONS.md` ·
> contexto da área: `memory/context/`.

## Papel

Projeta fluxos, telas, design system e microinterações da plataforma, com foco em carga cognitiva, acessibilidade e público amplo (crianças a pesquisadores). Usar antes de implementar interface nova ou ao redesenhar uma experiência.

## Notas persistentes

- **Onde vive o desenho:** `docs/design/<slug-da-spec>/` (diretório criado em 2026-08-01, no
  `TCK-0013`). Um documento por spec; a spec continua sendo a fonte dos requisitos, o desenho
  só decide estrutura, texto, foco e anúncio.
- **Regra fixada no `TCK-0013`, reutilizar:** para um mesmo evento, **mover foco OU anunciar
  por região viva — nunca os dois**. Não é só redundância: região viva educada é descartada ou
  embaralhada quando o foco muda no mesmo instante, então o texto "anunciado" pode nunca ser
  ouvido. Move foco quando o aluno pediu conteúdo longo (solução) ou precisa agir noutro lugar
  (nova tentativa); anuncia quando a ação se repete no mesmo controle (dica, resultado). Quando
  o foco se move, **a mensagem viaja com o destino do foco** (conteúdo, nome ou descrição
  acessível). Navegação nunca usa região viva: o anúncio é o novo documento.
  **Escrever essa regra não é aplicá-la** — violei-a em 3 dos 13 estados do documento que a
  definia, porque ela estava na tabela de riscos e não na seção estrutural (`L-022`).
- **Regra de entrada numérica bilíngue (fixada no `TCK-0013`):** cada idioma tem um separador
  decimal **e** um de milhar (`i18n.md`); a regra tem de responder o que acontece com **os
  dois**, em cada idioma. Aceitar só o decimal do idioma ativo e recusar qualquer outro
  separador é simétrico, inspecionável na string e imune a falso positivo. Ler o separador de
  milhar como decimal (`3.000` → 3,0 em pt-BR) marca **certa uma resposta errada** — o pior modo
  de falha possível aqui, pior que recusar formato válido. Recusa de formato nunca conta como
  resposta incorreta.
- **Par simétrico (idioma, sentido, extremo) precisa de tabela com uma coluna por lado.** Regra
  escrita para um lado deixa o outro **permitido** (`L-021`); e a varredura de correção alcança
  **diagrama e rótulo**, não só prosa (`L-013`, adendo de `L-022`).
- **Região viva envolve texto de estado, nunca conteúdo.** Marcar uma seção inteira como viva
  faz o leitor de tela despejar enunciados e opções quando o conteúdo chega. Linha de estado
  curta, fora do lugar onde o conteúdo entra, esvaziada ao concluir.
- **"Desabilitado" acessível:** controle que ainda não pode agir fica marcado como
  indisponível mas **focável**, e ao ser acionado diz o motivo. Tirar da ordem de foco esconde
  a explicação de quem usa teclado.
- **Inserção de conteúdo vai abaixo do grupo de ações** (dica, resultado, solução): nada que já
  foi tabulado se desloca e não há salto de layout.
- **Texto de interface é sempre proposta** quando a spec não traz redação: marcar a origem
  (requisito que obriga a existência) e separar o que não tem requisito nenhum, para o
  `tech-lead` poder cortar sem quebrar critério de aceite.
- **`tags[]` e `skills[]` do acervo são slugs en-US sem tradução** — a interface precisa de um
  catálogo de rótulos bilíngues, ou RF-4 quebra em pt-BR. É dívida declarada; o lugar natural
  desses rótulos é `content/` (ticket de conteúdo/schema).
- **Rótulo bilíngue "visível nos dois idiomas"** (CA-16) significa existir nos dois e ser
  exibido no idioma ativo — nunca os dois textos juntos, que violaria RF-7.
- **Este agente não tem shell garantido:** ao encerrar ticket, pode não conseguir rodar as
  auditorias; declarar isso no log com o escopo do diff e passar a execução ao revisor.

## Últimas execuções

| Data | Ticket/Tarefa | Resultado | Lição relacionada |
|---|---|---|---|
| 2026-08-01 | TCK-0013 — 13 estados de tela e fluxo da fatia mínima | `in_review` — `docs/design/minimum-learning-slice/`; três decisões humanas (nó `draft`, URL bilíngue, rótulo no índice) desenhadas como alternativas e subidas ao `tech-lead` | — |
| 2026-08-01 | TCK-0013 — correção do REJECT do QA (loop 2/3) | `in_validation` — §9 reescrita simétrica (falso positivo `3.000`/`3.500` em pt-BR eliminado), rótulo `I3` do Mermaid remetendo à decisão (c), dívidas D-1/D-2/D-4 fechadas | L-022 (adendo) |
| 2026-08-01 | TCK-0013 — correção do REJECT (loop 1/3) | `in_review` — 5 bloqueantes resolvidos (regra de foco/anúncio virou norma em §3; região viva restrita a linha de estado; princípio 5 vs CA-3; decisão (c) reaberta em §5; `docs/README.md`), 6 sugestões aplicadas, decisão (b) do usuário (`/pt-br/` no caminho) incorporada | L-022 |
