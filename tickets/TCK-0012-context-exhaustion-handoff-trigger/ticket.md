---
id: TCK-0012
title: Detectar esgotamento de contexto e disparar handoff entre CLIs
type: infra
status: done
owner: qa-validator
priority: P2
size: M
created: 2026-08-01
updated: 2026-08-01
related: []
---

# TCK-0012 — Detectar esgotamento de contexto e disparar handoff entre CLIs

## Pedido original (verbatim)

> elabore uma forma de identificar quando os tokens estão prestes a acabar para conseguir
> fazer handoff para outra ferramenta como o codex ou copilot, etc...

## Requisito refinado

O repositório já tem o mecanismo de troca de ferramenta (`/agent-handoff`,
`tools/agent-handoff.sh`, `docs/ai/cross-agent-handoff.md`), mas ele depende de **alguém
perceber a hora certa**. Na prática o handoff só é lembrado quando o contexto já está
comprometido — e a compactação automática do Claude Code é *lossy*: quando ela dispara, o
detalhe já se perdeu.

Falta a camada de **observação e gatilho**: medir o consumo real de contexto, avisar em
faixas antes do limite, e garantir que o `.agent-handoff.md` seja escrito **antes** da
compactação, não depois.

O que torna isso viável (verificado em 2026-08-01, nesta sessão): o Claude Code grava o
transcript em `~/.claude/projects/<slug>/<session>.jsonl`, e cada mensagem `assistant`
carrega `usage` com `input_tokens`, `cache_creation_input_tokens` e
`cache_read_input_tokens` — a soma é o contexto vivo. Protótipo mediu 325.000 / 1.000.000
tokens corretamente e foi exercitado nas cinco faixas.

## Critérios de aceite

- [x] 1. `tools/context-watch.py` existe e, rodado na raiz do repositório dentro de uma
      sessão do Claude Code, imprime a zona e o percentual de uso do contexto, calculados
      como `input_tokens + cache_creation_input_tokens + cache_read_input_tokens` da última
      mensagem `assistant` **não-sidechain** do transcript da sessão.
- [x] 2. Os exit codes são estáveis e documentados: `0` verde (<60%), `10` atenção (<75%),
      `20` preparar handoff (<85%), `30` crítico (≥85%), `40` sem telemetria. Um `if` de
      shell consegue ramificar sobre eles.
- [x] 3. A janela de contexto é resolvida nesta ordem: variável `CONTEXT_WINDOW` →
      `autoCompactWindow` de `.claude/settings.json` ou `~/.claude/settings.json` → padrão
      por modelo. A origem usada aparece na saída `--json`.
- [x] 4. `--json` emite objeto de uma linha com zona, usado, janela, percentual, modelo e
      instante da medição. **Nenhum conteúdo da conversa é impresso** — só números e
      metadados (o transcript contém a conversa inteira; vazá-la seria defeito de
      privacidade).
- [x] 5. Casos hostis tratados sem stack trace, cada um com teste: transcript ausente;
      transcript vazio; linha JSON malformada no meio do arquivo; uso acima de 100% da
      janela; nenhuma mensagem com `usage`; diretório de projeto inexistente.
- [x] 6. `tools/agent-handoff.sh snapshot` preenche o handoff com estado real, sem
      digitação: branch, HEAD, `git status --short`, `git diff --stat`, tickets com status
      diferente de `done` (id, título, status, owner) com a **última entrada** do `log.md`
      de cada um, estado de `.dev-loop/*/loop.md`, e os comandos de verificação do projeto.
- [x] 7. `snapshot` não sobrescreve um handoff existente sem `--force`, e o resultado passa
      em `tools/agent-handoff.sh validate`.
- [x] 8. Hooks registrados em `.claude/settings.json`, **preservando** os blocos já
      existentes: `PostToolBatch` avisa quando a zona **sobe** (nunca a cada chamada de
      ferramenta) e `PreCompact` com matcher `auto` gera o snapshot antes da compactação.
- [x] 9. Está documentado — e verificado — se os hooks passam a valer na sessão corrente ou
      exigem `/hooks`/reinício; se exigirem, o ticket diz isso explicitamente em vez de
      afirmar que "está ativo".
- [x] 10. Degradação honesta fora do Claude Code: sem transcript, o script sai com `40` e
      mensagem explícita de que a ferramenta não expõe telemetria — **não** inventa
      estimativa.
