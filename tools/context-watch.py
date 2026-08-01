#!/usr/bin/env python3
"""context-watch.py — mede o consumo de contexto da sessão do Claude Code.

Lê o transcript da sessão (`~/.claude/projects/<slug>/<session>.jsonl`) e soma
`input_tokens + cache_creation_input_tokens + cache_read_input_tokens` da última
mensagem `assistant` não-sidechain: esse é o contexto vivo enviado ao modelo.

PRIVACIDADE (requisito de segurança, não de estilo): o transcript contém a conversa
inteira. Este script lê apenas contagens e metadados e **nunca** imprime conteúdo de
mensagem, nome de arquivo lido, prompt ou resultado de ferramenta. Nada sai da máquina:
não há nenhuma requisição de rede.

Exit codes (critério 2 de TCK-0012):
    0   verde     — uso < 60%
    10  atencao   — uso < 75%
    20  preparar  — uso < 85%   (escrever o snapshot de handoff)
    30  critico   — uso >= 85%  (handoff agora; compactação é lossy)
    40  sem-telemetria — a ferramenta não expõe telemetria de contexto, ou o
        transcript não pôde ser lido. Nunca é uma estimativa inventada.

No modo `--hook` o exit code é sempre 0 (um hook não pode atrapalhar a sessão).

Zero dependência: apenas a biblioteca padrão do Python 3.
"""

from __future__ import annotations

import argparse
import glob
import datetime
import json
import os
import re
import sys
import time

# --------------------------------------------------------------------------------------
# Configuração
# --------------------------------------------------------------------------------------

#: (limite superior exclusivo da fração, nome da zona, exit code)
DEFAULT_THRESHOLDS = (0.60, 0.75, 0.85)
ZONE_NAMES = ("verde", "atencao", "preparar", "critico")
ZONE_CODES = (0, 10, 20, 30)
NO_TELEMETRY_CODE = 40

#: Janelas padrão por modelo — último recurso do critério 3, nunca fonte confiável.
#: O transcript grava `claude-opus-5` mesmo quando a sessão roda a variante de 1M
#: (`claude-opus-5[1m]`): o id é **ambíguo**. Para id ambíguo presumimos a janela
#: CONSERVADORA (a menor plausível): errar avisando cedo é recuperável; errar calando —
#: mostrar "20% VERDE" com o contexto cheio — é o modo de falha que este tool existe para
#: impedir. Sempre que a janela vem daqui, `janela_confiavel` sai `false` e o hook diz isso
#: uma vez por sessão.
AMBIGUOUS_MODELS = {"claude-opus-5", "claude-sonnet-5"}
CONSERVATIVE_WINDOW = 200_000

#: Degraus plausíveis de janela, em ordem. Só são usados quando a **medição refuta** a
#: presunção (`usado > janela presumida`): aí a presunção está provada errada e insistir
#: nela imprime um número autorrefutável. Refutação nunca se aplica a janela configurada
#: pelo usuário — se ele disse 200k e o uso passou disso, isso é um estouro real.
WINDOW_TIERS = (200_000, 1_000_000)
DEFAULT_WINDOWS = {
    "claude-haiku-5": 200_000,
    "claude-opus-4-1": 200_000,
    "claude-sonnet-4-5": 200_000,
    "claude-haiku-4-5": 200_000,
    "claude-3-5-haiku": 200_000,
}
FALLBACK_WINDOW = 200_000

#: Whitelist dos únicos dois campos de texto do transcript que chegam ao stdout.
#: Qualquer coisa fora do formato vira `None` — nenhuma string arbitrária do arquivo
#: atravessa a saída (defesa em profundidade do requisito de privacidade).
MODEL_RE = re.compile(r"^[A-Za-z0-9._\[\]-]{1,64}$")
TIMESTAMP_RE = re.compile(r"^[0-9T:.+\-]{10,32}Z?$")

BAR_WIDTH = 30

