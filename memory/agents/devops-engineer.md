# Memória do agente `devops-engineer`

> Memória persistente deste agente, mantida por ele próprio ao final de tarefas
> significativas. Índice geral: `memory/MEMORY.md` · lições: `memory/LESSONS.md` ·
> contexto da área: `memory/context/`.

## Papel

Cuida de CI/CD, build, deploy na Vercel, previews, variáveis de ambiente, monitoramento e performance de entrega. Usar para tickets de infraestrutura, pipeline e publicação.

## Notas persistentes

- **Hooks do Claude Code (a partir de TCK-0012):** o repositório registra dois em
  `.claude/settings.json` — `PostToolBatch` → `python3 tools/context-watch.py --hook`
  (avisa só quando a zona de contexto sobe) e `PreCompact` matcher `auto` →
  `bash tools/precompact-snapshot.sh` (escreve o handoff antes da compactação lossy).
  Ao mexer nesse arquivo: **nunca** reescrever sem preservar `permissions`; validar com
  `jq -e` (settings malformado desativa o arquivo inteiro em silêncio) e conferir que o
  `git diff` tem só inserções.
- **Hook não pode bloquear:** todo comando de hook deste repo sai `0` sempre; exit code de
  hook tem semântica de bloqueio no Claude Code. Isso inclui o caminho em que a **escrita**
  falha (`| head`, `> /dev/full`): sem `flush()` dentro do `try` + `dup2` para `os.devnull`,
  o Python sai `120` no shutdown e a invariante vira mentira documentada.
- **Medição incerta avisa cedo, nunca calada** (L-015): janela presumida usa o valor
  conservador e o hook declara a presunção uma vez por sessão. **Presunção refutada pela
  medida é abandonada** (L-017), e o estado do antirruído zera quando a régua muda — senão o
  alarme satura no topo e o mecanismo morre calado.
- **Verificar o desfecho, não a linha citada no `REJECT`** (L-018): encenar a promessa
  inteira (estado zerado, medidas crescentes, mais de um disparo) antes de dizer "resolvido".
- **`permissions` só se amplia a pedido do usuário** (L-016); provar preservação com
  `diff` de `jq -S` contra o `HEAD`, não com "o diff só tem inserções".
- **Hook ruidoso morre:** aviso repetido a cada chamada de ferramenta faz o usuário
  desligar o mecanismo. O estado da última zona vive em
  `${XDG_STATE_HOME:-~/.local/state}/mathematics-studies/`, fora do repositório.
- **Testes sem framework:** o padrão do repo é script bash + Python 3 da stdlib montando
  fixtures em `mktemp -d` (`tools/context-watch-test.sh`, 41 asserções), plugado no
  workflow `ai-surface-audit.yml`. Nada de `pip install`.
- **Medida de contexto:** `python3 tools/context-watch.py` (exit `0/10/20/30/40`). Sem
  telemetria, sai `40` — nunca inventar estimativa para Codex/Copilot/Gemini.

## Últimas execuções

| Data | Ticket/Tarefa | Resultado | Lição relacionada |
|---|---|---|---|
| 2026-08-01 | TCK-0012 — detectar esgotamento de contexto e disparar handoff | `context-watch.py` + hooks + `agent-handoff.sh snapshot` + suíte de 41 casos no CI; handoff ao `code-reviewer` | hooks só recarregam via `/hooks`/reinício — critério 9 |
| 2026-08-01 | TCK-0012 — `REJECT` 1/3 do `code-reviewer` (B1–B4) | janela presumida virou conservadora + aviso no hook; `--hook` sai 0 mesmo com stdout quebrado; suíte isolada do `HOME` (41 → 65 asserções); duas entradas de `permissions.allow` revertidas | L-015, L-016 |
| 2026-08-01 | TCK-0012 — `REJECT` 2/3 (B5 alarme saturado, B6 fd fechado) | presunção refutada pela medida passa a ser abandonada (escalona um degrau e anuncia); estado rearma ao trocar a régua; `>&-` tratado; janela declarada em `.claude/settings.local.json` (65 → 93 asserções) | L-017, L-018 |
