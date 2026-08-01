#!/usr/bin/env bash
# context-watch-test.sh — suíte de casos hostis de tools/context-watch.py (TCK-0012, critério 5).
#
# Por que bash + stdlib e não um framework: o repositório não tem runner de testes
# instalado e o ticket proíbe dependência nova. Este script monta transcripts sintéticos
# em diretório temporário (nunca toca no working tree nem em ~/.claude) e verifica exit
# code e saída. Roda em qualquer máquina com bash e Python 3.
#
# Uso: bash tools/context-watch-test.sh [-v]

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WATCH="$SCRIPT_DIR/context-watch.py"
VERBOSE=0
[[ "${1:-}" == "-v" ]] && VERBOSE=1

TMP="$(mktemp -d "${TMPDIR:-/tmp}/context-watch-test.XXXXXX")"
trap 'rm -rf "$TMP"' EXIT

PROJECTS="$TMP/projects"
FAKE_CWD="/fake/repo"
SLUG="-fake-repo"
mkdir -p "$PROJECTS/$SLUG" "$TMP/home"
export CLAUDE_PROJECTS_DIR="$PROJECTS"
export XDG_STATE_HOME="$TMP/state"
# Hermetismo (B3): sem isolar o HOME, `resolve_window` lê o ~/.claude/settings.json da
# máquina e a suíte falha justamente para quem seguiu a documentação e definiu
# `autoCompactWindow`. Teste que depende da configuração local não protege ninguém.
export HOME="$TMP/home"
unset CONTEXT_WATCH_THRESHOLDS CLAUDE_SESSION_ID 2>/dev/null || true

pass=0; fail=0
out=""; code=0

# --- helpers ---------------------------------------------------------------------------

# make_transcript <arquivo> <especificação por linha>
# Cada argumento extra é: assistant:<input>:<create>:<read>[:sidechain] | garbage | other | usageless
make_transcript() {
  local file="$1"; shift
  : > "$file"
  local spec
  for spec in "$@"; do
    python3 - "$file" "$spec" <<'PY'
import json, sys
path, spec = sys.argv[1], sys.argv[2]
parts = spec.split(":")
kind = parts[0]
if kind == "garbage":
    line = '{"type": "assistant", "message": {"usage": {broken'
elif kind == "other":
    line = json.dumps({"type": "user", "message": {"role": "user",
                       "content": "SEGREDO-DO-USUARIO-NAO-VAZAR"}})
elif kind == "usageless":
    line = json.dumps({"type": "assistant", "isSidechain": False,
                       "message": {"model": "claude-opus-5",
                                   "content": "SEGREDO-DO-USUARIO-NAO-VAZAR"}})
else:
    line = json.dumps({
        "type": "assistant",
        "isSidechain": len(parts) > 4 and parts[4] == "sidechain",
        "timestamp": "2026-08-01T12:00:00.000Z",
        "message": {
            "model": "claude-opus-5",
            "content": [{"type": "text", "text": "SEGREDO-DO-USUARIO-NAO-VAZAR"}],
            "usage": {"input_tokens": int(parts[1]),
                      "cache_creation_input_tokens": int(parts[2]),
                      "cache_read_input_tokens": int(parts[3]),
                      "output_tokens": 10},
        },
    })
with open(path, "a", encoding="utf-8") as fh:
    fh.write(line + "\n")
PY
  done
}

run_watch() {
  out="$(python3 "$WATCH" --cwd "$FAKE_CWD" "$@" 2>&1)"
  code=$?
}

report() {
  local name="$1" ok="$2"
  if [[ "$ok" == "1" ]]; then
    pass=$((pass + 1)); printf 'ok   %s\n' "$name"
  else
    fail=$((fail + 1)); printf 'FAIL %s\n     exit=%s saída: %s\n' "$name" "$code" "$out"
  fi
  (( VERBOSE )) && printf '     exit=%s | %s\n' "$code" "${out//$'\n'/ | }"
  return 0
}