ACTION_BY_ZONE = {
    "verde": "seguir normalmente.",
    "atencao": "evitar releitura de arquivos grandes; preferir trechos.",
    "preparar": "gerar o snapshot agora: bash tools/agent-handoff.sh snapshot --force",
    "critico": (
        "handoff agora — a compactação automática é lossy: "
        "bash tools/agent-handoff.sh snapshot --force && bash tools/agent-handoff.sh validate"
    ),
}


class TelemetryError(Exception):
    """Falha esperada de leitura: vira exit 40 com mensagem, nunca stack trace."""


# --------------------------------------------------------------------------------------
# Localização do transcript
# --------------------------------------------------------------------------------------


def project_slugs(cwd: str) -> list[str]:
    """Candidatos de slug do diretório de projeto usado pelo Claude Code."""
    candidates = [cwd.replace("/", "-"), re.sub(r"[^A-Za-z0-9]", "-", cwd)]
    seen: list[str] = []
    for slug in candidates:
        if slug and slug not in seen:
            seen.append(slug)
    return seen


def projects_root() -> str:
    return os.path.expanduser(os.environ.get("CLAUDE_PROJECTS_DIR", "~/.claude/projects"))


def sanitize_model(value) -> str | None:
    return value if isinstance(value, str) and MODEL_RE.match(value) else None


def sanitize_timestamp(value) -> str | None:
    if not isinstance(value, str) or not TIMESTAMP_RE.match(value):
        return None
    try:
        datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return value


def find_transcript(cwd: str, session_id: str | None = None) -> tuple[str, str, int]:
    """Resolve o transcript da sessão. Retorna (caminho, origem, candidatos)."""
    root = projects_root()
    dirs = [os.path.join(root, slug) for slug in project_slugs(cwd)]
    existing = [d for d in dirs if os.path.isdir(d)]
    if not existing:
        raise TelemetryError(
            "nenhum diretório de projeto do Claude Code para este cwd "
            f"(procurado em {root}/)"
        )
    files: list[str] = []
    for d in existing:
        files.extend(glob.glob(os.path.join(d, "*.jsonl")))
    if session_id:
        for d in existing:
            path = os.path.join(d, f"{session_id}.jsonl")
            if os.path.isfile(path):
                return path, "session-id", len(files)
    if not files:
        raise TelemetryError("nenhum transcript (.jsonl) no diretório de projeto")
    return max(files, key=os.path.getmtime), "mtime", len(files)


def resolve_transcript(args, payload: dict) -> tuple[str, str, int]:
    """Ordem: --session → payload do hook → CLAUDE_SESSION_ID → mais recente por mtime."""
    if args.session:
        if os.path.sep in args.session or args.session.endswith(".jsonl"):
            path = os.path.expanduser(args.session)
            if not os.path.isfile(path):
                raise TelemetryError(f"transcript não encontrado: {path}")
            return path, "argumento", 1
        return find_transcript(args.cwd, args.session)
    hook_path = payload.get("transcript_path")
    if hook_path:
        hook_path = os.path.expanduser(str(hook_path))
        if os.path.isfile(hook_path):
            return hook_path, "hook", 1
    session_id = payload.get("session_id") or os.environ.get("CLAUDE_SESSION_ID")
    return find_transcript(args.cwd, str(session_id) if session_id else None)


# --------------------------------------------------------------------------------------
# Leitura do uso
# --------------------------------------------------------------------------------------


def read_usage(path: str) -> dict:
    """Última mensagem `assistant` não-sidechain com `usage`.

    Linhas malformadas são ignoradas e contadas (o formato do transcript é interno do
    Claude Code e pode mudar sem aviso). Retorna apenas números e metadados.
    """
    last: dict | None = None
    malformed = 0
    total = 0
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if not line.strip():
                    continue
                total += 1
                try:
                    entry = json.loads(line)
                except (json.JSONDecodeError, ValueError):
                    malformed += 1
                    continue
                if not isinstance(entry, dict):
                    malformed += 1
                    continue
                if entry.get("type") != "assistant" or entry.get("isSidechain"):
                    continue
                message = entry.get("message")
                if not isinstance(message, dict):
                    continue
                usage = message.get("usage")
                if not isinstance(usage, dict):
                    continue
                used = 0
                for key in (
                    "input_tokens",
                    "cache_creation_input_tokens",
                    "cache_read_input_tokens",
                ):
                    value = usage.get(key, 0)
                    if isinstance(value, bool) or not isinstance(value, (int, float)):
                        continue
                    used += int(value)
                last = {
                    "used": used,
                    "model": sanitize_model(message.get("model")),
                    "timestamp": sanitize_timestamp(entry.get("timestamp")),
                }
    except OSError as exc:
        raise TelemetryError(f"transcript ilegível: {exc.strerror}") from exc
    if last is None:
        if total == 0:
            raise TelemetryError("transcript vazio — nenhuma mensagem registrada ainda")
        raise TelemetryError(
            f"nenhuma mensagem assistant com usage no transcript "
            f"({malformed} linha(s) ilegível(is) de {total})"
        )
    last["malformed_lines"] = malformed
    return last


