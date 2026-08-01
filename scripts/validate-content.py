#!/usr/bin/env python3
"""
validate-content.py — validador do contrato de carga de `content/` (spec RF-18).

É o portão que a carga (build ou runtime) usa para decidir se um nó pode ser
apresentado ao aluno. Falha silenciosa é defeito: toda violação sai nomeada, com
arquivo, item e regra, e o processo sai com código 1.

Roda fora de qualquer aplicação — linha de comando e pipeline —, sem dependência
de terceiros (Python 3 stdlib) e sem embutir decisão de framework.

Relação com `scripts/audit-content.py` — **redundância deliberada**, não divisão estanque
(descrição corrigida em 2026-08-01 depois do REJECT [006] do TCK-0014, que mostrou que a
divisão antes declarada aqui era falsa):

  * `audit-content.py` é a auditoria editorial do acervo e cobre bem mais que este arquivo:
    estrutura do nó, taxonomia (`stage`/`area`), grafo de pré-requisitos, trilhas,
    `references.json`, `skills` declaradas, unicidade de `id` de item, `status: published`
    completo, contagem de dicas.
  * Este validador é o **portão de carga** e **repete de propósito** as checagens de que a
    renderização depende. Identidade do nó (`audit-content.py:110`), gabarito
    (`:229-233`), campos localizados (`:131`, `:211`, `:216`, `:221`, `:239`, `:244`) e
    `answer` obrigatório (`:245-247`) **já existem lá**. A repetição é o ponto: um portão de
    carga não pode depender de outra ferramenta ter rodado antes.
  * Onde há sobreposição, **este validador prevalece por ser o mais estrito**. Divergências
    conhecidas em 2026-08-01, ambas com o auditor mais permissivo:
      - `"correct": "false"` (texto) na única alternativa de gabarito — o auditor aprova
        (veracidade implícita em `:229`/`:240`); aqui é `CORRECT-NOT-BOOLEAN` +
        `MC-NO-CORRECT-OPTION`;
      - `title.en-US: 5` (não-texto) — o auditor aprova (`str(5).strip()` em `:85`); aqui é
        `LOCALIZED-NOT-STRING`.
    As duas são defeitos do auditor, com ticket próprio a abrir pelo `tech-lead`; não se
    corrige `audit-content.py` a partir daqui.
  * Fora do escopo deste validador: `references.json` (tem ticket próprio, TCK-0009) e a
    teoria `theory.<lang>.md` (coberta pela auditoria estrutural).
  * Este validador **não decide a natureza da `tolerance`** (absoluta ou relativa): exige
    apenas número finito ≥ 0, regra idêntica nas duas leituras. Fechar essa decisão de
    contrato é do `tech-lead`, e precisa acontecer antes da correção de resposta
    (tasks 5–8 da spec), onde ela passa a ter efeito observável.

Regras verificadas (o identificador entre colchetes aparece na mensagem de erro):

  Identidade do nó
    [META-ID-MISMATCH]           meta.json.id diferente do caminho do nó
    [NODE-ID-MISMATCH]           nodeId de exercises/assessments diferente do caminho
  Bilinguismo (campo a campo)
    [LOCALIZED-NOT-OBJECT]       campo localizado que não é objeto {pt-BR, en-US}
    [LOCALIZED-MISSING-LANG]     falta pt-BR ou en-US
    [LOCALIZED-NOT-STRING]       valor da chave de idioma não é texto
    [LOCALIZED-EMPTY]            texto vazio em um dos idiomas
    [LOCALIZED-UNKNOWN-LANG]     chave de idioma fora do contrato
  Item de escolha
    [MC-NO-CORRECT-OPTION]       nenhuma opção com "correct": true
    [MC-MULTIPLE-CORRECT-OPTIONS] mais de uma opção correta
    [CHOICE-NO-CORRECT-OPTION]   matching sem nenhuma correspondência correta
    [OPTIONS-MISSING]            sem 'options' utilizável (mínimo 2)
    [OPTION-NOT-OBJECT]          alternativa que não é objeto
    [OPTION-ID-MISSING]          alternativa sem 'id' (não dá para registrar a escolha)
    [OPTION-ID-DUPLICATE]        dois 'id' iguais no mesmo item
    [CORRECT-NOT-BOOLEAN]        'correct' preenchido com algo que não é true/false
    [OPTION-FEEDBACK-MISSING]    alternativa errada sem feedback diagnóstico
  Item de resposta
    [NUMERIC-ANSWER-MISSING]     numeric sem 'answer'
    [NUMERIC-ANSWER-NOT-NUMBER]  'answer' que não é número de máquina
    [NUMERIC-ANSWER-NOT-FINITE]  'answer' NaN/Infinity
    [NUMERIC-TOLERANCE-MISSING]  numeric sem 'tolerance' (0 é válido; ausente não)
    [NUMERIC-TOLERANCE-NOT-NUMBER] 'tolerance' que não é número
    [NUMERIC-TOLERANCE-NEGATIVE] 'tolerance' negativa
    [NUMERIC-TOLERANCE-NOT-FINITE] 'tolerance' NaN/Infinity
    [ANSWER-MISSING]             short-answer/ordering sem 'answer'
  Estrutura mínima do item
    [ITEM-NOT-OBJECT] [ITEM-ID-MISSING] [ITEM-ID-DUPLICATE] [ITEM-TYPE-MISSING]
    [ITEM-TYPE-UNKNOWN] [ITEM-FIELD-MISSING] [ITEMS-MISSING] [ITEMS-EMPTY]
    [HINTS-NOT-LIST]
  Leitura
    [JSON-INVALID] [JSON-DUPLICATE-KEY] [NODE-META-MISSING] [META-NOT-OBJECT]
    [META-FIELD-MISSING] [FILE-UNREADABLE]

Um alvo é sempre percorrido **recursivamente**: um nó pode ter subnós (`AGENTS.md` §3,
`TOPIC --> SUBTOPIC`), e validar o pai sem descer devolveria "contrato íntegro" com um
subnó quebrado logo abaixo.

Uso:
  python3 scripts/validate-content.py                      # acervo inteiro
  python3 scripts/validate-content.py high-school/algebra/quadratic-equations
  python3 scripts/validate-content.py --root DIR NODE...   # raiz alternativa (fixtures)
  python3 scripts/validate-content.py --json               # saída para pipeline

Códigos de saída: 0 = contrato íntegro · 1 = violação · 2 = erro de uso.
Os três códigos são preservados mesmo com a saída padrão ou a saída de erro quebrada
(`| head`, `>&-`, `> /dev/full`): o veredito é sobre o conteúdo, nunca sobre o terminal.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROOT = REPO_ROOT / "content"

LANGS = ("pt-BR", "en-US")

ITEM_TYPES = {
    "multiple-choice", "true-false", "numeric", "short-answer",
    "ordering", "matching", "step-by-step", "proof",
}
# Tipos que exigem exatamente uma alternativa correta (RF-18).
SINGLE_CORRECT_TYPES = {"multiple-choice", "true-false"}
# Tipos de escolha em geral: precisam de 'options' e de ao menos uma correta.
CHOICE_TYPES = SINGLE_CORRECT_TYPES | {"matching"}
# Tipos com resposta de máquina.
ANSWER_TYPES = {"numeric", "short-answer", "ordering"}

EXERCISE_FILES = ("exercises.json", "assessments.json")


# --------------------------------------------------------------------------- #
# Violação
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Violation:
    """Uma violação localizada: arquivo, item, regra e o que fazer."""

    file: str
    locator: str
    rule: str
    message: str

    def as_line(self) -> str:
        return f"{self.file}: {self.locator}: [{self.rule}] {self.message}"

    def as_dict(self) -> dict:
        return {
            "file": self.file,
            "locator": self.locator,
            "rule": self.rule,
            "message": self.message,
        }


class Collector:
    """Acumula violações — nunca interrompe na primeira (critério 1 do TCK-0014)."""

    def __init__(self) -> None:
        self.violations: list[Violation] = []

    def add(self, file: str, locator: str, rule: str, message: str) -> None:
        self.violations.append(Violation(file, locator, rule, message))


# --------------------------------------------------------------------------- #
# Auxiliares
# --------------------------------------------------------------------------- #


def _mute_stream(stream) -> None:
    """Aponta um fluxo para devnull quando o destino real morreu."""
    try:
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, stream.fileno())
    except Exception:  # noqa: BLE001 — silenciar é o próprio objetivo
        pass


def _write(stream, text: str, newline: bool = True) -> None:
    """Escreve sem deixar que um fluxo quebrado altere o veredito do contrato.

    Vale para stdout **e** stderr: `2>&1 | true` e `2> /dev/full` transformavam o
    `exit 2` de erro de uso em `120` (REJECT [006], B2).
    """
    if stream is None:  # `>&-` deixa o fluxo como None
        return
    try:
        stream.write(text + "\n" if newline else text)
        stream.flush()
    except (BrokenPipeError, OSError, ValueError):
        _mute_stream(stream)


def emit(text: str) -> None:
    _write(sys.stdout, text)


def emit_err(text: str) -> None:
    _write(sys.stderr, text)


def safe_flush() -> None:
    """Fecha as saídas sem deixar o flush de encerramento virar código 120."""
    for stream in (sys.stdout, sys.stderr):
        if stream is None:
            continue
        try:
            stream.flush()
        except (BrokenPipeError, OSError, ValueError):
            _mute_stream(stream)


def make_output_lossless() -> None:
    """Impede que um terminal ASCII apague a mensagem (S3 do REJECT [006]).

    Sem isto, `LC_ALL=POSIX PYTHONUTF8=0` fazia o validador sair 1 sem imprimir uma
    linha: `UnicodeEncodeError` é subclasse de `ValueError` e era engolido. Mensagem
    sem localização (ou sem mensagem alguma) é o critério 5 perdido.
    """
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:  # noqa: BLE001 — fluxo ausente ou sem reconfigure
            pass


def display_path(path: Path) -> str:
    """Caminho acionável: relativo ao repositório quando possível, absoluto fora dele."""
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path.resolve())


def type_name(value: object) -> str:
    return {
        dict: "objeto", list: "lista", str: "texto", bool: "booleano",
        int: "número", float: "número", type(None): "null",
    }.get(type(value), type(value).__name__)


def is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def load_json(path: Path, col: Collector) -> object | None:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    except OSError as exc:
        col.add(display_path(path), "arquivo", "FILE-UNREADABLE",
                f"não foi possível ler o arquivo: {exc.strerror or exc}")
        return None

    duplicated: list[str] = []

    def object_with_duplicate_check(pairs: list[tuple[str, object]]) -> dict:
        seen: set[str] = set()
        for key, _ in pairs:
            if key in seen:
                duplicated.append(key)
            seen.add(key)
        return dict(pairs)

    try:
        data = json.loads(raw, object_pairs_hook=object_with_duplicate_check)
    except json.JSONDecodeError as exc:
        col.add(display_path(path), f"linha {exc.lineno}, coluna {exc.colno}",
                "JSON-INVALID",
                f"JSON inválido ({exc.msg}) — o arquivo inteiro fica indisponível para a carga")
        return None

    for key in sorted(set(duplicated)):
        col.add(display_path(path), f"chave '{key}'", "JSON-DUPLICATE-KEY",
                f"a chave '{key}' aparece mais de uma vez no mesmo objeto — só o último valor "
                f"vale, e o valor descartado fica invisível na revisão; deixe uma só")

    return data


def check_localized(col: Collector, file: str, locator: str, field: str, value: object) -> None:
    """Paridade bilíngue de um campo localizado (RF-18, RNF-1: sem fallback)."""
    if not isinstance(value, dict):
        col.add(file, locator, "LOCALIZED-NOT-OBJECT",
                f"campo '{field}' deve ser um objeto localizado "
                f"{{\"pt-BR\": …, \"en-US\": …}} — encontrado {type_name(value)}")
        return

    present = list(value.keys())
    for lang in LANGS:
        if lang not in value:
            col.add(file, locator, "LOCALIZED-MISSING-LANG",
                    f"campo '{field}' sem a chave '{lang}' — paridade bilíngue é obrigatória "
                    f"e não há fallback (chaves presentes: {present or 'nenhuma'})")
        elif not isinstance(value[lang], str):
            col.add(file, locator, "LOCALIZED-NOT-STRING",
                    f"campo '{field}.{lang}' deve ser texto — encontrado {type_name(value[lang])}")
        elif not value[lang].strip():
            col.add(file, locator, "LOCALIZED-EMPTY",
                    f"campo '{field}.{lang}' está vazio — traduza ou marque o nó como 'draft'")

    for extra in present:
        if extra not in LANGS:
            col.add(file, locator, "LOCALIZED-UNKNOWN-LANG",
                    f"campo '{field}' tem a chave de idioma '{extra}', fora do contrato "
                    f"{list(LANGS)}")


# --------------------------------------------------------------------------- #
# meta.json
# --------------------------------------------------------------------------- #


def validate_meta(col: Collector, node: Path, node_id: str) -> dict:
    path = node / "meta.json"
    file = display_path(path)

    if not path.exists():
        col.add(display_path(node), "nó", "NODE-META-MISSING",
                "meta.json ausente — sem ele o nó não tem identidade nem idioma declarado")
        return {}

    meta = load_json(path, col)
    if meta is None:
        return {}
    if not isinstance(meta, dict):
        col.add(file, "raiz", "META-NOT-OBJECT",
                f"meta.json deve ser um objeto — encontrado {type_name(meta)}")
        return {}

    if "id" not in meta:
        col.add(file, "id", "META-FIELD-MISSING",
                f"meta.json sem o campo 'id' — deveria ser '{node_id}' (o caminho do nó "
                f"é a URL pública, RF-17)")
    elif meta.get("id") != node_id:
        col.add(file, "id", "META-ID-MISMATCH",
                f"meta.json.id é '{meta.get('id')}' mas o nó está em '{node_id}' — "
                f"o identificador canônico tem de ser o caminho da taxonomia (RF-17); "
                f"corrija o campo ou mova o nó")

    for field in ("title", "summary"):
        if field not in meta:
            col.add(file, field, "META-FIELD-MISSING",
                    f"meta.json sem o campo localizado '{field}'")
        else:
            check_localized(col, file, field, field, meta[field])

    return meta


# --------------------------------------------------------------------------- #
# exercises.json / assessments.json
# --------------------------------------------------------------------------- #


def validate_choice_item(col: Collector, file: str, locator: str, item: dict, itype: str) -> None:
    options = item.get("options")
    if not isinstance(options, list) or len(options) < 2:
        col.add(file, locator, "OPTIONS-MISSING",
                f"item do tipo '{itype}' precisa de 'options' com pelo menos 2 alternativas — "
                f"encontrado {type_name(options)}"
                + (f" com {len(options)} item(ns)" if isinstance(options, list) else ""))
        return

    seen_ids: set[str] = set()
    correct_ids: list[str] = []

    for oi, opt in enumerate(options):
        olocator = f"{locator}.options[{oi}]"
        if not isinstance(opt, dict):
            col.add(file, olocator, "OPTION-NOT-OBJECT",
                    f"alternativa deve ser objeto — encontrado {type_name(opt)}")
            continue

        opt_id = opt.get("id")
        if not isinstance(opt_id, str) or not opt_id.strip():
            col.add(file, olocator, "OPTION-ID-MISSING",
                    "alternativa sem 'id' de texto — a escolha do aluno não teria como ser "
                    "registrada nem o feedback localizado")
            opt_id = f"#{oi}"
        elif opt_id in seen_ids:
            col.add(file, olocator, "OPTION-ID-DUPLICATE",
                    f"'id' de alternativa repetido: '{opt_id}'")
        else:
            seen_ids.add(opt_id)

        olocator = f"{locator}.options[{oi}] (id={opt_id})"

        correct = opt.get("correct", False)
        if not isinstance(correct, bool):
            col.add(file, olocator, "CORRECT-NOT-BOOLEAN",
                    f"'correct' deve ser true ou false — encontrado {type_name(correct)} "
                    f"({correct!r}); valor ambíguo faz o gabarito depender de conversão implícita")
        elif correct:
            correct_ids.append(opt_id)

        check_localized(col, file, olocator, "text", opt.get("text"))

        if correct is not True:
            if "feedback" not in opt:
                col.add(file, olocator, "OPTION-FEEDBACK-MISSING",
                        "alternativa errada sem 'feedback' diagnóstico — o aluno precisa saber "
                        "qual equívoco leva a ela (docs/content/exercise-schema.md, regra 1)")
            else:
                check_localized(col, file, olocator, "feedback", opt["feedback"])
        elif "feedback" in opt:
            check_localized(col, file, olocator, "feedback", opt["feedback"])

    listed = ", ".join(correct_ids) if correct_ids else "nenhuma"
    if itype in SINGLE_CORRECT_TYPES:
        if not correct_ids:
            col.add(file, locator, "MC-NO-CORRECT-OPTION",
                    f"item '{itype}' sem nenhuma opção com \"correct\": true — não há gabarito, "
                    f"o item não pode ser apresentado ao aluno (RF-18); marque exatamente uma "
                    f"das {len(options)} alternativas")
        elif len(correct_ids) > 1:
            col.add(file, locator, "MC-MULTIPLE-CORRECT-OPTIONS",
                    f"item '{itype}' com {len(correct_ids)} opções corretas ({listed}) — "
                    f"esperada exatamente 1 (RF-18); múltipla resposta exige tipo próprio "
                    f"declarado no enunciado")
    elif not correct_ids:
        col.add(file, locator, "CHOICE-NO-CORRECT-OPTION",
                f"item '{itype}' sem nenhuma correspondência marcada como correta — "
                f"sem gabarito não há como corrigir a resposta")


def validate_answer_item(col: Collector, file: str, locator: str, item: dict, itype: str) -> None:
    if itype != "numeric":
        if "answer" not in item or item["answer"] in (None, "", [], {}):
            col.add(file, locator, "ANSWER-MISSING",
                    f"item do tipo '{itype}' sem 'answer' utilizável — o gabarito de máquina "
                    f"é obrigatório para corrigir a resposta")
        return

    if "answer" not in item:
        col.add(file, locator, "NUMERIC-ANSWER-MISSING",
                "item 'numeric' sem 'answer' — sem gabarito numérico não há correção (RF-18)")
    elif not is_number(item["answer"]):
        extra = (" — use número de máquina com ponto decimal (3.5), não texto"
                 if isinstance(item["answer"], str) else "")
        col.add(file, locator, "NUMERIC-ANSWER-NOT-NUMBER",
                f"'answer' de item 'numeric' deve ser número — encontrado "
                f"{type_name(item['answer'])} ({item['answer']!r}){extra}")
    elif not math.isfinite(float(item["answer"])):
        col.add(file, locator, "NUMERIC-ANSWER-NOT-FINITE",
                f"'answer' de item 'numeric' deve ser finito — encontrado {item['answer']!r}")

    if "tolerance" not in item:
        col.add(file, locator, "NUMERIC-TOLERANCE-MISSING",
                "item 'numeric' sem 'tolerance' — declare a margem aceita; "
                "use \"tolerance\": 0 para exigir valor exato (ausente é ambíguo, 0 é explícito)")
        return

    tol = item["tolerance"]
    if not is_number(tol):
        col.add(file, locator, "NUMERIC-TOLERANCE-NOT-NUMBER",
                f"'tolerance' deve ser número — encontrado {type_name(tol)} ({tol!r})")
    elif not math.isfinite(float(tol)):
        col.add(file, locator, "NUMERIC-TOLERANCE-NOT-FINITE",
                f"'tolerance' deve ser finita — encontrado {tol!r}")
    elif tol < 0:
        col.add(file, locator, "NUMERIC-TOLERANCE-NEGATIVE",
                f"'tolerance' negativa ({tol}) — nenhuma resposta seria aceita (RF-18); "
                f"use 0 para exigir valor exato")


def validate_item(col: Collector, file: str, index: int, item: object,
                  seen_ids: set[str] | None = None) -> None:
    locator = f"items[{index}]"
    seen_ids = seen_ids if seen_ids is not None else set()

    if not isinstance(item, dict):
        col.add(file, locator, "ITEM-NOT-OBJECT",
                f"item deve ser objeto — encontrado {type_name(item)}")
        return

    item_id = item.get("id")
    if isinstance(item_id, str) and item_id.strip():
        locator = f"items[{index}] (id={item_id})"
        if item_id in seen_ids:
            col.add(file, locator, "ITEM-ID-DUPLICATE",
                    f"'id' de item repetido: '{item_id}' — dois itens com o mesmo endereço "
                    f"tornam resultado, dica e link ambíguos")
        seen_ids.add(item_id)
    else:
        col.add(file, locator, "ITEM-ID-MISSING",
                "item sem 'id' de texto — sem ele nenhuma violação, nenhum resultado e "
                "nenhum link para o item têm endereço estável")

    itype = item.get("type")
    if itype is None:
        col.add(file, locator, "ITEM-TYPE-MISSING",
                f"item sem 'type' — a carga não sabe como corrigir a resposta "
                f"(tipos válidos: {', '.join(sorted(ITEM_TYPES))})")
        itype = ""
    elif itype not in ITEM_TYPES:
        col.add(file, locator, "ITEM-TYPE-UNKNOWN",
                f"type '{itype}' desconhecido — tipos válidos: {', '.join(sorted(ITEM_TYPES))} "
                f"(docs/content/exercise-schema.md)")

    for field in ("stem", "solution"):
        if field not in item:
            col.add(file, locator, "ITEM-FIELD-MISSING",
                    f"item sem o campo localizado obrigatório '{field}'")
        else:
            check_localized(col, file, locator, field, item[field])

    hints = item.get("hints")
    if hints is not None:
        if not isinstance(hints, list):
            col.add(file, locator, "HINTS-NOT-LIST",
                    f"'hints' deve ser lista de objetos localizados — encontrado {type_name(hints)}")
        else:
            for hi, hint in enumerate(hints):
                check_localized(col, file, f"{locator}.hints[{hi}]", f"hints[{hi}]", hint)

    if itype in CHOICE_TYPES:
        validate_choice_item(col, file, locator, item, itype)
    elif itype in ANSWER_TYPES:
        validate_answer_item(col, file, locator, item, itype)


def validate_exercise_file(col: Collector, node: Path, node_id: str, filename: str) -> None:
    path = node / filename
    if not path.exists():
        return
    file = display_path(path)

    data = load_json(path, col)
    if data is None:
        return
    if not isinstance(data, dict):
        col.add(file, "raiz", "ITEMS-MISSING",
                f"{filename} deve ser um objeto com 'nodeId' e 'items' — "
                f"encontrado {type_name(data)}")
        return

    if "nodeId" not in data:
        col.add(file, "nodeId", "NODE-ID-MISMATCH",
                f"{filename} sem 'nodeId' — deveria ser '{node_id}' (o arquivo precisa "
                f"declarar a que nó pertence)")
    elif data.get("nodeId") != node_id:
        col.add(file, "nodeId", "NODE-ID-MISMATCH",
                f"nodeId é '{data.get('nodeId')}' mas o arquivo está no nó '{node_id}' — "
                f"exercícios seriam servidos sob o nó errado (RF-18); corrija o campo "
                f"ou mova o arquivo")

    items = data.get("items")
    if not isinstance(items, list):
        col.add(file, "items", "ITEMS-MISSING",
                f"{filename} sem a lista 'items' — encontrado {type_name(items)}")
        return

    if not items:
        col.add(file, "items", "ITEMS-EMPTY",
                f"{filename} existe mas não tem nenhum item — o nó promete prática e não "
                f"entrega nenhuma; remova o arquivo ou preencha 'items'")
        return

    seen_ids: set[str] = set()
    for index, item in enumerate(items):
        validate_item(col, file, index, item, seen_ids)


# --------------------------------------------------------------------------- #
# Nó e acervo
# --------------------------------------------------------------------------- #


def validate_node(node: Path, root: Path, col: Collector | None = None) -> list[Violation]:
    """Valida um nó isolado. `root` é a raiz do acervo (define o id canônico)."""
    col = col if col is not None else Collector()
    node_id = node.resolve().relative_to(root.resolve()).as_posix()

    validate_meta(col, node, node_id)
    for filename in EXERCISE_FILES:
        validate_exercise_file(col, node, node_id, filename)

    return col.violations


def find_nodes(scope: Path) -> list[Path]:
    """Nó = diretório com meta.json OU com arquivo de exercícios. Sempre recursivo.

    Duas condições, uma regra: nada some da varredura.

    * Reconhecer o nó por mais de um marcador impede que a falta de `meta.json` apague
      um diretório que tem exercícios.
    * A varredura **nunca para no alvo**. A versão anterior retornava `[scope]` quando o
      próprio alvo era um nó, e um subnó quebrado (`TOPIC --> SUBTOPIC`, `AGENTS.md` §3)
      ficava invisível: validar o tópico devolvia "contrato íntegro" enquanto a raiz
      acusava violações — portão que fica cego conforme o acervo cresce (REJECT [006], B1).
    """
    markers = ("meta.json", *EXERCISE_FILES)
    found = {p.parent for marker in markers for p in scope.rglob(marker)}
    if any((scope / marker).exists() for marker in markers):
        found.add(scope)
    return sorted(found)


def resolve_root(target: Path, explicit: Path | None) -> Path | None:
    """Raiz do acervo: --root, ou o ancestral chamado 'content', ou o padrão do repo."""
    if explicit is not None:
        return explicit.resolve()
    target = target.resolve()
    for candidate in (target, *target.parents):
        if candidate.name == "content":
            return candidate
    if DEFAULT_ROOT.exists() and DEFAULT_ROOT.resolve() in (target, *target.parents):
        return DEFAULT_ROOT.resolve()
    return None


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


class SafeArgumentParser(argparse.ArgumentParser):
    """argparse cujo texto de uso/erro não derruba o código de saída.

    `--xx 2>&1 | true` fazia o `exit 2` virar `120`, porque a mensagem do próprio
    argparse ia por `print` direto (REJECT [006], B2). Todo texto do argparse passa
    por `_print_message`; roteá-lo para `_write` resolve na origem.
    """

    def _print_message(self, message: str, file=None) -> None:  # noqa: D102
        if message:
            _write(file if file is not None else sys.stderr, message, newline=False)


def build_parser() -> argparse.ArgumentParser:
    parser = SafeArgumentParser(
        prog="validate-content.py",
        description="Valida o contrato de carga de content/ (RF-18). "
                    "Lista TODAS as violações e sai com 1 se houver alguma.",
    )
    parser.add_argument("targets", nargs="*", metavar="CAMINHO",
                        help="nó, subárvore ou acervo (padrão: content/ do repositório)")
    parser.add_argument("--root", type=Path, default=None,
                        help="raiz do acervo, que define o id canônico do nó "
                             "(padrão: content/ ou o ancestral chamado 'content')")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="saída JSON para consumo em pipeline")
    parser.add_argument("--quiet", action="store_true",
                        help="não imprime nada; só o código de saída importa")
    return parser


def main(argv: list[str] | None = None) -> int:
    make_output_lossless()
    args = build_parser().parse_args(argv)

    if args.root is not None and (args.root / "content").is_dir():
        # S5: com --root no pai de content/, o id vira 'content/<stage>/…' e um nó íntegro
        # sai com META-ID-MISMATCH — falso positivo confiante, pior que erro barulhento.
        emit_err(f"ERRO DE USO: a raiz informada em --root ('{args.root}') contém um "
                 f"diretório 'content/' — a raiz do acervo é ele, não o pai; use "
                 f"--root {args.root / 'content'}")
        return 2

    targets: list[Path] = []
    for raw in args.targets or []:
        candidate = Path(raw)
        if not candidate.exists():
            candidate = (args.root or DEFAULT_ROOT) / raw
        if not candidate.exists():
            emit_err(f"ERRO DE USO: caminho não encontrado: {raw}")
            return 2
        if candidate.is_file():  # apontar para meta.json/exercises.json vale pelo nó
            candidate = candidate.parent
        targets.append(candidate)

    if not targets:
        fallback = args.root or DEFAULT_ROOT
        if not fallback.exists():
            emit_err(f"ERRO DE USO: {display_path(fallback)} não existe e nenhum caminho "
                     f"foi informado")
            return 2
        targets = [fallback]

    col = Collector()
    nodes: list[tuple[Path, Path]] = []
    for target in targets:
        root = resolve_root(target, args.root)
        if root is None:
            emit_err(f"ERRO DE USO: não foi possível deduzir a raiz do acervo para "
                     f"'{target}' — informe --root")
            return 2
        for node in find_nodes(target):
            try:
                node.resolve().relative_to(root)
            except ValueError:
                emit_err(f"ERRO DE USO: o nó '{node}' está fora da raiz '{root}'")
                return 2
            nodes.append((node, root))

    if not nodes:
        alvo = ", ".join(str(t) for t in targets)
        emit_err(f"ERRO DE USO: nenhum nó de conteúdo encontrado em: {alvo} — "
                 f"um caminho errado não pode passar por 'validado com sucesso'")
        return 2

    seen: set[Path] = set()
    for node, root in nodes:
        if node.resolve() in seen:
            continue
        seen.add(node.resolve())
        validate_node(node, root, col)

    violations = col.violations

    if args.quiet:
        return 1 if violations else 0

    if args.as_json:
        emit(json.dumps({
            "nodes": len(seen),
            "violations": len(violations),
            "items": [v.as_dict() for v in violations],
        }, ensure_ascii=False, indent=2))
        return 1 if violations else 0

    for violation in violations:
        emit(violation.as_line())

    if violations:
        emit(f"\nCONTRATO VIOLADO: {len(violations)} violação(ões) em {len(seen)} nó(s). "
             f"Conteúdo com violação não pode ser publicado nem apresentado ao aluno.")
    else:
        emit(f"Contrato íntegro: {len(seen)} nó(s) validado(s), 0 violações.")

    return 1 if violations else 0


if __name__ == "__main__":
    # Saída quebrada (`| head`, `>&-`, `> /dev/full`), em stdout OU em stderr, não pode
    # virar o código de saída: o veredito sobre o conteúdo é o que o pipeline lê. Sem o
    # `safe_flush`, o flush de encerramento do Python trocava 0, 1 e 2 por 120.
    try:
        status = main()
    except SystemExit as exc:  # argparse: --help (0) e uso inválido (2)
        status = exc.code if isinstance(exc.code, int) else 2
    safe_flush()
    raise SystemExit(status)
