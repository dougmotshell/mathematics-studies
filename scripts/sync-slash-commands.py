#!/usr/bin/env python3
"""
sync-slash-commands.py — Fonte única de paridade da superfície de IA.

Descobre duas famílias de fontes e gera os adapters equivalentes para os CLIs usados
no projeto (Claude Code, GitHub Copilot, Gemini CLI, OpenAI Codex):

  1. skills locais (.claude/skills/<name>/SKILL.md):
       Claude  -> nativo (/<name>), nada a gerar
       Copilot -> .github/prompts/<name>.prompt.md
       Gemini  -> .gemini/commands/<name>.toml
       Codex   -> $CODEX_HOME/prompts/<name>.md        (com --codex)
  2. agents (.claude/agents/<name>.md):
       Claude  -> .claude/commands/<name>.md           (slash command do agente)
       Copilot -> .github/chatmodes/<name>.chatmode.md
       Gemini  -> .gemini/commands/agent/<name>.toml   (/agent:<name>)
       Codex   -> $CODEX_HOME/prompts/<name>.md        (com --codex)

Adapters são sobrescritos apenas se contiverem o MANAGED_MARKER — arquivos escritos
à mão são preservados e contam como paridade. O gerador também exige memória por
agente em memory/agents/<name>.md.

Uso:
  python3 scripts/sync-slash-commands.py            # gera Claude + Copilot + Gemini
  python3 scripts/sync-slash-commands.py --codex    # também instala prompts do Codex
  python3 scripts/sync-slash-commands.py --check    # não escreve; falha se desatualizado

Custom prompts do Codex só são descobertos em $CODEX_HOME/prompts (top-level) e não
podem viver no repositório — por isso o passo --codex copia os arquivos para lá,
embutindo o caminho absoluto deste repo em cada prompt.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LOCAL_SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
AGENTS_DIR = REPO_ROOT / ".claude" / "agents"
MEMORY_AGENTS_DIR = REPO_ROOT / "memory" / "agents"
CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))

PROJECT = "mathematics-studies"
CODEX_MARKER = f"<!-- managed-by:{PROJECT} -->"
MANAGED_MARKER = f"<!-- managed-by:{PROJECT}/sync-slash-commands -->"
TOML_MARKER = f"# managed-by:{PROJECT}/sync-slash-commands"


def parse_frontmatter(text: str) -> dict[str, str]:
    """Parser minimalista de frontmatter YAML: escalares e blocos '|' / '>'."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip("\n")
    data: dict[str, str] = {}
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            i += 1
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest in ("|", ">", "|-", ">-"):
            base_indent = len(line) - len(line.lstrip())
            collected: list[str] = []
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if nxt.strip() and (len(nxt) - len(nxt.lstrip())) <= base_indent:
                    break
                collected.append(nxt.strip())
                i += 1
            data[key] = " ".join(c for c in collected if c).strip()
        else:
            data[key] = rest.strip().strip('"').strip("'")
            i += 1
    return data


def short_desc(desc: str, limit: int = 200) -> str:
    one = " ".join(desc.split())
    return one if len(one) <= limit else one[: limit - 1].rstrip() + "…"


def toml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def discover_skills() -> list[dict[str, str]]:
    skills = []
    for skill_md in sorted(LOCAL_SKILLS_DIR.glob("*/SKILL.md")):
        fm = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        skills.append(
            {
                "name": fm.get("name") or skill_md.parent.name,
                "desc": fm.get("description", ""),
                "path": f".claude/skills/{skill_md.parent.name}/SKILL.md",
            }
        )
    return skills


def discover_agents() -> list[dict[str, str]]:
    agents = []
    for agent_md in sorted(AGENTS_DIR.glob("*.md")):
        fm = parse_frontmatter(agent_md.read_text(encoding="utf-8"))
        agents.append(
            {
                "name": fm.get("name") or agent_md.stem,
                "desc": fm.get("description", ""),
                "path": f".claude/agents/{agent_md.name}",
            }
        )
    return agents