# --------------------------------------------------------------------------------------
# Janela e zona
# --------------------------------------------------------------------------------------


def read_setting(path: str, key: str):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError, ValueError):
        return None
    return data.get(key) if isinstance(data, dict) else None


def positive_int(value) -> int | None:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return None
    return number if number > 0 else None


def presume_window(model: str | None) -> tuple[int, str]:
    """Último elo do critério 3: palpite a partir do id do modelo."""
    key = (model or "").strip()
    if "[1m]" in key:
        return 1_000_000, f"modelo:{key}"
    base = key.split("[")[0]
    if base in AMBIGUOUS_MODELS:
        # O id não distingue a variante de 200k da de 1M: presumir a MENOR.
        return CONSERVATIVE_WINDOW, f"modelo-ambiguo:{base}"
    if base in DEFAULT_WINDOWS:
        return DEFAULT_WINDOWS[base], f"modelo:{base}"
    return FALLBACK_WINDOW, "padrao"


def resolve_window(model: str | None, cwd: str, used: int) -> tuple[int, str, bool]:
    """Retorna (janela, origem, confiavel). Ordem do critério 3.

    `used` entra porque a medição é **prova**: `usado > janela` é impossível numa janela
    real (a sessão já teria compactado). Quando isso acontece com uma janela apenas
    presumida, a presunção está refutada — abandoná-la é obrigatório, senão o script
    imprime um número que ele mesmo desmente.
    """
    env = positive_int(os.environ.get("CONTEXT_WINDOW"))
    if env:
        return env, "env:CONTEXT_WINDOW", True
    for path in (
        os.path.join(cwd, ".claude", "settings.local.json"),
        os.path.join(cwd, ".claude", "settings.json"),
        os.path.expanduser("~/.claude/settings.json"),
    ):
        value = positive_int(read_setting(path, "autoCompactWindow"))
        if value:
            where = "projeto" if path.startswith(cwd) else "usuario"
            return value, f"settings:{where}:autoCompactWindow", True

    window, origin = presume_window(model)
    if used <= window:
        return window, origin, False
    for tier in WINDOW_TIERS:
        if tier > used:
            # Sobe UM degrau, e só porque a medida obrigou. Continua não confiável, e o
            # hook é obrigado a dizer isso (window_hook_message).
            return tier, f"refutado:{origin}", False
    raise TelemetryError(
        f"medição incompatível com qualquer janela conhecida: {used:,} tokens vivos "
        f"excedem o maior valor plausível ({WINDOW_TIERS[-1]:,}). Sem janela verificável não "
        "há percentual honesto — defina CONTEXT_WINDOW ou autoCompactWindow "
        "(.claude/settings.local.json)"
    )


def thresholds() -> tuple[float, float, float]:
    raw = os.environ.get("CONTEXT_WATCH_THRESHOLDS")
    if not raw:
        return DEFAULT_THRESHOLDS
    try:
        parts = tuple(float(p) for p in raw.split(","))
    except ValueError:
        return DEFAULT_THRESHOLDS
    if len(parts) != 3 or not 0 < parts[0] < parts[1] < parts[2] <= 1:
        return DEFAULT_THRESHOLDS
    return parts  # type: ignore[return-value]


