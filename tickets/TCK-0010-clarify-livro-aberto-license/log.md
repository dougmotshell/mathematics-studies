# Log — TCK-0010

> Append-only. Formatos em `docs/ai/ticket-protocol.md`.

## [001] ACTION — 2026-08-01 15:55 — tech-lead
- Ação: criação do ticket a partir da pendência 2 do `docs-writer#2` (`TCK-0004/log.md`
  `[009]`, também em `[006]`) e da divergência confirmada de forma independente por
  `researcher` e `qa-validator` no TCK-0001 (`[004]`, `[007]`). Trechos verbatim no ticket.
- Motivo: a divergência é real e verificada duas vezes (página do projeto: BY-NC-SA; selo do
  colofão do PDF: BY-SA, sem NC e sem versão). Enquanto ela existir, vale a leitura mais
  restritiva e o projeto segue **sem nenhuma** fonte pt-BR adaptável.
- Resultado: ok — `tickets/TCK-0010-clarify-livro-aberto-license/` criado.
- Lição: n/a — não resolve `REJECT`.

## [002] ACTION — 2026-08-01 15:57 — tech-lead
- Ação: triagem. Status `new` → `triaged`. **Sem `HANDOFF`** (L-005).
- **Agrupamento (justificativa em uma linha):** fica **separado** do TCK-0009 (schema)
  porque tem outro dono, outro tipo e outro modo de falhar — pode terminar em
  `blocked: human-input` esperando resposta de terceiro, e arrastar o contrato de dados para
  essa espera seria bloquear trabalho pronto por causa de um e-mail.
- **Tipo:** `research`. Cadeia curta do protocolo: `tech-lead` → `researcher` → `tech-lead`.
  **Extensão declarada:** se a conclusão alterar arquivos (critérios 4 e 5), segue
  `code-reviewer` → `qa-validator` antes do `done`; se terminar em relatório + pergunta ao
  usuário, volta a mim e vira `blocked: human-input`. Registro a bifurcação agora para o
  executor não improvisar cadeia.
- **Prioridade P2 · tamanho P.** Não bloqueia nada em curso: a leitura restritiva já está
  registrada e é segura. Está acima de P3 pelo retorno assimétrico — se a resposta for BY-SA,
  o projeto ganha um livro didático completo de ensino médio em pt-BR como matéria-prima
  legítima, e o custo de produção autoral da Fase 1 muda de patamar. Aposta barata, prêmio
  alto.
- **Owner: `researcher`** — fontes gratuitas, licenças e literatura didática são sua área
  exclusiva; foi quem levantou as três referências do nó piloto no TCK-0001.
- **Restrições passadas ao executor:**
  1. **Nada de adaptar antes da conclusão.** Enquanto o resultado não for (a), a obra é
     `citable-only` (`AGENTS.md` §9.7, L-009). Critério 6 é bloqueante.
  2. **Verificar por obra, não por projeto** (L-006): licença de coleção pode variar entre
     volumes; concluir a partir de um único PDF é o erro já registrado.
  3. Toda declaração vale por **citação literal + URL + HTTP code + data** — selo gráfico
     conta como evidência, mas registrar como foi lido (no TCK-0001 foi `pdftoppm` sobre o
     colofão, porque o selo é imagem; L-007).
  4. Se as fontes públicas não fecharem a questão, **não inventar contato nem enviar nada**:
     entregar a pergunta objetiva e o canal verificado, e parar em `blocked: human-input`.
  5. Nenhuma edição em `theory.*.md` ou `exercises.json`, qualquer que seja a conclusão.
- **Aderência ao plano:** Fase 1 do roadmap depende de fontes gratuitas com licença
  registrada; `ADR-0005` já fixou a regra de compatibilidade. Este ticket não altera decisão,
  apura fato. Dentro do plano.
- **Requisitos inegociáveis conferidos:** gratuidade (critério 7 exige acesso público
  anônimo), bilinguismo (o objetivo é justamente destravar fonte em pt-BR); a11y, offline e
  privacidade não aplicáveis, com o porquê no ticket.
- **Dependências:** nenhuma. Interage com o `TCK-0009` apenas no formato do registro — se o
  schema já estiver entregue, a conclusão vira valor de `usage`; se não, vira nota no campo
  `license`/`licenseNotes` no formato vigente. O executor usa o formato do dia, sem esperar.
- Resultado: ok — `status: triaged`, `owner: researcher`. Aguardando ordem de execução.
- Lição: n/a — não resolve `REJECT`.
