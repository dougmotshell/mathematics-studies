#!/usr/bin/env bash
# validate-content-test.sh — suíte do validador de contrato de conteúdo (TCK-0014).
#
# Por que bash + Python stdlib e não um framework de teste: o `ADR-0003` não decidiu
# runner, o ticket proíbe dependência nova e o repositório já tem esse precedente em
# `tools/context-watch-test.sh`. O que os critérios 1, 3 e 5 julgam é a SUPERFÍCIE DE
# LINHA DE COMANDO — código de saída e texto da mensagem —, e não funções internas;
# testar pelo CLI é testar exatamente o contrato que o pipeline vai consumir.
#
# Todas as fixtures são construídas em diretório temporário a partir de uma CÓPIA do nó
# piloto, com UMA mutação por caso: assim cada teste prova que o validador pega aquele
# defeito e que não inventa outros. `content/` nunca é tocado (há verificação de hash
# no fim da suíte).
#
# Uso: bash scripts/validate-content-test.sh [-v]

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VALIDATOR="$SCRIPT_DIR/validate-content.py"
PILOT="$REPO_ROOT/content/high-school/algebra/quadratic-equations"
NODE_REL="high-school/algebra/quadratic-equations"
VERBOSE=0
[[ "${1:-}" == "-v" ]] && VERBOSE=1

TMP="$(mktemp -d "${TMPDIR:-/tmp}/validate-content-test.XXXXXX")"
trap 'rm -rf "$TMP"' EXIT

pass=0; fail=0
out=""; code=0

CONTENT_HASH_BEFORE="$(find "$REPO_ROOT/content" -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum)"

# --- helpers ----------------------------------------------------------------------------

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
  grep -Eq -- "$re" <<<"$out" && report "$name" 1 || report "$name (não casou: $re)" 0
}

expect_nomatch() {
  local name="$1" re="$2"
  grep -Eq -- "$re" <<<"$out" && report "$name (casou indevidamente: $re)" 0 || report "$name" 1
}

no_stacktrace() {
  grep -q "Traceback" <<<"$out" && report "$1" 0 || report "$1" 1
}

count_violations() { grep -cE '\[[A-Z0-9-]+\]' <<<"$out"; }