def zone_for(frac: float) -> tuple[str, int, int]:
    """Retorna (nome, exit code, índice). Sem `next()` sem default: frac >= 1 é crítico."""
    limits = thresholds()
    index = len(ZONE_NAMES) - 1
    for i, limit in enumerate(limits):
        if frac < limit:
            index = i
            break
    return ZONE_NAMES[index], ZONE_CODES[index], index


# --------------------------------------------------------------------------------------
# Estado da última zona (para o hook avisar só quando a zona sobe)
# --------------------------------------------------------------------------------------


def state_path(session_key: str) -> str:
    """Fora do repositório — o working tree não pode ser sujo pelo hook."""
    base = os.environ.get("XDG_STATE_HOME") or os.path.expanduser("~/.local/state")
    directory = os.path.join(base, "mathematics-studies")
    safe = re.sub(r"[^A-Za-z0-9_.-]", "-", session_key)[:120] or "sessao"
    return os.path.join(directory, f"context-zone-{safe}.json")


def read_state(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def last_zone(state: dict) -> int:
    value = state.get("zone_index")
    return value if isinstance(value, int) and not isinstance(value, bool) else -1


def write_state(path: str, index: int, window_warned: bool, result: dict) -> None:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = f"{path}.tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(
                {
                    "zone_index": index,
                    "window_warned": bool(window_warned),
                    "window": result["janela"],
                    "window_origin": result["janela_origem"],
                    "updated_at": int(time.time()),
                },
                fh,
            )
        os.replace(tmp, path)
    except OSError:
        pass  # estado é otimização, não requisito: falhar aqui não pode quebrar o hook


def window_changed(state: dict, result: dict) -> bool:
    """A régua mudou? Então a zona anterior não vale como referência.

    Sem isso, uma zona alta registrada sob janela errada **trava** o mecanismo: `rose`
    exige índice maior que o anterior e nada é maior que `critico`. Um alarme que satura
    no topo deixa de ser alarme.
    """
    if "window" not in state:
        return False
    return state.get("window") != result["janela"] or state.get("window_origin") != result[
        "janela_origem"
    ]


# --------------------------------------------------------------------------------------
# Medição e saída
# --------------------------------------------------------------------------------------


def measure(args, payload: dict) -> dict:
    path, path_origin, candidates = resolve_transcript(args, payload)
    usage = read_usage(path)
    window, window_origin, trustworthy = resolve_window(
        usage["model"], args.cwd, usage["used"]
    )
    frac = usage["used"] / window
    zone, code, index = zone_for(frac)
    return {
        "zona": zone,
        "usado": usage["used"],
        "janela": window,
        "restante": max(0, window - usage["used"]),
        "percentual": round(frac * 100, 1),
        "modelo": usage["model"],
        "medido_em": usage["timestamp"],
        "janela_origem": window_origin,
        "janela_confiavel": trustworthy,
        "transcript": os.path.basename(path),
        "transcript_origem": path_origin,
        "transcript_candidatos": candidates,
        "linhas_ilegiveis": usage["malformed_lines"],
        "exit_code": code,
        "zona_indice": index,
    }


def render_text(result: dict) -> str:
    frac = result["percentual"] / 100
    filled = max(0, min(BAR_WIDTH, int(frac * BAR_WIDTH)))
    bar = "#" * filled + "." * (BAR_WIDTH - filled)
    model = result["modelo"] or "modelo desconhecido"
    line = (
        f"[{result['zona'].upper()}] [{bar}] {result['percentual']:.1f}%  "
        f"({result['usado']:,} / {result['janela']:,} tokens · {model})"
    )
    line += f"\n  ação: {ACTION_BY_ZONE[result['zona']]}"
    if not result["janela_confiavel"]:
        line += "\n  " + window_caveat(result)
    if result["transcript_origem"] == "mtime" and result["transcript_candidatos"] > 1:
        line += (
            f"\n  aviso: {result['transcript_candidatos']} sessões neste projeto; medida a mais "
            "recente por mtime. Use --session <id> para escolher."
        )
    if result["linhas_ilegiveis"]:
        line += f"\n  aviso: {result['linhas_ilegiveis']} linha(s) ilegível(is) ignorada(s)."
    return line