- [x] 11. `.claude/skills/agent-handoff/SKILL.md` e `docs/ai/cross-agent-handoff.md`
      descrevem quando checar, o que cada zona exige e o procedimento nas ferramentas sem
      telemetria. `python3 scripts/sync-ai-adapters.py` rodado.
- [x] 12. Zero dependência nova: apenas Python 3 da stdlib e bash. `bash
      scripts/audit-ai-surface.sh` e `bash scripts/audit-content.sh` sem erros.

### Requisitos transversais (marcar todos)

- [x] Bilinguismo pt-BR + en-US · [x] não aplicável (ferramenta interna, seção 2a)
- [x] Acessibilidade WCAG 2.2 AA · [x] não aplicável
- [x] Funciona offline / PWA · [x] não aplicável
- [x] Custo zero mantido — sem serviço externo, sem telemetria enviada para fora
- [x] Privacidade — o transcript contém a conversa; o script lê contagens e nunca imprime
      conteúdo (critério 4)
- [x] URLs de `content/` preservadas · [x] não aplicável
- [x] Correção matemática verificada · [x] não aplicável

## Fora de escopo

- Implementar detecção de contexto para Codex, Copilot ou Gemini — nenhum expõe a
  telemetria; tentar estimar produziria número falso.
- Enviar qualquer métrica para fora da máquina.
- Adotar `totalTokensReminder` como base do mecanismo: o schema o marca `@internal` e ele
  pode mudar sem aviso. Pode ser **documentado** como reforço opcional, nunca como
  fundamento.
- Compactação automática, resumo de sessão ou qualquer alteração no comportamento do
  Claude Code além dos hooks.
- Handoff automático **executado** sem pedido — o gatilho escreve o arquivo e avisa; trocar
  de ferramenta continua sendo decisão do usuário.

## Contexto e referências

- Protótipo validado nas cinco faixas (medição, `--json`, e o bug de `frac ≥ 101%` já
  corrigido nele): `/tmp/claude-1000/-home-douglas-silva-www-mathematics-studies/e98cd8af-8218-4a45-aa57-a2b62c2126cd/scratchpad/context-watch.py`
- Handoff atual: `tools/agent-handoff.sh`, `tools/agent-handoff-template.md`,
  `docs/ai/cross-agent-handoff.md`, `.claude/skills/agent-handoff/SKILL.md`
- Transcript: `~/.claude/projects/-home-douglas-silva-www-mathematics-studies/*.jsonl`
- Eventos de hook válidos e formato: schema de `settings.json` (inclui `PostToolBatch`,
  `PreCompact`, `PostCompact`, `SessionEnd`, `Stop`)
- Settings atuais a preservar: `.claude/settings.json` (permissions) e
  `~/.claude/settings.json` (já tem um hook `PreToolUse` em `Bash` — **não remover**)
- Contexto da área: `memory/context/devops.md`, `memory/context/process.md`

## Perguntas em aberto

- Nenhuma. Os limiares (60/75/85%) são ponto de partida justificado — escrever um handoff
  bom custa 5–10k tokens, e o corte em 85% preserva folga para escrevê-lo. Ajustáveis por
  variável de ambiente.

## Resultado final

**Validado por `qa-validator#6` em 2026-08-01 (commit `08fe2e9`), 12/12 critérios com
evidência de execução própria, 0 defeitos.** Detalhamento comando a comando em
`log.md` `[014]`.

### O que foi entregue

| Artefato | Papel |
|---|---|
| `tools/context-watch.py` | Mede o contexto vivo da sessão (soma `input_tokens + cache_creation_input_tokens + cache_read_input_tokens` da última mensagem `assistant` não-sidechain do transcript). Zonas, exit codes `0/10/20/30/40`, `--json`, `--quiet`, `--hook`, `--session`, `--cwd`. Só stdlib. |
| `tools/context-watch-test.sh` | Suíte de 93 asserções (6 casos hostis, privacidade, refutação, matriz de E/S). Roda em bash + Python 3, sem runner. |
| `tools/precompact-snapshot.sh` | Wrapper do hook `PreCompact`: grava o handoff **antes** da compactação automática. Sai `0` sempre. |
| `tools/agent-handoff.sh snapshot` | Preenche o `.agent-handoff.md` com estado real (branch, HEAD, `git status`, `git diff --stat`, tickets fora de `done` com a última entrada do log, dev-loops, comandos de verificação, medição). Não inventa intenção: os `<preencher>` ficam. |
| `.claude/settings.json` | Hooks `PostToolBatch` (aviso quando a zona **sobe**) e `PreCompact` (matcher `auto`). Bloco `permissions` **idêntico ao `HEAD`**. |
| `.github/workflows/ai-surface-audit.yml` | A suíte de casos hostis entrou no CI. |
| `.claude/skills/agent-handoff/SKILL.md` · `docs/ai/cross-agent-handoff.md` | Quando checar, o que cada zona exige, como declarar a janela e o procedimento honesto nas ferramentas sem telemetria. |