expect_code() { # nome esperado
  local name="$1" want="$2"
  [[ "$code" == "$want" ]] && report "$name (exit $want)" 1 || report "$name (esperado exit $want)" 0
}

expect_match() { # nome regex
  local name="$1" re="$2"
  grep -Eqi -- "$re" <<<"$out" && report "$name" 1 || report "$name (não casou: $re)" 0
}

expect_nomatch() {
  local name="$1" re="$2"
  grep -Eqi -- "$re" <<<"$out" && report "$name (casou indevidamente: $re)" 0 || report "$name" 1
}

no_stacktrace() {
  local name="$1"
  grep -q "Traceback" <<<"$out" && report "$name" 0 || report "$name" 1
}

# --- caso 1: transcript ausente --------------------------------------------------------

export CONTEXT_WINDOW=1000000
run_watch
expect_code "caso 1 · transcript ausente" 40
expect_match "caso 1 · mensagem explícita" "nenhum transcript"
no_stacktrace "caso 1 · sem stack trace"

# --- caso 2: transcript vazio ----------------------------------------------------------

: > "$PROJECTS/$SLUG/vazio.jsonl"
run_watch --session "$PROJECTS/$SLUG/vazio.jsonl"
expect_code "caso 2 · transcript vazio" 40
expect_match "caso 2 · mensagem explícita" "transcript vazio"
no_stacktrace "caso 2 · sem stack trace"

# --- caso 3: linha JSON malformada no meio ---------------------------------------------

make_transcript "$PROJECTS/$SLUG/misto.jsonl" \
  "assistant:10:0:100000" "garbage" "other" "assistant:5:1000:299000" "assistant:1:0:900000:sidechain"
run_watch --session "$PROJECTS/$SLUG/misto.jsonl" --json
expect_code "caso 3 · linha malformada ignorada" 0
expect_match "caso 3 · mede a última válida (300.005)" '"usado": 300005'
expect_match "caso 3 · conta a linha ilegível" '"linhas_ilegiveis": 1'
expect_nomatch "caso 3 · ignora sidechain" '"usado": 900001'
no_stacktrace "caso 3 · sem stack trace"

# --- caso 4: uso acima de 100% da janela -----------------------------------------------

make_transcript "$PROJECTS/$SLUG/estouro.jsonl" "assistant:0:0:324000"
CONTEXT_WINDOW=200000 run_watch --session "$PROJECTS/$SLUG/estouro.jsonl"
expect_code "caso 4 · uso 162% da janela" 30
expect_match "caso 4 · percentual acima de 100" "162\.0%"
no_stacktrace "caso 4 · sem StopIteration/stack trace"
bar_len="$(sed -n 's/.*\[\([#.]*\)\].*/\1/p' <<<"$out" | head -1 | tr -d '\n' | wc -c)"
[[ "$bar_len" == "30" ]] && report "caso 4 · barra não estoura (30 chars)" 1 \
  || { out="barra com $bar_len chars"; report "caso 4 · barra não estoura (30 chars)" 0; }

# --- caso 5: nenhuma mensagem com usage ------------------------------------------------

make_transcript "$PROJECTS/$SLUG/sem-usage.jsonl" "other" "usageless" "other"
run_watch --session "$PROJECTS/$SLUG/sem-usage.jsonl"
expect_code "caso 5 · nenhuma mensagem com usage" 40
expect_match "caso 5 · mensagem explícita" "nenhuma mensagem assistant com usage"
no_stacktrace "caso 5 · sem stack trace"

# --- caso 6: diretório de projeto inexistente ------------------------------------------

out="$(python3 "$WATCH" --cwd /diretorio/que/nao/existe 2>&1)"; code=$?
expect_code "caso 6 · diretório de projeto inexistente" 40
expect_match "caso 6 · mensagem explícita" "nenhum diretório de projeto"
no_stacktrace "caso 6 · sem stack trace"