def window_caveat(result: dict) -> str:
    """Texto único da incerteza — usado no terminal E no hook (B1: a incerteza tem de
    chegar ao caminho automático, não só a quem roda o comando à mão)."""
    origem = result["janela_origem"]
    fix = (
        "Para medir de verdade, declare a janela desta máquina em "
        ".claude/settings.local.json (gitignored): {\"autoCompactWindow\": <tokens>} — vale "
        "para o terminal, para o hook e para o snapshot. CONTEXT_WINDOW no shell **não** "
        "alcança o hook, que é lançado pelo Claude Code."
    )
    if origem.startswith("refutado:"):
        return (
            f"JANELA PRESUMIDA POR REFUTAÇÃO {result['janela']:,} tokens (origem {origem}): a "
            f"presunção anterior foi desmentida pela própria medição ({result['usado']:,} "
            "tokens vivos não cabem nela), então subi um degrau plausível. O percentual é um "
            f"limite superior grosseiro. {fix}"
        )
    if origem.startswith("modelo-ambiguo"):
        motivo = "o transcript não distingue a variante do modelo (200k × 1M)"
    elif origem == "padrao":
        motivo = "o modelo desta sessão não está mapeado"
    else:
        motivo = "a janela veio do id do modelo, não de configuração"
    return (
        f"JANELA PRESUMIDA {result['janela']:,} tokens (origem {origem}): {motivo}, então a "
        f"presunção é a mais conservadora e o percentual pode estar errado nos dois "
        f"sentidos. {fix}"
    )


def hook_message(result: dict) -> str:
    message = (
        f"[context-watch] contexto em {result['percentual']:.1f}% "
        f"({result['usado']:,}/{result['janela']:,}) — zona {result['zona'].upper()}. "
        f"{ACTION_BY_ZONE[result['zona']]}"
    )
    if not result["janela_confiavel"]:
        message += " " + window_caveat(result)
    return message


def window_hook_message(result: dict) -> str:
    """Aviso único por sessão quando a janela é presumida e a zona não subiu."""
    return (
        f"[context-watch] {window_caveat(result)} Medição atual sob essa presunção: "
        f"{result['percentual']:.1f}% (zona {result['zona'].upper()}). Aviso único por sessão."
    )


def emit_hook(message: str | None) -> int:
    """Hook nunca bloqueia: exit 0 sempre. Silêncio quando não há nada a dizer."""
    if message:
        safe_print(json.dumps({"systemMessage": message}, ensure_ascii=False))
    return 0


def _discard_stream(stream) -> None:
    """Redireciona um fd quebrado para /dev/null: sem isso o Python tenta dar flush no
    shutdown, imprime `Exception ignored` e sai com 120 — inaceitável num hook."""
    try:
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, stream.fileno())
        os.close(devnull)
    except (OSError, ValueError, AttributeError):
        pass


#: Toda falha possível de escrita/flush. `AttributeError` cobre o caso em que o fd já vem
#: fechado do shell (`>&-`): aí `sys.stdout` é `None`, não um arquivo quebrado.
WRITE_ERRORS = (BrokenPipeError, OSError, ValueError, AttributeError, TypeError)


def safe_write(stream, text: str) -> bool:
    """Escreve e dá flush **dentro** do try. `| head`, `> /dev/full`, pipe fechado e fd
    fechado não podem virar exit code: o contrato do script é a zona, não o sucesso da
    escrita."""
    if stream is None:
        return False
    try:
        stream.write(text + "\n")
        stream.flush()
        return True
    except WRITE_ERRORS:
        _discard_stream(stream)
        return False


def safe_print(text: str) -> bool:
    return safe_write(sys.stdout, text)


def safe_eprint(text: str) -> bool:
    return safe_write(sys.stderr, text)


def flush_stdio() -> None:
    """Último flush antes do exit, para o interpretador não falhar no shutdown.
    Não pode levantar nada: é chamada depois do `except` que garante o exit code."""
    for stream in (sys.stdout, sys.stderr):
        if stream is None:
            continue
        try:
            stream.flush()
        except WRITE_ERRORS:
            _discard_stream(stream)