# --------------------------------------------------------------------------- #
# Renderizadores por ferramenta
# --------------------------------------------------------------------------- #


def skill_copilot_prompt(s: dict[str, str]) -> str:
    return f"""---
mode: agent
description: {short_desc(s['desc'])}
---
{MANAGED_MARKER}

Leia e siga integralmente as instruções da skill em [`{s['path']}`](../../{s['path']}).

Aplique-as ao seguinte contexto: ${{input:contexto}}

Respeite os arquivos de apoio da skill (`references/`, `scripts/`) e as regras do
`AGENTS.md` — em especial bilinguismo pt-BR/en-US, acessibilidade e verificação de
resultados matemáticos. Se a skill depender de um MCP (ex.: `chrome-devtools` em
`/pwa-audit` e `/a11y-audit`), verifique se ele está configurado; sem ele, use o
fallback documentado na própria skill e declare o que não foi verificado.

Caso o contexto esteja vazio, pergunte ao usuário o que a skill precisa antes de agir.
"""


def skill_gemini_command(s: dict[str, str]) -> str:
    return f'''{TOML_MARKER}
description = "{toml_escape(short_desc(s['desc'], 120))}"

prompt = """
Leia e siga integralmente as instruções da skill em `{s['path']}` deste repositório.

Antes de agir, leia também `AGENTS.md` (fonte única de instruções) e, se a tarefa for
significativa, `memory/MEMORY.md` e `docs/errors/README.md`.

Aplique a skill à seguinte entrada do usuário:

{{{{args}}}}

Se nenhuma entrada for fornecida, pergunte o que a skill precisa antes de prosseguir.
"""
'''


def agent_claude_command(a: dict[str, str]) -> str:
    return f"""---
description: {short_desc(a['desc'])}
argument-hint: [tarefa ou pergunta para o agente]
---
{MANAGED_MARKER}

Delegue ao subagent `{a['name']}` (definido em @{a['path']}) a seguinte tarefa:

$ARGUMENTS

Passe a tarefa como prompt do subagent via tool Agent (subagent_type:
`{a['name']}`) e devolva o resultado ao usuário. Se nenhuma tarefa for fornecida,
pergunte ao usuário o que o agente deve fazer antes de prosseguir.
"""


def agent_copilot_chatmode(a: dict[str, str]) -> str:
    return f"""---
description: {short_desc(a['desc'])}
---
{MANAGED_MARKER}

Assuma o papel definido em [`{a['path']}`](../../{a['path']}) e siga integralmente suas
instruções, limites, escopo exclusivo e fontes. As regras gerais do projeto estão em
[`AGENTS.md`](../../AGENTS.md); o fluxo de trabalho por tickets está em
[`docs/ai/ticket-protocol.md`](../../docs/ai/ticket-protocol.md).

## Memória (obrigatório)

- **Antes da tarefa:** ler `memory/MEMORY.md`, `memory/agents/{a['name']}.md`, o contexto
  da área em `memory/context/` e `docs/errors/README.md`.
- **Ao concluir tarefa significativa:** atualizar `memory/agents/{a['name']}.md` (notas
  persistentes + linha em "Últimas execuções") e registrar lições de erro ou sucesso em
  `memory/lessons/` com os índices (`memory/MEMORY.md` e `memory/LESSONS.md`).
- **Em ticket:** toda ação vira entrada no `log.md` do ticket, no formato do protocolo.
"""