# --- privacidade (critério 4): nada de conteúdo na saída -------------------------------

run_watch --session "$PROJECTS/$SLUG/misto.jsonl"
expect_nomatch "privacidade · texto não vaza conteúdo" "SEGREDO-DO-USUARIO"
run_watch --session "$PROJECTS/$SLUG/misto.jsonl" --json
expect_nomatch "privacidade · json não vaza conteúdo" "SEGREDO-DO-USUARIO"
run_watch --session "$PROJECTS/$SLUG/sem-usage.jsonl"
expect_nomatch "privacidade · erro não vaza conteúdo" "SEGREDO-DO-USUARIO"

# --- extras de robustez ----------------------------------------------------------------

run_watch --session "$PROJECTS/$SLUG/nao-existe.jsonl"
expect_code "extra · --session apontando para arquivo inexistente" 40

make_transcript "$PROJECTS/$SLUG/so-lixo.jsonl" "garbage" "garbage"
run_watch --session "$PROJECTS/$SLUG/so-lixo.jsonl"
expect_code "extra · transcript inteiramente ilegível" 40
no_stacktrace "extra · sem stack trace"

CONTEXT_WATCH_THRESHOLDS="lixo" run_watch --session "$PROJECTS/$SLUG/misto.jsonl" --json
expect_code "extra · CONTEXT_WATCH_THRESHOLDS inválido cai no padrão" 0

CONTEXT_WINDOW=0 run_watch --session "$PROJECTS/$SLUG/misto.jsonl" --json
expect_match "extra · CONTEXT_WINDOW inválido é ignorado, não zera a divisão" '"janela": (200000|1000000)'
expect_nomatch "extra · CONTEXT_WINDOW inválido não vira origem" '"janela_origem": "env'

CONTEXT_WINDOW=400000 run_watch --session "$PROJECTS/$SLUG/misto.jsonl" --json
expect_match "extra · origem da janela aparece no json (critério 3)" '"janela_origem": "env:CONTEXT_WINDOW"'

run_watch --session "$PROJECTS/$SLUG/misto.jsonl" --quiet
[[ -z "$out" ]] && report "extra · --quiet não imprime nada" 1 || report "extra · --quiet não imprime nada" 0

# --- B1: janela presumida é conservadora e a incerteza é declarada ----------------------

unset CONTEXT_WINDOW
make_transcript "$PROJECTS/$SLUG/cabe.jsonl" "assistant:0:0:150000"
run_watch --session "$PROJECTS/$SLUG/cabe.jsonl" --json
expect_match "B1 · id ambíguo presume a MENOR janela" '"janela": 200000'
expect_match "B1 · origem diz que o id é ambíguo" '"janela_origem": "modelo-ambiguo:claude-opus-5"'
expect_match "B1 · janela presumida é declarada não confiável" '"janela_confiavel": false'
expect_code "B1 · presunção conservadora avisa cedo (150k/200k = 75%)" 20
run_watch --session "$PROJECTS/$SLUG/cabe.jsonl"
expect_match "B1 · texto declara a presunção" "JANELA PRESUMIDA"

make_transcript "$PROJECTS/$SLUG/um-mega.jsonl" "assistant:0:0:300000"
python3 - "$PROJECTS/$SLUG/um-mega.jsonl" <<'PY'
import json, sys
path = sys.argv[1]
lines = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
lines[-1]["message"]["model"] = "claude-opus-5[1m]"
with open(path, "w", encoding="utf-8") as fh:
    for entry in lines:
        fh.write(json.dumps(entry) + "\n")
PY
run_watch --session "$PROJECTS/$SLUG/um-mega.jsonl" --json
expect_match "B1 · id explícito [1m] usa 1M" '"janela": 1000000'
expect_code "B1 · id explícito [1m] fica verde" 0