def read_stdin_payload() -> dict:
    if sys.stdin is None or sys.stdin.isatty():
        return {}
    try:
        raw = sys.stdin.read()
    except (OSError, ValueError):
        return {}
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="context-watch.py",
        description="Mede o consumo de contexto da sessão do Claude Code.",
        epilog="Exit codes: 0 verde · 10 atenção · 20 preparar · 30 crítico · 40 sem telemetria.",
    )
    parser.add_argument("--json", action="store_true", help="objeto JSON de uma linha")
    parser.add_argument("--quiet", action="store_true", help="não imprime nada; só exit code")
    parser.add_argument(
        "--hook",
        action="store_true",
        help="modo hook: lê o payload no stdin, avisa só quando a zona sobe, exit 0 sempre",
    )
    parser.add_argument("--session", help="caminho do .jsonl ou id da sessão")
    parser.add_argument("--cwd", default=None, help="raiz do projeto (default: cwd atual)")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    payload = read_stdin_payload() if args.hook else {}
    if not args.cwd:
        args.cwd = payload.get("cwd") if isinstance(payload.get("cwd"), str) else os.getcwd()
    args.cwd = os.path.abspath(os.path.expanduser(args.cwd))

    try:
        result = measure(args, payload)
    except TelemetryError as exc:
        if args.hook:
            return emit_hook(None)  # hook silencioso: sem telemetria não é assunto do usuário
        if not args.quiet:
            if args.json:
                safe_print(
                    json.dumps(
                        {"zona": "sem-telemetria", "motivo": str(exc), "exit_code": 40},
                        ensure_ascii=False,
                    )
                )
            else:
                safe_eprint(f"[SEM-TELEMETRIA] {exc}")
                safe_eprint(
                    "Esta ferramenta não expõe telemetria de contexto; nenhuma estimativa "
                    "será inventada. Procedimento: docs/ai/cross-agent-handoff.md"
                )
        return NO_TELEMETRY_CODE
    except Exception as exc:  # degradar, nunca quebrar a sessão
        if args.hook:
            return emit_hook(None)
        if not args.quiet:
            safe_eprint(
                f"[SEM-TELEMETRIA] falha inesperada ao ler o transcript "
                f"({type(exc).__name__}) — formato pode ter mudado."
            )
        return NO_TELEMETRY_CODE

    if args.hook:
        session_key = str(
            payload.get("session_id") or os.path.splitext(result["transcript"])[0]
        )
        path = state_path(session_key)
        state = read_state(path)
        if window_changed(state, result):
            state = {}  # régua nova: zona antiga não trava nem cala o mecanismo
        previous = last_zone(state)
        warned = bool(state.get("window_warned"))
        rose = result["zona_indice"] > previous and result["zona_indice"] > 0
        presumed = not result["janela_confiavel"]

        message = None
        if rose:
            message = hook_message(result)          # já embute o caveat da janela presumida
            warned = warned or presumed
        elif presumed and not warned:
            message = window_hook_message(result)   # B1: a incerteza chega ao caminho automático
            warned = True

        write_state(path, result["zona_indice"], warned, result)
        return emit_hook(message)

    if not args.quiet:
        safe_print(
            json.dumps(result, ensure_ascii=False) if args.json else render_text(result)
        )
    return result["exit_code"]


if __name__ == "__main__":
    hook_mode = "--hook" in sys.argv[1:]
    try:
        exit_code = main()
    except SystemExit as exc:  # argparse (--help, argumento inválido)
        exit_code = 0 if hook_mode else (exc.code if isinstance(exc.code, int) else 2)
    except KeyboardInterrupt:
        exit_code = 0 if hook_mode else NO_TELEMETRY_CODE
    except BaseException:  # nada escapa: hook não pode ter caminho != 0
        exit_code = 0 if hook_mode else NO_TELEMETRY_CODE
    try:
        flush_stdio()  # dentro da região protegida: nem a limpeza pode mudar o exit code
    except BaseException:
        pass
    sys.exit(exit_code)