### Como usar

```bash
python3 tools/context-watch.py            # zona + percentual + ação recomendada
python3 tools/context-watch.py --json     # objeto de uma linha (só números e metadados)
python3 tools/context-watch.py --quiet    # só exit code, para ramificar em shell
bash tools/agent-handoff.sh snapshot      # escreve o handoff com o estado real
bash tools/agent-handoff.sh validate      # confere as seções obrigatórias
bash tools/context-watch-test.sh          # 93 asserções
```

| Zona | Uso | Exit code | O que fazer |
|---|---|---|---|
| verde | < 60% | `0` | seguir normalmente |
| atenção | < 75% | `10` | evitar releitura de arquivos grandes |
| preparar | < 85% | `20` | `bash tools/agent-handoff.sh snapshot --force` |
| crítico | ≥ 85% | `30` | handoff agora — a compactação é lossy |
| sem telemetria | — | `40` | a ferramenta não expõe uso de contexto; **não** estimar |

**Primeiro passo recomendado em cada máquina** — acaba com o palpite e vale para os três
canais (terminal, hook e `snapshot`): criar `.claude/settings.local.json` (gitignored) com

```json
{ "autoCompactWindow": 1000000 }
```

`export CONTEXT_WINDOW=…` **não** serve como configuração permanente: o hook é lançado pelo
Claude Code, não pelo shell interativo, e a mesma sessão passaria a reportar números
diferentes em canais diferentes. A ferramenta **não depende** desse arquivo — a validação
dos critérios 1, 2, 3, 5 e 10 foi feita com ele movido para fora do repositório.

### Hooks: `/hooks` ou reinício

Editar `.claude/settings.json` **não** recarrega os hooks de forma garantida na sessão em
curso — o watcher só observa diretórios que já tinham arquivo de settings quando a sessão
começou. **Para ter certeza, abra `/hooks` uma vez (recarrega a configuração) ou reinicie a
sessão.** Na validação de 2026-08-01 o `PostToolBatch` foi observado **ativo** nesta sessão
(o arquivo de estado em `~/.local/state/mathematics-studies/` avançou a cada lote de
ferramenta, sem invocação manual), o que é consistente com a condição acima — o
`.claude/settings.json` já existia no início da sessão. O `PreCompact` não é observável sem
provocar uma compactação real e continua declarado como não provado ativo.

### Dívidas aceitas

1. **D-1 — `WINDOW_TIERS = (200_000, 1_000_000)`.** Um modelo com janela intermediária
   (ex.: 400k) seria superestimado para 1M: medido na validação, o efeito é **um** aviso de
   refutação e depois silêncio ao longo de toda a faixa de perigo. Aceito porque hoje não
   existe modelo Claude com janela entre os dois degraus, a incerteza é declarada
   (`janela_confiavel: false`, origem `refutado:`, `systemMessage` no hook) e a correção é um
   item na tupla. **Gatilho:** no dia em que existir esse modelo, isto vira defeito — abrir
   ticket antes de medi-lo.
2. **D-2 — `janela_origem` não distingue `settings.local.json` de `settings.json`** (ambos
   saem como `settings:projeto:autoCompactWindow`).
3. **D-3 — até 3 alarmes falsos por ciclo** na faixa 120k–200k de uma sessão de 1M **não
   configurada**, antes da refutação; todos acompanhados da ressalva de janela presumida. É o
   preço aceito da presunção conservadora (errar avisando cedo, nunca calando). Vale uma
   linha na documentação avisando o usuário.
4. **D-4 — `.dev-loop/analyze-open-tickets/`** está `Status: done` no disco e aparece no
   snapshot como loop ativo. Fora de escopo — candidato a ticket de limpeza.
5. **D-5 — decisão do usuário, não aplicada:** acrescentar
   `Bash(python3 tools/context-watch.py:*)` e `Bash(bash tools/context-watch-test.sh:*)` a
   `permissions.allow` evitaria o prompt ao rodar a ferramenta. É decisão de quem opera a
   máquina; o ticket não pediu e não aplicou.