# --- B5: presunção REFUTADA pela própria medição ----------------------------------------
# 300.005 tokens vivos não cabem em 200.000: a medida prova que a presunção está errada.
# Insistir nela imprimiria "150%", número que o próprio dado desmente, e travaria o alarme
# no topo da escala (nada é maior que `critico`) — o mecanismo morreria calado depois.

run_watch --session "$PROJECTS/$SLUG/misto.jsonl" --json
expect_match "B5 · janela refutada sobe um degrau plausível" '"janela": 1000000'
expect_match "B5 · a origem registra a refutação" '"janela_origem": "refutado:modelo-ambiguo:claude-opus-5"'
expect_match "B5 · continua declarada não confiável" '"janela_confiavel": false'
expect_code "B5 · não imprime número autorrefutável (30%, não 150%)" 0
run_watch --session "$PROJECTS/$SLUG/misto.jsonl"
expect_match "B5 · texto explica a refutação" "REFUTAÇÃO"
expect_nomatch "B5 · percentual acima de 100 não sobra" "1[0-9][0-9]\.[0-9]%"

# Janela CONFIGURADA nunca é refutada: se o usuário disse 200k, 300k é estouro real.
CONTEXT_WINDOW=200000 run_watch --session "$PROJECTS/$SLUG/misto.jsonl" --json
expect_code "B5 · janela configurada não é escalonada" 30
expect_match "B5 · janela configurada é respeitada como dita" '"janela": 200000'

# Refutação que esgota os degraus conhecidos → sem-telemetria, não um número inventado.
make_transcript "$PROJECTS/$SLUG/gigante.jsonl" "assistant:0:0:1500000"
run_watch --session "$PROJECTS/$SLUG/gigante.jsonl"
expect_code "B5 · medida acima de todo degrau conhecido sai 40" 40
expect_match "B5 · e diz por quê" "incompatível com qualquer janela conhecida"
no_stacktrace "B5 · sem stack trace"

# --- B3: hermetismo — a suíte não pode depender do ~/.claude da máquina -----------------

mkdir -p "$TMP/home/.claude"
printf '{"autoCompactWindow": 500000}\n' > "$TMP/home/.claude/settings.json"
run_watch --session "$PROJECTS/$SLUG/misto.jsonl" --json
expect_match "B3 · autoCompactWindow do usuário é respeitado" '"janela": 500000'
expect_match "B3 · origem aponta o settings do usuário" '"janela_origem": "settings:usuario:autoCompactWindow"'
expect_match "B3 · janela configurada é confiável" '"janela_confiavel": true'
CONTEXT_WINDOW=250000 run_watch --session "$PROJECTS/$SLUG/misto.jsonl" --json
expect_match "B3 · CONTEXT_WINDOW tem precedência sobre o settings" '"janela": 250000'
rm -f "$TMP/home/.claude/settings.json"

# --- S1: só campos com formato conhecido chegam ao stdout ------------------------------

python3 - "$PROJECTS/$SLUG/meta-fuzz.jsonl" <<'PY'
import json, sys
entry = {"type": "assistant", "isSidechain": False,
         "timestamp": "CANARIO-NO-TIMESTAMP",
         "message": {"model": "CANARIO NO MODELO ${}",
                     "usage": {"input_tokens": 1, "cache_creation_input_tokens": 0,
                               "cache_read_input_tokens": 99999}}}
with open(sys.argv[1], "w", encoding="utf-8") as fh:
    fh.write(json.dumps(entry) + "\n")
PY
run_watch --session "$PROJECTS/$SLUG/meta-fuzz.jsonl" --json
expect_nomatch "S1 · modelo fora do formato não chega ao stdout" "CANARIO"
run_watch --session "$PROJECTS/$SLUG/meta-fuzz.jsonl"
expect_nomatch "S1 · texto também não ecoa o canário" "CANARIO"
expect_code "S1 · medição continua funcionando sem os metadados" 0

# --- hook: avisa só quando a zona sobe (critério 8) -------------------------------------