def agent_gemini_command(a: dict[str, str]) -> str:
    return f'''{TOML_MARKER}
description = "{toml_escape(short_desc(a['desc'], 120))}"

prompt = """
Assuma o papel do agente definido em `{a['path']}` deste repositório e siga
integralmente suas instruções, limites, escopo exclusivo e fontes.

Antes de agir, leia: `AGENTS.md`, `memory/MEMORY.md`, `memory/agents/{a['name']}.md`,
o contexto da sua área em `memory/context/` e `docs/errors/README.md`. Se o trabalho
pertence a um ticket, siga `docs/ai/ticket-protocol.md` e registre no `log.md`.

Aplique o papel à seguinte entrada:

{{{{args}}}}

Ao concluir tarefa significativa, atualize `memory/agents/{a['name']}.md` e registre
lições em `memory/lessons/` com os índices.
"""
'''


def codex_prompt(item: dict[str, str], kind: str) -> str:
    abs_path = REPO_ROOT / item["path"]
    if kind == "skill":
        body = f"""Leia e siga integralmente as instruções da skill localizada em:

{abs_path}

(Repositório: {REPO_ROOT})

Aplique-as à seguinte entrada: $ARGUMENTS

Respeite os arquivos de apoio da skill e as regras de {REPO_ROOT}/AGENTS.md."""
    else:
        body = f"""Assuma o papel do agente definido em:

{abs_path}

(Repositório: {REPO_ROOT})

Siga integralmente as instruções, limites, escopo exclusivo e o protocolo de memória do
arquivo (incluindo memory/agents/{item['name']}.md e o contexto da área em
memory/context/). Se o trabalho pertence a um ticket, siga
{REPO_ROOT}/docs/ai/ticket-protocol.md.

Aplique o papel à seguinte entrada: $ARGUMENTS"""
    return f"""---
description: {short_desc(item['desc'])}
argument-hint: [contexto, tarefa ou alvo — opcional]
---
{CODEX_MARKER}

{body}

Se nenhuma entrada for fornecida, pergunte ao usuário o que é necessário antes de
prosseguir.
"""


# --------------------------------------------------------------------------- #
# SLASH_COMMANDS.md
# --------------------------------------------------------------------------- #

SLASH_MD = REPO_ROOT / "SLASH_COMMANDS.md"
SLASH_BEGIN = "<!-- BEGIN GENERATED COMMANDS (sync-slash-commands.py) -->"
SLASH_END = "<!-- END GENERATED COMMANDS -->"


def commands_table(skills: list[dict[str, str]], agents: list[dict[str, str]]) -> str:
    lines = [
        SLASH_BEGIN,
        "### Skills (`.claude/skills/`)",
        "",
        "| Comando | O que faz |",
        "|---|---|",
    ]
    for s in skills:
        lines.append(f"| `/{s['name']}` | {short_desc(s['desc'], 130)} |")
    lines += [
        "",
        "### Agents (`.claude/agents/`)",
        "",
        "| Comando | Papel |",
        "|---|---|",
    ]
    for a in agents:
        lines.append(f"| `/{a['name']}` | {short_desc(a['desc'], 130)} |")
    lines += [
        "",
        "> No Gemini CLI os agents ficam no namespace `agent:` (ex.: `/agent:math-reviewer`).",
        "> No Copilot, agents são **chat modes** e skills são **prompt files**.",
        "> No Codex, ambos são prompts pessoais instalados por `--codex`.",
        SLASH_END,
    ]
    return "\n".join(lines)


def render_slash_md(skills, agents) -> str | None:
    if not SLASH_MD.exists():
        return None
    text = SLASH_MD.read_text(encoding="utf-8")
    begin = text.find(SLASH_BEGIN)
    end = text.find(SLASH_END)
    if begin == -1 or end == -1:
        return None
    return text[:begin] + commands_table(skills, agents) + text[end + len(SLASH_END):]


# --------------------------------------------------------------------------- #


