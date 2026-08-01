# Contexto operacional — devops

> Documento **vivo**: pegadinhas do ambiente, estado atual e decisões operacionais em vigor
> na área. Lido por todo agente antes de trabalhar; atualizado (com data) ao final de
> qualquer ticket que mude esse conhecimento. Conhecimento generalizável sobre **erros** vai
> para `memory/lessons/`, não para cá.

**Última atualização:** 2026-08-01 (TCK-0012)

## Estado atual

- CI: um único workflow, `.github/workflows/ai-surface-audit.yml` (PR, push em `main`,
  semanal). Roda `audit-ai-surface.sh`, `sync-ai-adapters.py --check`, `audit-content.sh` e,
  desde TCK-0012, `tools/context-watch-test.sh`. Sem deploy configurado ainda; a stack
  segue indefinida (ADR-0003 `proposed`).
- Observabilidade de sessão (TCK-0012): `tools/context-watch.py` mede o consumo de contexto
  do Claude Code; hooks `PostToolBatch` e `PreCompact` em `.claude/settings.json`;
  `tools/agent-handoff.sh snapshot` grava o estado real antes da compactação.

## Pegadinhas conhecidas

*(verificadas em 2026-08-01, Claude Code 2.1.220)*

- **Recarga de hooks:** o watcher de settings só observa diretórios que já tinham arquivo de
  settings **quando a sessão começou**. Editar `.claude/settings.json` no meio da sessão não
  garante hook ativo: é preciso abrir `/hooks` (recarrega) ou reiniciar. Um agente não
  consegue provar a ativação sozinho pela UI — `/hooks` é do usuário. Não afirmar "está
  ativo" sem prova; dizer o que foi provado (pipe-test + `jq -e`).
  **Adendo (QA de TCK-0012, 2026-08-01): dá para provar por efeito colateral.** Se o hook
  escreve arquivo (aqui, o estado de zona em
  `${XDG_STATE_HOME:-~/.local/state}/mathematics-studies/context-zone-<session>.json`), basta
  observar o `updated_at`/mtime avançar **em lockstep com os lotes de ferramenta, sem
  invocação manual do script** — foi assim que o `PostToolBatch` ficou provado ativo nesta
  sessão (1785610758 → 1785610768 → 1785610776). Vale só para hooks com efeito colateral
  observável: o `PreCompact` continua não provável sem provocar uma compactação real.
- **Arquivo de configuração gitignored falsifica validação e revisão.**
  `.claude/settings.local.json` é lido **primeiro** por `resolve_window` e não aparece em
  `git status` nem em diff nenhum. Quem for medir/validar comportamento default tem de
  movê-lo para fora e restaurá-lo depois (conferindo por `diff` contra a cópia). Regra geral:
  antes de validar ferramenta que lê configuração, listar os arquivos ignorados que ela
  consulta.
- **`settings.json` malformado desativa o arquivo inteiro em silêncio** — inclusive
  `permissions`. Sempre validar com `jq -e` depois de editar, e conferir que o `git diff`
  não removeu blocos existentes.
- **Exit code de hook tem semântica:** `2` bloqueia a ação. Watcher/observador deve sair `0`
  em todos os caminhos, inclusive em erro. Saída visível ao usuário: uma linha JSON com
  `systemMessage` no stdout.
- **Python sai 120 quando falha o flush do stdout no shutdown** (`| head`, `| true`,
  `> /dev/full`) — acontece *depois* do seu `try/except`, então não adianta proteger só o
  `main()`. Receita: escrever **e** dar `flush()` dentro do `try`, redirecionar o fd para
  `os.devnull` com `dup2` quando quebrar, e dar um último `flush` protegido antes do
  `sys.exit`. Sem isso, "o hook sai 0 sempre" é falso e ninguém percebe.
- **Com o fd fechado pelo shell (`>&-`), `sys.stdout` é `None`** — não um arquivo quebrado:
  a exceção é `AttributeError`, que não está em `(BrokenPipeError, OSError, ValueError)`, e
  a limpeza pós-`except` volta a derrubar o processo. Matriz mínima de E/S para qualquer
  ferramenta de hook: `| head`, `| true`, `> /dev/full`, `>&-`, `2>&-`, stdin fechado,
  stdin lixo, stdin binário. Baseline honesto: `python3 -c 'print("x")' >&-` sai `0`.
- **Suíte de teste precisa isolar `HOME`**, não só o diretório de dados: qualquer código que
  leia `~/.claude/settings.json` (ou `~/.config/…`) faz o teste passar/falhar conforme a
  máquina. O CI fica verde por acidente (runner sem `~/.claude`) e quebra para quem seguiu a
  documentação do próprio projeto.
- **Transcript da sessão** (`~/.claude/projects/<cwd-com-barras-viradas-em-hífen>/<session>.jsonl`):
  - `message.model` vem como `claude-opus-5` **mesmo em sessão de 1M** — a variante `[1m]`
    não está lá (aparece só, por acidente, em `toolUseResult.resolvedModel`). Logo, deduzir
    a janela pelo modelo é chute; declare a janela da máquina em
    `.claude/settings.local.json` (`{"autoCompactWindow": <tokens>}`) — é o único lugar que
    alcança terminal, hook e `snapshot` ao mesmo tempo. **`CONTEXT_WINDOW` exportado no shell
    não chega ao hook**, que é lançado pelo Claude Code: usar a variável só para teste
    pontual. Quando o chute é inevitável, ele é **conservador** (200k), é abandonado assim
    que a medida o refuta (`usado > janela` → sobe um degrau, origem `refutado:…`) e é
    declarado no canal automático — L-015, L-017.
  - Pode haver **vários** `.jsonl` no mesmo diretório de projeto (uma sessão cada). O
    caminho confiável é o `transcript_path` que o hook entrega no stdin; `mtime` é fallback.
  - Mensagens de subagente têm `isSidechain: true` e não contam para o contexto da thread
    principal — que é o que a compactação atinge.
  - O arquivo contém a **conversa inteira**: qualquer ferramenta que o leia trata isso como
    requisito de segurança (só contagens e metadados na saída).
- **`~/.claude/settings.json` é do usuário**, não do repositório: já tem um hook
  `PreToolUse` em `Bash` (`rtk hook claude`). Não editar a partir de tarefas do projeto.

## Decisões operacionais em vigor

- Custo zero: nenhuma telemetria sai da máquina; nenhum serviço externo. As ferramentas de
  observação usam só bash + Python 3 da stdlib.
- Testes de ferramentas internas: script bash com fixtures em `mktemp -d`, executável no CI
  sem instalar nada (`tools/context-watch-test.sh` é o modelo).
- Estado efêmero de ferramenta (última zona de contexto etc.) vive em
  `${XDG_STATE_HOME:-~/.local/state}/mathematics-studies/` — nunca no working tree.
- Artefatos de handoff (`.agent-handoff.md`, `.agent-handoff.prev.md`) são gitignored.
- **`permissions` em `.claude/settings.json` não se amplia por conta própria** (L-016):
  entrada nova em `allow` é pedido ao usuário, não efeito colateral de entrega de tooling.
  Prova de preservação:
  `diff <(git show HEAD:.claude/settings.json | jq -S .permissions) <(jq -S .permissions .claude/settings.json)`.
- **Monitor que adivinha limiar adivinha pessimista** (L-015) e declara a dúvida no canal
  automático, com no máximo um aviso por sessão.