hook_call() { # janela → saída do hook
  out="$(CONTEXT_WINDOW="$1" python3 "$WATCH" --hook --cwd "$FAKE_CWD" \
        --session "$PROJECTS/$SLUG/misto.jsonl" <<<'{"session_id":"teste-hook","cwd":"/fake/repo"}' 2>&1)"
  code=$?
}

hook_call 1000000
expect_code "hook · exit 0 sempre" 0
[[ -z "$out" ]] && report "hook · zona verde inicial é silenciosa" 1 || report "hook · zona verde inicial é silenciosa" 0

hook_call 400000   # 75.0% → preparar (sobe)
expect_match "hook · avisa quando a zona sobe" "systemMessage"
expect_match "hook · aviso traz a ação da zona" "snapshot"

hook_call 400000   # mesma zona → silêncio
[[ -z "$out" ]] && report "hook · não repete na mesma zona" 1 || report "hook · não repete na mesma zona" 0

hook_call 1000000  # zona cai → silêncio
[[ -z "$out" ]] && report "hook · zona que cai não avisa" 1 || report "hook · zona que cai não avisa" 0

hook_call 340000   # 88% → critico (sobe de novo)
expect_match "hook · volta a avisar quando sobe de novo" "CRITICO"

out="$(python3 "$WATCH" --hook --cwd /diretorio/que/nao/existe <<<'{}' 2>&1)"; code=$?
expect_code "hook · sem telemetria não quebra a sessão" 0
[[ -z "$out" ]] && report "hook · sem telemetria é silencioso" 1 || report "hook · sem telemetria é silencioso" 0

out="$(python3 "$WATCH" --hook --cwd "$FAKE_CWD" --session "$PROJECTS/$SLUG/misto.jsonl" <<<'não é json' 2>&1)"; code=$?
expect_code "hook · stdin não-JSON não quebra" 0

# --- B1 no caminho automático: o hook precisa comunicar a janela presumida --------------

hook_presumed() { # <session_id> — sem CONTEXT_WINDOW: janela presumida
  out="$(python3 "$WATCH" --hook --cwd "$FAKE_CWD" --session "$PROJECTS/$SLUG/um-mega.jsonl" \
        <<<"{\"session_id\":\"$1\"}" 2>&1)"
  code=$?
}

# 300.000 / 1.000.000 = 30% → zona verde: sem o ramo de incerteza, o hook ficaria mudo.
hook_presumed "b1-verde"
expect_code "B1 · hook com janela presumida sai 0" 0
expect_match "B1 · hook fala mesmo em zona verde quando a janela é presumida" "JANELA PRESUMIDA"
hook_presumed "b1-verde"
[[ -z "$out" ]] && report "B1 · aviso de janela presumida é único por sessão" 1 \
  || report "B1 · aviso de janela presumida é único por sessão" 0

out="$(CONTEXT_WINDOW=2000000 python3 "$WATCH" --hook --cwd "$FAKE_CWD" \
      --session "$PROJECTS/$SLUG/um-mega.jsonl" <<<'{"session_id":"b1-configurado"}' 2>&1)"; code=$?
[[ -z "$out" ]] && report "B1 · janela configurada não gera aviso de incerteza" 1 \
  || report "B1 · janela configurada não gera aviso de incerteza" 0

hook_presumed "b1-subida"   # 1ª chamada: aviso de janela presumida
out="$(CONTEXT_WATCH_THRESHOLDS='0.10,0.20,0.25' python3 "$WATCH" --hook --cwd "$FAKE_CWD" \
      --session "$PROJECTS/$SLUG/um-mega.jsonl" <<<'{"session_id":"b1-subida"}' 2>&1)"; code=$?
expect_match "B1 · aviso de subida de zona carrega o caveat da janela" "JANELA PRESUMIDA"

# --- S2: privacidade também no caminho que fala sozinho ---------------------------------