def write_file(path: Path, content: str, check: bool, changes: list[str]) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else None
    if existing == content:
        return
    changes.append(str(path.relative_to(REPO_ROOT) if REPO_ROOT in path.parents else path))
    if check:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_managed(
    path: Path, content: str, marker: str, check: bool, changes: list[str], preserved: list[str]
) -> None:
    """Como write_file, mas nunca sobrescreve adapter manual (sem o marcador)."""
    if path.exists() and marker not in path.read_text(encoding="utf-8"):
        preserved.append(str(path))
        return
    write_file(path, content, check, changes)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--codex", action="store_true", help="instala prompts em $CODEX_HOME/prompts")
    ap.add_argument("--check", action="store_true", help="não escreve; falha se desatualizado")
    args = ap.parse_args()

    skills = discover_skills()
    agents = discover_agents()
    if not skills:
        print("Nenhuma skill encontrada em .claude/skills/*/SKILL.md", file=sys.stderr)
        return 1
    if not agents:
        print("Nenhum agent encontrado em .claude/agents/*.md", file=sys.stderr)
        return 1

    changes: list[str] = []
    preserved: list[str] = []
    claude_cmds = REPO_ROOT / ".claude" / "commands"
    copilot_prompts = REPO_ROOT / ".github" / "prompts"
    chatmodes = REPO_ROOT / ".github" / "chatmodes"
    gemini_cmds = REPO_ROOT / ".gemini" / "commands"
    codex_dir = CODEX_HOME / "prompts"

    # Skills: Claude descobre nativamente; gerar Copilot, Gemini e Codex.
    for s in skills:
        write_managed(
            copilot_prompts / f"{s['name']}.prompt.md",
            skill_copilot_prompt(s), MANAGED_MARKER, args.check, changes, preserved,
        )
        write_managed(
            gemini_cmds / f"{s['name']}.toml",
            skill_gemini_command(s), TOML_MARKER, args.check, changes, preserved,
        )
        if args.codex:
            write_file(codex_dir / f"{s['name']}.md", codex_prompt(s, "skill"), args.check, changes)

    # Agents: slash command Claude + chatmode Copilot + command Gemini + prompt Codex.
    missing_memory: list[str] = []
    for a in agents:
        write_managed(
            claude_cmds / f"{a['name']}.md",
            agent_claude_command(a), MANAGED_MARKER, args.check, changes, preserved,
        )
        write_managed(
            chatmodes / f"{a['name']}.chatmode.md",
            agent_copilot_chatmode(a), MANAGED_MARKER, args.check, changes, preserved,
        )
        write_managed(
            gemini_cmds / "agent" / f"{a['name']}.toml",
            agent_gemini_command(a), TOML_MARKER, args.check, changes, preserved,
        )
        if args.codex:
            write_file(codex_dir / f"{a['name']}.md", codex_prompt(a, "agent"), args.check, changes)
        if not (MEMORY_AGENTS_DIR / f"{a['name']}.md").exists():
            missing_memory.append(a["name"])

    slash_md = render_slash_md(skills, agents)
    if slash_md is None:
        print(
            f"AVISO: {SLASH_MD.name} sem os marcadores '{SLASH_BEGIN}' / '{SLASH_END}' — "
            "tabela não gerenciada.",
            file=sys.stderr,
        )
    else:
        write_file(SLASH_MD, slash_md, args.check, changes)

    label = "verificados" if args.check else "sincronizados"
    print(f"{len(skills)} skills + {len(agents)} agents → adapters {label}.")

    if preserved:
        print(f"{len(preserved)} adapter(s) manual(is) preservado(s) (sem marcador gerenciado).")

    if missing_memory:
        print(
            "\nERRO: agents sem memória em memory/agents/: " + ", ".join(missing_memory),
            file=sys.stderr,
        )
        return 1

    if args.check and changes:
        print("\nDesatualizados (rode sem --check para regenerar):", file=sys.stderr)
        for c in changes:
            print(f"  {c}", file=sys.stderr)
        return 1

    if changes:
        print(f"{len(changes)} arquivo(s) escrito(s)/atualizado(s).")
    else:
        print("Tudo já estava atualizado.")

    if not args.codex:
        print("Codex: rode com --codex para instalar em $CODEX_HOME/prompts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