# new_fixture <nome> → cria $TMP/<nome>/content/<NODE_REL> a partir do piloto; ecoa a raiz
new_fixture() {
  local root="$TMP/$1/content"
  mkdir -p "$root/$NODE_REL"
  cp "$PILOT"/*.json "$PILOT"/*.md "$root/$NODE_REL/"
  printf '%s' "$root"
}

# edit_json <arquivo> <statements python operando sobre `data`>  (sem `$` no snippet)
edit_json() {
  python3 - "$1" <<PY
import json, sys
p = sys.argv[1]
with open(p, encoding="utf-8") as fh:
    data = json.load(fh)
$2
with open(p, "w", encoding="utf-8") as fh:
    json.dump(data, fh, ensure_ascii=False, indent=2)
PY
}

run_validate() { # <raiz> [args...]
  local root="$1"; shift
  out="$(python3 "$VALIDATOR" --root "$root" "$@" 2>&1)"
  code=$?
}

# --- caso 1: o nó piloto real passa sem alteração de content/ (critério 6) --------------

out="$(python3 "$VALIDATOR" "$NODE_REL" 2>&1)"; code=$?
expect_code "1 · nó piloto real passa" 0
expect_match "1 · declara contrato íntegro" "Contrato íntegro: 1 nó"
no_stacktrace "1 · sem stack trace"

out="$(python3 "$VALIDATOR" 2>&1)"; code=$?
expect_code "1b · acervo inteiro passa" 0

# --- caso 2: cópia intacta — nenhum falso positivo (critério 4) -------------------------

ROOT_OK="$(new_fixture valido)"
run_validate "$ROOT_OK"
expect_code "2 · cópia intacta do piloto passa" 0
expect_nomatch "2 · tolerance 0 (qe-003) não vira violação" "qe-003"
expect_nomatch "2 · prerequisites vazio não vira violação" "prerequisite"

ROOT_TOL0="$(new_fixture tolerancia-zero)"
edit_json "$ROOT_TOL0/$NODE_REL/exercises.json" 'data["items"][4]["tolerance"] = 0'
run_validate "$ROOT_TOL0"
expect_code "2b · tolerance 0 também em qe-005 continua válido" 0

# --- caso 3 (CA-13): multiple-choice sem nenhuma opção correta --------------------------

ROOT_NOCORRECT="$(new_fixture mc-sem-correta)"
edit_json "$ROOT_NOCORRECT/$NODE_REL/exercises.json" '
for opt in data["items"][0]["options"]:
    opt["correct"] = False'
run_validate "$ROOT_NOCORRECT"
expect_code "3 · CA-13 multiple-choice sem opção correta falha" 1
expect_match "3 · regra nomeada" "\[MC-NO-CORRECT-OPTION\]"
expect_match "3 · aponta arquivo, item e índice" "exercises\.json: items\[0\] \(id=qe-001\)"
expect_match "3 · mensagem acionável" "não pode ser apresentado ao aluno"
expect_match "3 · resumo visível" "CONTRATO VIOLADO"
[[ "$(count_violations)" == "1" ]] && report "3 · uma única violação, sem ruído" 1 \
  || { report "3 · uma única violação, sem ruído" 0; }
no_stacktrace "3 · sem stack trace"

# --- caso 4: multiple-choice com mais de uma opção correta ------------------------------

ROOT_MULTI="$(new_fixture mc-duas-corretas)"
edit_json "$ROOT_MULTI/$NODE_REL/exercises.json" 'data["items"][1]["options"][2]["correct"] = True'
run_validate "$ROOT_MULTI"
expect_code "4 · multiple-choice com duas corretas falha" 1
expect_match "4 · regra nomeada" "\[MC-MULTIPLE-CORRECT-OPTIONS\]"
expect_match "4 · aponta o item" "items\[1\] \(id=qe-002\)"
expect_match "4 · lista as opções conflitantes" "2 opções corretas \(a, c\)"

# --- caso 5: numeric com tolerance negativa ---------------------------------------------

ROOT_NEG="$(new_fixture tolerancia-negativa)"
edit_json "$ROOT_NEG/$NODE_REL/exercises.json" 'data["items"][2]["tolerance"] = -0.5'
run_validate "$ROOT_NEG"
expect_code "5 · tolerance negativa falha" 1
expect_match "5 · regra nomeada" "\[NUMERIC-TOLERANCE-NEGATIVE\]"
expect_match "5 · aponta o item numeric" "items\[2\] \(id=qe-003\)"
expect_match "5 · explica a consequência" "[Nn]enhuma resposta seria aceita"

ROOT_SEMTOL="$(new_fixture tolerancia-ausente)"
edit_json "$ROOT_SEMTOL/$NODE_REL/exercises.json" 'del data["items"][2]["tolerance"]'
run_validate "$ROOT_SEMTOL"
expect_code "5b · tolerance ausente falha (ausente != 0)" 1
expect_match "5b · regra nomeada" "\[NUMERIC-TOLERANCE-MISSING\]"

ROOT_ANS="$(new_fixture answer-texto)"
edit_json "$ROOT_ANS/$NODE_REL/exercises.json" 'data["items"][4]["answer"] = "3,5"'
run_validate "$ROOT_ANS"
expect_code "5c · answer numeric em texto falha" 1
expect_match "5c · regra nomeada" "\[NUMERIC-ANSWER-NOT-NUMBER\]"
expect_match "5c · orienta o formato de máquina" "ponto decimal"

# --- caso 6 (CA-14): chave de idioma faltando em campo localizado -----------------------

ROOT_I18N="$(new_fixture meta-sem-en)"
edit_json "$ROOT_I18N/$NODE_REL/meta.json" 'del data["title"]["en-US"]'
run_validate "$ROOT_I18N"
expect_code "6 · CA-14 meta.json.title sem en-US falha" 1
expect_match "6 · regra nomeada" "\[LOCALIZED-MISSING-LANG\]"
expect_match "6 · aponta arquivo e campo" "meta\.json: title: .*'title' sem a chave 'en-US'"
expect_match "6 · diz que não há fallback" "não há fallback"

ROOT_HINT="$(new_fixture dica-sem-en)"
edit_json "$ROOT_HINT/$NODE_REL/exercises.json" 'del data["items"][0]["hints"][1]["en-US"]'
run_validate "$ROOT_HINT"
expect_code "6b · dica sem en-US falha" 1
expect_match "6b · localiza a dica exata" "items\[0\] \(id=qe-001\)\.hints\[1\]"

ROOT_FB="$(new_fixture feedback-sem-pt)"
edit_json "$ROOT_FB/$NODE_REL/exercises.json" 'del data["items"][0]["options"][1]["feedback"]["pt-BR"]'
run_validate "$ROOT_FB"
expect_code "6c · feedback de alternativa sem pt-BR falha" 1
expect_match "6c · localiza a alternativa" "options\[1\] \(id=b\): \[LOCALIZED-MISSING-LANG\]"

ROOT_XLANG="$(new_fixture idioma-extra)"
edit_json "$ROOT_XLANG/$NODE_REL/meta.json" 'data["summary"]["es-ES"] = "hola"'
run_validate "$ROOT_XLANG"
expect_code "6d · idioma fora do contrato falha" 1
expect_match "6d · regra nomeada" "\[LOCALIZED-UNKNOWN-LANG\]"

# --- caso 7: identidade do nó divergente do caminho -------------------------------------

ROOT_NODEID="$(new_fixture nodeid-divergente)"
edit_json "$ROOT_NODEID/$NODE_REL/exercises.json" 'data["nodeId"] = "high-school/algebra/linear-equations"'
run_validate "$ROOT_NODEID"
expect_code "7 · nodeId divergente do caminho falha" 1
expect_match "7 · regra nomeada" "\[NODE-ID-MISMATCH\]"
expect_match "7 · mostra o valor e o caminho real" "nodeId é 'high-school/algebra/linear-equations' mas o arquivo está no nó '$NODE_REL'"

ROOT_METAID="$(new_fixture metaid-divergente)"
edit_json "$ROOT_METAID/$NODE_REL/meta.json" 'data["id"] = "middle-school/algebra/quadratic-equations"'
run_validate "$ROOT_METAID"
expect_code "7b · meta.json.id divergente falha" 1
expect_match "7b · regra nomeada" "\[META-ID-MISMATCH\]"
expect_match "7b · cita RF-17 (URL pública)" "RF-17"

ROOT_ASSESS="$(new_fixture assessments-nodeid)"
python3 - "$ROOT_ASSESS/$NODE_REL" <<'PY'
import json, sys, pathlib
node = pathlib.Path(sys.argv[1])
data = json.loads((node / "exercises.json").read_text(encoding="utf-8"))
data["nodeId"] = "high-school/algebra/outro-no"
(node / "assessments.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
PY
run_validate "$ROOT_ASSESS"
expect_code "7c · assessments.json também é validado" 1
expect_match "7c · aponta o arquivo certo" "assessments\.json: nodeId: \[NODE-ID-MISMATCH\]"

# --- caso 8: gabarito ambíguo e tipo desconhecido ---------------------------------------

ROOT_BOOL="$(new_fixture correct-string)"
edit_json "$ROOT_BOOL/$NODE_REL/exercises.json" 'data["items"][0]["options"][0]["correct"] = "true"'
run_validate "$ROOT_BOOL"
expect_code "8 · 'correct' em texto falha" 1
expect_match "8 · regra nomeada" "\[CORRECT-NOT-BOOLEAN\]"
expect_match "8 · e o item fica sem gabarito" "\[MC-NO-CORRECT-OPTION\]"

ROOT_TYPE="$(new_fixture tipo-desconhecido)"
edit_json "$ROOT_TYPE/$NODE_REL/exercises.json" 'data["items"][0]["type"] = "quiz"'
run_validate "$ROOT_TYPE"
expect_code "8b · type desconhecido falha" 1
expect_match "8b · regra nomeada" "\[ITEM-TYPE-UNKNOWN\]"

# --- caso 9: TODAS as violações, não só a primeira (critério 1) -------------------------

ROOT_MULTI_DEF="$(new_fixture defeitos-multiplos)"
edit_json "$ROOT_MULTI_DEF/$NODE_REL/meta.json" '
del data["title"]["en-US"]
data["id"] = "outro/caminho/errado"'
edit_json "$ROOT_MULTI_DEF/$NODE_REL/exercises.json" '
data["nodeId"] = "outro/caminho/errado"
for opt in data["items"][0]["options"]:
    opt["correct"] = False
data["items"][1]["options"][2]["correct"] = True
data["items"][2]["tolerance"] = -1
del data["items"][4]["answer"]'
run_validate "$ROOT_MULTI_DEF"
expect_code "9 · nó com 7 defeitos falha" 1
n="$(count_violations)"
[[ "$n" == "7" ]] && report "9 · lista as 7 violações, não só a primeira" 1 \
  || { out="violações listadas: $n"$'\n'"$out"; report "9 · lista as 7 violações, não só a primeira" 0; }
for rule in LOCALIZED-MISSING-LANG META-ID-MISMATCH NODE-ID-MISMATCH MC-NO-CORRECT-OPTION \
            MC-MULTIPLE-CORRECT-OPTIONS NUMERIC-TOLERANCE-NEGATIVE NUMERIC-ANSWER-MISSING; do
  expect_match "9 · inclui $rule" "\[$rule\]"
done
expect_match "9 · resumo conta as violações" "CONTRATO VIOLADO: 7 violação"

# --- caso 10: arquivo ilegível e nó sem meta.json ---------------------------------------

ROOT_BROKEN="$(new_fixture json-quebrado)"
printf '{ "nodeId": "x", "items": [ }\n' > "$ROOT_BROKEN/$NODE_REL/exercises.json"
run_validate "$ROOT_BROKEN"
expect_code "10 · JSON inválido falha sem quebrar" 1
expect_match "10 · regra nomeada" "\[JSON-INVALID\]"
expect_match "10 · aponta linha e coluna" "linha [0-9]+, coluna [0-9]+"
no_stacktrace "10 · sem stack trace"

ROOT_NOMETA="$(new_fixture sem-meta)"
mkdir -p "$ROOT_NOMETA/high-school/algebra/vazio"
cp "$PILOT/exercises.json" "$ROOT_NOMETA/high-school/algebra/vazio/"
run_validate "$ROOT_NOMETA" "$ROOT_NOMETA/high-school/algebra/vazio"
expect_code "10b · diretório sem meta.json não some em silêncio" 1
expect_match "10b · regra nomeada" "\[NODE-META-MISSING\]"
expect_match "10b · o nodeId do arquivo copiado também acusa o nó errado" "\[NODE-ID-MISMATCH\]"

mkdir -p "$TMP/vazio/content"
run_validate "$TMP/vazio/content"
expect_code "10c · raiz sem nenhum nó é erro de uso, não 'tudo certo'" 2
expect_match "10c · mensagem explícita" "nenhum nó de conteúdo encontrado"

# --- caso 11: nó sintético mínimo válido (independe do piloto) --------------------------

ROOT_MIN="$TMP/minimo/content"
mkdir -p "$ROOT_MIN/elementary/arithmetic/counting"
python3 - "$ROOT_MIN/elementary/arithmetic/counting" <<'PY'
import json, pathlib, sys
node = pathlib.Path(sys.argv[1])
loc = lambda pt, en: {"pt-BR": pt, "en-US": en}
(node / "meta.json").write_text(json.dumps({
    "id": "elementary/arithmetic/counting",
    "stage": "elementary", "area": "arithmetic",
    "title": loc("Contagem", "Counting"),
    "summary": loc("Contar objetos.", "Counting objects."),
    "prerequisites": [], "difficulty": 1, "status": "draft",
    "languages": ["pt-BR", "en-US"], "skills": ["count"],
}, ensure_ascii=False, indent=2), encoding="utf-8")
(node / "exercises.json").write_text(json.dumps({
    "nodeId": "elementary/arithmetic/counting", "version": 1,
    "items": [{
        "id": "ct-001", "type": "numeric", "difficulty": 1, "skills": ["count"],
        "stem": loc("Quantos dedos há em uma mão?", "How many fingers are on one hand?"),
        "answer": 5, "tolerance": 0,
        "hints": [loc("Conte um a um.", "Count one by one.")],
        "solution": loc("São 5 dedos.", "There are 5 fingers."),
    }],
}, ensure_ascii=False, indent=2), encoding="utf-8")
PY
run_validate "$ROOT_MIN"
expect_code "11 · nó sintético mínimo com tolerance 0 e prerequisites [] passa" 0
expect_match "11 · confirma 1 nó validado" "1 nó\(s\) validado"

# --- caso 12: interface de linha de comando ---------------------------------------------

run_validate "$ROOT_NEG" --json
expect_code "12 · --json mantém o código de saída" 1
python3 -c "
import json,sys
d=json.loads(sys.stdin.read())
assert d['violations']==1 and d['items'][0]['rule']=='NUMERIC-TOLERANCE-NEGATIVE', d
assert d['items'][0]['file'].endswith('exercises.json') and 'qe-003' in d['items'][0]['locator'], d
" <<<"$out" && report "12 · --json traz arquivo, item e regra estruturados" 1 \
  || report "12 · --json traz arquivo, item e regra estruturados" 0

run_validate "$ROOT_NEG" --quiet
expect_code "12b · --quiet mantém o código de saída" 1
[[ -z "$out" ]] && report "12b · --quiet não imprime nada" 1 || report "12b · --quiet não imprime nada" 0

out="$(python3 "$VALIDATOR" caminho/que/nao/existe 2>&1)"; code=$?
expect_code "12c · caminho inexistente é erro de uso, não violação" 2
expect_match "12c · mensagem explícita" "ERRO DE USO"

out="$(python3 "$VALIDATOR" --root "$ROOT_OK" "$ROOT_OK/$NODE_REL" 2>&1)"; code=$?
expect_code "12d · aceita caminho absoluto de nó" 0

bash -c "python3 '$VALIDATOR' --root '$ROOT_NEG' | true; exit \${PIPESTATUS[0]}"
code=$?; out="(pipe fechado)"
expect_code "12e · pipe fechado não altera o veredito" 1

bash -c "python3 '$VALIDATOR' --root '$ROOT_NEG' >&- 2>'$TMP/fd.err'"
code=$?; out="$(cat "$TMP/fd.err" 2>/dev/null)"
expect_code "12f · stdout fechado (>&-) não altera o veredito" 1
no_stacktrace "12f · sem traceback com stdout fechado"

bash -c "python3 '$VALIDATOR' --root '$ROOT_OK' >&- 2>'$TMP/fd2.err'"
code=$?; out="$(cat "$TMP/fd2.err" 2>/dev/null)"
expect_code "12g · stdout fechado com contrato íntegro continua 0" 0

# --- caso 14 (B1): subnó quebrado é visto a partir do nó pai ----------------------------
# Regressão do REJECT [006]: `find_nodes` parava no alvo e um subnó quebrado sumia.
# Portão que enxerga menos conforme o acervo cresce dá confiança falsa (L-019).

ROOT_SUB="$(new_fixture subno-quebrado)"
SUB="$ROOT_SUB/$NODE_REL/discriminant"
mkdir -p "$SUB"
python3 - "$SUB" <<'PY'
import json, pathlib, sys
sub = pathlib.Path(sys.argv[1])
(sub / "meta.json").write_text(json.dumps({
    "id": "high-school/algebra/errado", "stage": "high-school", "area": "algebra",
    "title": {"pt-BR": "Discriminante"}, "summary": "não é objeto localizado",
    "prerequisites": [], "difficulty": 3, "status": "draft",
    "languages": ["pt-BR", "en-US"], "skills": ["interpret-discriminant"],
}, ensure_ascii=False, indent=2), encoding="utf-8")
(sub / "exercises.json").write_text(json.dumps({
    "nodeId": "high-school/algebra/outro-no", "version": 1,
    "items": [{"id": "dc-001", "type": "numeric", "difficulty": 2,
               "skills": ["interpret-discriminant"]}],
}, ensure_ascii=False, indent=2), encoding="utf-8")
PY

run_validate "$ROOT_SUB" "$ROOT_SUB/$NODE_REL"
expect_code "14 · B1 alvo = nó pai enxerga o subnó quebrado" 1
expect_match "14 · conta os dois nós" "em 2 nó\(s\)"
expect_match "14 · localiza o subnó" "quadratic-equations/discriminant/meta\.json"
expect_match "14 · pega a identidade do subnó" "\[META-ID-MISMATCH\]"
expect_match "14 · pega o item quebrado do subnó" "items\[0\] \(id=dc-001\)"
sub_only="$out"

run_validate "$ROOT_SUB"
expect_code "14b · alvo = raiz dá o mesmo veredito" 1
[[ "$(count_violations)" == "$(grep -cE '\[[A-Z0-9-]+\]' <<<"$sub_only")" ]] \
  && report "14b · raiz e nó pai acusam o mesmo número de violações" 1 \
  || report "14b · raiz e nó pai acusam o mesmo número de violações" 0

run_validate "$ROOT_SUB" "$ROOT_SUB/$NODE_REL/discriminant"
expect_code "14c · alvo = o próprio subnó continua falhando" 1

# Pai + filho íntegros não podem virar falso positivo.
ROOT_SUBOK="$(new_fixture subno-valido)"
mkdir -p "$ROOT_SUBOK/$NODE_REL/discriminant"
python3 - "$ROOT_SUBOK/$NODE_REL" <<'PY'
import json, pathlib, sys
node = pathlib.Path(sys.argv[1])
meta = json.loads((node / "meta.json").read_text(encoding="utf-8"))
meta["id"] = "high-school/algebra/quadratic-equations/discriminant"
(node / "discriminant" / "meta.json").write_text(
    json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
PY
run_validate "$ROOT_SUBOK" "$ROOT_SUBOK/$NODE_REL"
expect_code "14d · pai + subnó íntegros passam" 0
expect_match "14d · e os dois foram validados" "2 nó\(s\) validado\(s\)"

# --- caso 15 (B2): saída de erro quebrada não altera o exit 2 ---------------------------

usage_exit() { # <descrição> <comando bash> — ecoa o código
  bash -c "$1"
  code=$?; out="(saída de erro quebrada)"
}

usage_exit "python3 '$VALIDATOR' nao/existe 2>&1 | true; exit \${PIPESTATUS[0]}"
expect_code "15 · B2 caminho inexistente com stderr em pipe fechado" 2
usage_exit "python3 '$VALIDATOR' nao/existe 2>/dev/full"
expect_code "15b · B2 caminho inexistente com stderr em /dev/full" 2
usage_exit "python3 '$VALIDATOR' --root '$TMP/vazio/content' 2>&1 | true; exit \${PIPESTATUS[0]}"
expect_code "15c · B2 raiz sem nó com stderr em pipe fechado" 2
usage_exit "python3 '$VALIDATOR' --xx 2>&1 | true; exit \${PIPESTATUS[0]}"
expect_code "15d · B2 opção inválida (argparse) com stderr em pipe fechado" 2
usage_exit "python3 '$VALIDATOR' --xx 2>/dev/full"
expect_code "15e · B2 opção inválida com stderr em /dev/full" 2
usage_exit "python3 '$VALIDATOR' nao/existe 2>&-"
expect_code "15f · B2 stderr fechado (2>&-)" 2
usage_exit "python3 '$VALIDATOR' --help >/dev/null 2>&1"
expect_code "15g · --help continua 0" 0

out="$(bash -c "python3 '$VALIDATOR' nao/existe 2>&1")"; code=$?
no_stacktrace "15h · erro de uso não imprime traceback"
expect_match "15h · e continua explicando o motivo" "ERRO DE USO"

# --- caso 16 (S3): terminal ASCII não pode engolir a mensagem ---------------------------

out="$(PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 LC_ALL=POSIX LANG=POSIX \
      python3 "$VALIDATOR" --root "$ROOT_NEG" 2>&1)"; code=$?
expect_code "16 · S3 stdout ASCII mantém o veredito" 1
expect_match "16 · S3 a violação continua sendo impressa" "NUMERIC-TOLERANCE-NEGATIVE"
expect_match "16 · S3 com o item localizado" "id=qe-003"

# --- caso 17: sugestões S1, S2, S4, S5 --------------------------------------------------

ROOT_EMPTY="$(new_fixture itens-vazios)"
edit_json "$ROOT_EMPTY/$NODE_REL/exercises.json" 'data["items"] = []'
run_validate "$ROOT_EMPTY"
expect_code "17 · S1 exercises.json com items vazio falha" 1
expect_match "17 · S1 regra nomeada" "\[ITEMS-EMPTY\]"

ROOT_DUPID="$(new_fixture id-item-duplicado)"
edit_json "$ROOT_DUPID/$NODE_REL/exercises.json" 'data["items"][1]["id"] = data["items"][0]["id"]'
run_validate "$ROOT_DUPID"
expect_code "17b · S2 id de item duplicado falha" 1
expect_match "17b · S2 regra nomeada" "\[ITEM-ID-DUPLICATE\]"
expect_match "17b · S2 aponta a segunda ocorrência" "items\[1\] \(id=qe-001\)"

ROOT_DUPKEY="$(new_fixture chave-json-duplicada)"
python3 - "$ROOT_DUPKEY/$NODE_REL/exercises.json" <<'PY'
import pathlib, sys
p = pathlib.Path(sys.argv[1])
raw = p.read_text(encoding="utf-8")
p.write_text(raw.replace('"correct": true,', '"correct": true, "correct": false,', 1),
             encoding="utf-8")
PY
run_validate "$ROOT_DUPKEY"
expect_code "17c · S4 chave JSON duplicada falha" 1
expect_match "17c · S4 regra nomeada" "\[JSON-DUPLICATE-KEY\]"
expect_match "17c · S4 nomeia a chave" "chave 'correct'"

out="$(python3 "$VALIDATOR" --root "$TMP/valido" 2>&1)"; code=$?
expect_code "17d · S5 --root no pai de content/ é erro de uso, não falso positivo" 2
expect_match "17d · S5 aponta a raiz correta" "use --root .*/content"
expect_nomatch "17d · S5 não inventa violação em nó íntegro" "META-ID-MISMATCH"

run_validate "$ROOT_OK" "$ROOT_OK/$NODE_REL/meta.json"
expect_code "17e · alvo apontando para um arquivo vale pelo nó" 0

# --- caso 13: content/ permanece intocado (critério 8) ----------------------------------

CONTENT_HASH_AFTER="$(find "$REPO_ROOT/content" -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum)"
[[ "$CONTENT_HASH_BEFORE" == "$CONTENT_HASH_AFTER" ]] \
  && report "13 · content/ não foi alterado pela suíte" 1 \
  || { out="hash antes != depois"; report "13 · content/ não foi alterado pela suíte" 0; }

# --- resultado ---------------------------------------------------------------------------

printf '\n%s\n' "----------------------------------------"
printf 'validate-content: %d passaram, %d falharam\n' "$pass" "$fail"
(( fail == 0 )) || exit 1
