# TASKS — Fatia mínima de aprendizagem

- **Spec:** [`spec.md`](spec.md) · **Plan:** [`plan.md`](plan.md)
- **Data:** 2026-08-01

Cada task vira (ou entra em) um ticket `TCK-NNNN`. Tasks pequenas, ordenadas, com critério de
pronto verificável e agente sugerido. **Nenhuma task de implementação começa antes da task 1 e
da spec `approved`.**

| # | Task | Agente sugerido | Depende de | Critério de pronto | Ticket |
|---|---|---|---|---|---|
| 1 | Registrar o aceite do `ADR-0003` (site estático + ilhas, local-first sem conta) e as consequências para esta spec | `platform-architect` + decisão humana | — | `docs/adr/ADR-0003-platform-stack.md` com `Status: accepted`, data e consequências; `docs/adr/README.md` atualizado; nenhuma decisão de biblioteca embutida no ADR | TCK-0003 |
| 2 | Aprovar a spec (`/spec-review`) com evidência de que não trava a stack nem introduz coleta de dados | `code-reviewer` / revisor independente | 1 | Spec em `approved` no front matter e em `docs/specs/README.md`; perguntas em aberto resolvidas ou explicitamente adiadas com dono | — |
| 3 | Desenhar os 13 estados de tela e o fluxo `índice → nó → exercício`, incluindo rótulo de rascunho, alternador de idioma e estados de rede | `ui-ux-designer` | 2 | Um artefato por estado da tabela da spec, com texto de interface nos dois idiomas, ordem de foco por teclado e anúncio do resultado por região viva | — |
| 4 | Implementar o validador do contrato de conteúdo (RF-18) com fixtures válidas e inválidas | `backend-developer` | 2 | CA-13 e CA-14 passam; fixture com `multiple-choice` sem `correct: true`, `numeric` com `tolerance` negativa, chave de idioma faltando e `nodeId` divergente falham de forma visível e registrada | — |
| 5 | Implementar o índice de navegação `estágio → área → tópico` até o nó piloto | `frontend-developer` | 3, 4 | CA-1 passa; a URL contém `high-school/algebra/quadratic-equations` sem tradução ou normalização (RNF-5) | — |
| 6 | Implementar o leitor de nó: metadados, rótulo `draft`, pré-requisitos e teoria com KaTeX acessível | `frontend-developer` | 3, 4 | CA-2 e CA-16 passam; nenhum LaTeX cru na tela; parágrafos de leitura presentes no DOM acessível; `prerequisites[]` vazio não gera seção (RF-6) | — |
| 7 | Implementar o player de exercícios: `multiple-choice`, `numeric` com tolerância, feedback da opção escolhida e nova tentativa | `frontend-developer` | 6 | CA-4, CA-5, CA-6 e CA-15 (parte do exercício) passam; `qe-003` com `tolerance: 0` só aceita o valor exato; nova tentativa preserva dicas reveladas | — |
| 8 | Implementar dicas progressivas e solução sob demanda | `frontend-developer` | 7 | CA-8 e CA-9 passam; `solution` ausente do DOM enquanto o item não é respondido; controle de dica indisponível e anunciado após a última | — |
| 9 | Implementar a alternância de idioma e provar a paridade sem fallback | `i18n-steward` + `frontend-developer` | 6, 7 | CA-3, CA-7 e CA-14 passam; `/i18n-parity` sem pendências; separador decimal por idioma conforme `docs/content/i18n.md`; `lang` do documento correto em cada idioma | — |
| 10 | Implementar a camada offline do conteúdo visitado e os dois estados de rede | `frontend-developer` + `devops-engineer` | 6, 7 | CA-10 e CA-11 passam; nó visitado reabre sem rede com indicador de modo offline; idioma nunca visitado offline mostra indisponibilidade, nunca o outro idioma | — |
| 11 | Configurar build e publicação estática com a validação do RF-18 no pipeline | `devops-engineer` | 4, 5 | Build falha quando uma fixture inválida entra no acervo; publicação em hospedagem estática sem serviço pago (RNF-4); orçamento de performance (RNF-8) registrado como critério de `/pwa-audit` | — |
| 12 | Auditar acessibilidade (WCAG 2.2 AA) da fatia completa, incluindo a matemática | `a11y-ux-reviewer` | 8, 9, 10 | CA-15 passa; `/a11y-audit` sem violação AA; navegação completa por teclado com foco visível; resultado anunciado por região viva, não só por cor | — |
| 13 | Auditar privacidade e dependências (zero coleta, zero terceiro rastreador) | `security-auditor` | 10, 11 | CA-12 passa; inspeção de tráfego sem resposta do aluno, identificador ou domínio de analytics; nenhuma dependência de terceiro que registre o visitante (RNF-7) | — |
| 14 | Validar a fatia contra CA-1…CA-16 e marcar `done` | `qa-validator` | 12, 13 | Evidência por critério no `log.md` do ticket; nenhum critério sem prova; escopo dentro dos limites da spec | — |
| 15 | Atualizar documentação e memória: C4 da aplicação, contexto por área, roadmap e status da spec | `docs-writer` | 14 | `docs/architecture/` com Container e Component da aplicação; `docs/specs/README.md` com a spec em `done`; `memory/context/` e `memory/lessons/` atualizados | — |

## Paralelizáveis

- Tasks **3 e 4** não dependem entre si (desenho de estados × validador do contrato) e podem
  correr em tickets separados logo após a aprovação da spec.
- Tasks **5 e 6** dependem das mesmas bases (3 e 4), mas não uma da outra.
- Tasks **9 e 10** partem de 6 e 7 e podem correr em paralelo — idioma e offline se cruzam
  apenas em CA-11, que deve ser validado por quem terminar por último.
- Tasks **12 e 13** (a11y e privacidade) são auditorias independentes entre si.
- **Não paralelizar** 7 e 8: a solução e as dicas dependem do ciclo de resposta já pronto.

## Validação final

O `qa-validator` só marca `done` com evidência por item:

1. **CA-1…CA-16** — cada critério exercitado e o resultado registrado no `log.md` do ticket
   correspondente, citando o critério pelo identificador. Critério sem evidência = não
   atendido.
2. **`bash scripts/audit-content.sh`** — sem erros; garante que a fatia não alterou o acervo
   nem quebrou a paridade bilíngue (RNF-9, RNF-1).
3. **`bash scripts/audit-ai-surface.sh`** — sem erros; garante que a superfície de IA seguiu
   íntegra durante a implementação.
4. **`/a11y-audit`** sem violação WCAG 2.2 AA e **`/pwa-audit`** dentro do orçamento de
   performance definido na task 11.
5. **`/i18n-parity`** sem pendências no nó piloto.
6. **Inspeção de tráfego** de uma sessão completa: nenhuma requisição com resposta do aluno,
   identificador ou domínio de analytics (CA-12).
7. **Conferência de escopo:** nada entregue além do que a spec autoriza — sem progresso
   persistente, sem trilhas, sem busca, sem `references.json`, sem alteração em `content/`.

Cada agente valida apenas o que não produziu (AGENTS.md §10, regra 4).