out="$(python3 "$WATCH" --hook --cwd "$FAKE_CWD" --session "$PROJECTS/$SLUG/misto.jsonl" \
      <<<'{"session_id":"s2-privacidade"}' 2>&1)"
expect_nomatch "S2 · hook não vaza conteúdo da conversa" "SEGREDO-DO-USUARIO"
out="$(python3 "$WATCH" --hook --cwd "$FAKE_CWD" --session "$PROJECTS/$SLUG/meta-fuzz.jsonl" \
      <<<'{"session_id":"s2-canario"}' 2>&1)"
expect_nomatch "S2 · hook não ecoa metadado fora do formato" "CANARIO"

# --- B2: saída quebrada não pode virar exit code ----------------------------------------

bash -c "CONTEXT_WATCH_THRESHOLDS='0.10,0.20,0.25' CLAUDE_PROJECTS_DIR='$PROJECTS' XDG_STATE_HOME='$TMP/state-b2' HOME='$TMP/home' python3 '$WATCH' --hook --cwd '$FAKE_CWD' --session '$PROJECTS/$SLUG/um-mega.jsonl' <<<'{\"session_id\":\"b2-pipe\"}' | true; exit \${PIPESTATUS[0]}"
code=$?; out="(pipe fechado)"
expect_code "B2 · --hook com stdout fechado (| true)" 0

if [[ -w /dev/full ]]; then
  bash -c "CONTEXT_WATCH_THRESHOLDS='0.10,0.20,0.25' CLAUDE_PROJECTS_DIR='$PROJECTS' XDG_STATE_HOME='$TMP/state-b2' HOME='$TMP/home' python3 '$WATCH' --hook --cwd '$FAKE_CWD' --session '$PROJECTS/$SLUG/um-mega.jsonl' <<<'{\"session_id\":\"b2-full\"}' > /dev/full 2>/dev/null"
  code=$?; out="(dispositivo cheio)"
  expect_code "B2 · --hook com stdout em /dev/full" 0
else
  report "B2 · /dev/full indisponível nesta máquina (teste pulado)" 1
fi

bash -c "CONTEXT_WINDOW=200000 CLAUDE_PROJECTS_DIR='$PROJECTS' HOME='$TMP/home' python3 '$WATCH' --cwd '$FAKE_CWD' --session '$PROJECTS/$SLUG/misto.jsonl' | true; exit \${PIPESTATUS[0]}"
code=$?; out="(pipe fechado)"
expect_code "B2 · modo normal mantém o exit code da zona sob pipe fechado" 30

# --- B6: fd de saída FECHADO (`>&-`) — sys.stdout é None, não um arquivo quebrado -------
# Baseline: `python3 -c 'print("x")' >&-` sai 0. O script não pode ficar pior que isso.

hook_fd_closed() {
  bash -c "CLAUDE_PROJECTS_DIR='$PROJECTS' XDG_STATE_HOME='$TMP/state-b6' HOME='$TMP/home' $1 python3 '$WATCH' --hook --cwd '$FAKE_CWD' --session '$2' <<<'{\"session_id\":\"b6\"}' >&- 2>'$TMP/b6.err'"
  code=$?
  out="$(cat "$TMP/b6.err" 2>/dev/null)"
}

hook_fd_closed "CONTEXT_WINDOW=1000000" "$PROJECTS/$SLUG/um-mega.jsonl"
expect_code "B6 · --hook com stdout fechado (>&-), zona verde silenciosa" 0
no_stacktrace "B6 · sem traceback com stdout fechado"

hook_fd_closed "CONTEXT_WINDOW=310000" "$PROJECTS/$SLUG/misto.jsonl"
expect_code "B6 · --hook com stdout fechado tendo mensagem a emitir" 0
no_stacktrace "B6 · sem traceback ao tentar emitir com fd fechado"

bash -c "CONTEXT_WINDOW=200000 CLAUDE_PROJECTS_DIR='$PROJECTS' HOME='$TMP/home' python3 '$WATCH' --cwd '$FAKE_CWD' --session '$PROJECTS/$SLUG/misto.jsonl' >&- 2>/dev/null"
code=$?; out="(fd fechado)"
expect_code "B6 · modo normal com stdout fechado mantém a zona" 30

# --- B5 no canal automático: refutação anunciada e alarme que volta a falar --------------

hook_at() { # <session_id> <janela> <transcript> — hook com estado isolado por sessão
  out="$(CONTEXT_WINDOW="$2" XDG_STATE_HOME="$TMP/state-b5" python3 "$WATCH" --hook \
        --cwd "$FAKE_CWD" --session "$3" <<<"{\"session_id\":\"$1\"}" 2>&1)"
  code=$?
}

out="$(XDG_STATE_HOME="$TMP/state-b5" python3 "$WATCH" --hook --cwd "$FAKE_CWD" \
      --session "$PROJECTS/$SLUG/misto.jsonl" <<<'{"session_id":"b5-refutado"}' 2>&1)"; code=$?
expect_code "B5 · hook com janela refutada sai 0" 0
expect_match "B5 · hook anuncia a refutação (obrigatório)" "REFUTAÇÃO"
expect_nomatch "B5 · hook não grita handoff com 30% de uso real" "handoff agora"

# O alarme precisa voltar a falar quando a zona sobe DE VERDADE — a falha do loop 2 foi o
# índice pinado em `critico` por uma presunção errada, calando o hook para o resto da sessão.
make_transcript "$PROJECTS/$SLUG/cresce-1.jsonl" "assistant:0:0:100000"
make_transcript "$PROJECTS/$SLUG/cresce-2.jsonl" "assistant:0:0:650000"
make_transcript "$PROJECTS/$SLUG/cresce-3.jsonl" "assistant:0:0:780000"
make_transcript "$PROJECTS/$SLUG/cresce-4.jsonl" "assistant:0:0:900000"

hook_at "b5-crescendo" 1000000 "$PROJECTS/$SLUG/cresce-1.jsonl"
[[ -z "$out" ]] && report "B5 · 10% verde: silêncio" 1 || report "B5 · 10% verde: silêncio" 0
hook_at "b5-crescendo" 1000000 "$PROJECTS/$SLUG/cresce-2.jsonl"
expect_match "B5 · 65%: fala (1ª vez)" "ATENCAO"
hook_at "b5-crescendo" 1000000 "$PROJECTS/$SLUG/cresce-3.jsonl"
expect_match "B5 · 78%: fala de novo (2ª vez)" "PREPARAR"
hook_at "b5-crescendo" 1000000 "$PROJECTS/$SLUG/cresce-4.jsonl"
expect_match "B5 · 90%: fala de novo (3ª vez)" "CRITICO"
expect_match "B5 · e manda fazer o handoff no momento certo" "handoff agora"

# Pino do índice: zona alta gravada sob uma janela e régua trocada em seguida.
hook_at "b5-pino" 200000 "$PROJECTS/$SLUG/cabe.jsonl"     # 150k/200k = 75% → preparar
expect_match "B5 · zona alta registrada sob a janela antiga" "PREPARAR"
hook_at "b5-pino" 1000000 "$PROJECTS/$SLUG/cresce-1.jsonl" # régua nova: 10% → verde
[[ -z "$out" ]] && report "B5 · troca de régua não gera alarme" 1 || report "B5 · troca de régua não gera alarme" 0
hook_at "b5-pino" 1000000 "$PROJECTS/$SLUG/cresce-2.jsonl" # 65% → atenção
expect_match "B5 · índice não fica pinado após troca de régua" "ATENCAO"

# --- resultado --------------------------------------------------------------------------

printf '\n%s\n' "----------------------------------------"
printf 'context-watch: %d passaram, %d falharam\n' "$pass" "$fail"
(( fail == 0 )) || exit 1
