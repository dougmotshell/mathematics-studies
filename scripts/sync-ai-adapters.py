#!/usr/bin/env python3
"""
sync-ai-adapters.py — Fonte única de paridade da superfície de IA.

Três famílias de fontes canônicas, escritas à mão uma única vez:

  * skills   -> .claude/skills/<name>/SKILL.md          (capacidades)
  * agents   -> .claude/agents/<name>.md                (papéis)
  * rules    -> .github/instructions/<name>.instructions.md  (regras por escopo, campo applyTo)

A partir delas, gera os adapters de cada ferramenta:

| Ferramenta   | Skills                          | Agents                              | Rules                      |
|--------------|---------------------------------|-------------------------------------|----------------------------|
| Claude Code  | nativas (/<skill>)              | .claude/commands/<name>.md          | CLAUDE.md → AGENTS.md      |
| Copilot      | .github/prompts/<n>.prompt.md   | .github/chatmodes/<n>.chatmode.md   | fonte (applyTo)            |
| Gemini CLI   | .gemini/commands/<n>.toml       | .gemini/commands/agent/<n>.toml     | GEMINI.md → AGENTS.md      |
| Cursor       | .cursor/commands/<n>.md         | .cursor/commands/agent-<n>.md       | .cursor/rules/<n>.mdc      |
| Antigravity  | .agents/workflows/<n>.md        | .agents/workflows/agent-<n>.md      | .agents/rules/<n>.md       |
| Windsurf     | .windsurf/workflows/<n>.md      | .windsurf/workflows/agent-<n>.md    | .windsurf/rules/<n>.md     |
| Codex        | $CODEX_HOME/prompts/<n>.md      | $CODEX_HOME/prompts/<n>.md          | AGENTS.md (nativo)         |

Adapters são sobrescritos apenas se contiverem o marcador `managed-by` — arquivos escritos
à mão são preservados e contam como paridade. Também exige memória por agente em
memory/agents/<name>.md.

Uso:
  python3 scripts/sync-ai-adapters.py                      # todas as ferramentas do repo
  python3 scripts/sync-ai-adapters.py --codex              # + prompts do Codex
  python3 scripts/sync-ai-adapters.py --codex --codex-prefix ms
                                                           # + prompts prefixados (evita
                                                           #   colisão com outros repos)
  python3 scripts/sync-ai-adapters.py --check              # não escreve; falha se desatualizado

Prompts do Codex só são descobertos em $CODEX_HOME/prompts (global por usuário, top-level).
Use --codex-prefix ou um CODEX_HOME por projeto quando houver mais de um repositório
instalando prompts — ver docs/ai/tool-support.md.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
AGENTS_DIR = REPO_ROOT / ".claude" / "agents"
RULES_DIR = REPO_ROOT / ".github" / "instructions"
MEMORY_AGENTS_DIR = REPO_ROOT / "memory" / "agents"
CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))

PROJECT = "mathematics-studies"
MD_MARKER = f"<!-- managed-by:{PROJECT}/sync-ai-adapters -->"
HASH_MARKER = f"# managed-by:{PROJECT}/sync-ai-adapters"

# Antigravity e Windsurf truncam arquivos de regra/workflow acima deste tamanho.
RULE_CHAR_LIMIT = 12000


# --------------------------------------------------------------------------- #
# Leitura das fontes
# --------------------------------------------------------------------------- #


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Devolve (frontmatter, corpo). Parser minimalista: escalares e blocos '|' / '>'."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    block = text[3:end].strip("\n")
    body = text[end + 4:].lstrip("\n")
    data: dict[str, str] = {}
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            i += 1
            continue
        key, _, rest = line.partition(":")
        key, rest = key.strip(), rest.strip()
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
    return data, body


def short_desc(desc: str, limit: int = 200) -> str:
    one = " ".join(desc.split())
    return one if len(one) <= limit else one[: limit - 1].rstrip() + "…"


def toml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def discover_skills() -> list[dict[str, str]]:
    out = []
    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        fm, _ = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        out.append({
            "name": fm.get("name") or skill_md.parent.name,
            "desc": fm.get("description", ""),
            "path": f".claude/skills/{skill_md.parent.name}/SKILL.md",
        })
    return out


def discover_agents() -> list[dict[str, str]]:
    out = []
    for agent_md in sorted(AGENTS_DIR.glob("*.md")):
        fm, _ = parse_frontmatter(agent_md.read_text(encoding="utf-8"))
        out.append({
            "name": fm.get("name") or agent_md.stem,
            "desc": fm.get("description", ""),
            "path": f".claude/agents/{agent_md.name}",
        })
    return out


def discover_rules() -> list[dict[str, str]]:
    """Regras por escopo. A fonte é o formato Copilot (applyTo = globs)."""
    out = []
    for rule_md in sorted(RULES_DIR.glob("*.instructions.md")):
        fm, body = parse_frontmatter(rule_md.read_text(encoding="utf-8"))
        name = rule_md.name.replace(".instructions.md", "")
        globs = fm.get("applyTo", "**")
        first_heading = next(
            (ln.lstrip("# ").strip() for ln in body.splitlines() if ln.startswith("#")),
            name,
        )
        out.append({
            "name": name,
            "globs": globs,
            "always": globs.strip() in ("**", "**/*"),
            "title": first_heading,
            "body": body.rstrip(),
            "path": f".github/instructions/{rule_md.name}",
        })
    return out


# --------------------------------------------------------------------------- #
# Renderizadores — capacidades (skills)
# --------------------------------------------------------------------------- #

SKILL_BODY = """Leia e siga integralmente as instruções da skill em `{path}` deste repositório.

Antes de agir, leia também `AGENTS.md` (fonte única de regras) e, para tarefa
significativa, `memory/MEMORY.md` e `docs/errors/README.md`. Respeite os arquivos de apoio
da skill (`references/`, `scripts/`).

Se a skill depender de um MCP (por exemplo `chrome-devtools` em `/pwa-audit` e
`/a11y-audit`), verifique se ele está disponível; sem ele, use o fallback documentado na
própria skill e **declare o que não foi verificado**."""


def skill_copilot_prompt(s: dict) -> str:
    return f"""---
mode: agent
description: {short_desc(s['desc'])}
---
{MD_MARKER}

{SKILL_BODY.format(path=s['path'])}

Aplique a skill ao seguinte contexto: ${{input:contexto}}

Caso o contexto esteja vazio, pergunte ao usuário o que a skill precisa antes de agir.
"""


def skill_gemini_command(s: dict) -> str:
    return f'''{HASH_MARKER}
description = "{toml_escape(short_desc(s['desc'], 120))}"

prompt = """
{SKILL_BODY.format(path=s['path'])}

Aplique a skill à seguinte entrada do usuário:

{{{{args}}}}

Se nenhuma entrada for fornecida, pergunte o que a skill precisa antes de prosseguir.
"""
'''


def skill_cursor_command(s: dict) -> str:
    return f"""{MD_MARKER}

# /{s['name']}

> {short_desc(s['desc'])}

{SKILL_BODY.format(path=s['path'])}

Aplique a skill ao que o usuário pedir nesta conversa. Se nada for informado, pergunte o que
a skill precisa antes de prosseguir.
"""


def skill_workflow_md(s: dict, tool: str) -> str:
    """Workflow do Antigravity / Windsurf (markdown com passos)."""
    trigger = "---\ndescription: " + short_desc(s['desc'], 120) + "\n---\n" if tool == "windsurf" else ""
    return f"""{trigger}{MD_MARKER}

# /{s['name']}

{short_desc(s['desc'])}

## Passos

1. Abra e leia integralmente `{s['path']}` neste repositório — ele contém o procedimento
   completo desta capacidade.
2. Leia `AGENTS.md` (regras do projeto). Para tarefa significativa, leia também
   `memory/MEMORY.md`, o contexto da área em `memory/context/` e `docs/errors/README.md`.
3. Execute o procedimento da skill sobre a entrada fornecida pelo usuário, respeitando os
   arquivos de apoio referenciados (`references/`, `scripts/`).
4. Se a skill depender de um MCP indisponível, use o fallback documentado nela e declare
   explicitamente o que não foi verificado.
5. Ao concluir, apresente o resultado com evidência (saída de comando, trecho de arquivo) e
   proponha as atualizações de `memory/` cabíveis.

Se o usuário não informar a entrada necessária, pergunte antes de prosseguir.
"""


# --------------------------------------------------------------------------- #
# Renderizadores — papéis (agents)
# --------------------------------------------------------------------------- #

AGENT_MEMORY_BLOCK = """## Memória (obrigatório)

- **Antes da tarefa:** ler `memory/MEMORY.md`, `memory/agents/{name}.md`, o contexto da área
  em `memory/context/` e `docs/errors/README.md`.
- **Ao concluir tarefa significativa:** atualizar `memory/agents/{name}.md` (notas
  persistentes + linha em "Últimas execuções") e registrar lições em `memory/lessons/` com os
  índices (`memory/MEMORY.md` e `memory/LESSONS.md`).
- **Em ticket:** toda ação vira entrada no `log.md`, no formato de
  `docs/ai/ticket-protocol.md`."""

AGENT_CONDUCT = """Regras de conduta do papel:

- **Escopo exclusivo:** não invada a área de outro agente — declare o handoff necessário.
- **Não valide o que você mesmo produziu**; validação vem de cadeia distinta.
- **Evidência > afirmação:** mostre a saída real dos comandos e o trecho exato dos arquivos."""


def agent_claude_command(a: dict) -> str:
    return f"""---
description: {short_desc(a['desc'])}
argument-hint: [tarefa ou pergunta para o agente]
---
{MD_MARKER}

Delegue ao subagent `{a['name']}` (definido em @{a['path']}) a seguinte tarefa:

$ARGUMENTS

Passe a tarefa como prompt do subagent via tool Agent (subagent_type:
`{a['name']}`) e devolva o resultado ao usuário. Se nenhuma tarefa for fornecida,
pergunte ao usuário o que o agente deve fazer antes de prosseguir.
"""


def agent_copilot_chatmode(a: dict) -> str:
    return f"""---
description: {short_desc(a['desc'])}
---
{MD_MARKER}

Assuma o papel definido em [`{a['path']}`](../../{a['path']}) e siga integralmente suas
instruções, limites, escopo exclusivo e fontes. As regras gerais estão em
[`AGENTS.md`](../../AGENTS.md); o fluxo de trabalho por tickets, em
[`docs/ai/ticket-protocol.md`](../../docs/ai/ticket-protocol.md).

{AGENT_CONDUCT}

{AGENT_MEMORY_BLOCK.format(name=a['name'])}
"""


def agent_gemini_command(a: dict) -> str:
    return f'''{HASH_MARKER}
description = "{toml_escape(short_desc(a['desc'], 120))}"

prompt = """
Assuma o papel do agente definido em `{a['path']}` deste repositório e siga integralmente
suas instruções, limites, escopo exclusivo e fontes.

Antes de agir, leia: `AGENTS.md`, `memory/MEMORY.md`, `memory/agents/{a['name']}.md`, o
contexto da sua área em `memory/context/` e `docs/errors/README.md`. Se o trabalho pertence a
um ticket, siga `docs/ai/ticket-protocol.md` e registre no `log.md`.

{AGENT_CONDUCT}

Aplique o papel à seguinte entrada:

{{{{args}}}}

Ao concluir tarefa significativa, atualize `memory/agents/{a['name']}.md` e registre lições
em `memory/lessons/` com os índices.
"""
'''


def agent_cursor_command(a: dict) -> str:
    return f"""{MD_MARKER}

# /agent-{a['name']}

> {short_desc(a['desc'])}

Assuma o papel do agente definido em `{a['path']}` deste repositório e siga integralmente
suas instruções, limites, escopo exclusivo e fontes.

Antes de agir, leia `AGENTS.md`, `memory/MEMORY.md`, `memory/agents/{a['name']}.md`, o
contexto da sua área em `memory/context/` e `docs/errors/README.md`. Se o trabalho pertence a
um ticket, siga `docs/ai/ticket-protocol.md`.

{AGENT_CONDUCT}

Aplique o papel ao que o usuário pedir nesta conversa. Ao concluir tarefa significativa,
proponha a atualização de `memory/agents/{a['name']}.md` e, havendo aprendizado
generalizável, uma lição para `memory/lessons/`.
"""


def agent_workflow_md(a: dict, tool: str) -> str:
    trigger = "---\ndescription: " + short_desc(a['desc'], 120) + "\n---\n" if tool == "windsurf" else ""
    return f"""{trigger}{MD_MARKER}

# /agent-{a['name']}

{short_desc(a['desc'])}

## Passos

1. Abra e leia integralmente `{a['path']}` — ele define o papel, o escopo exclusivo, os
   limites e o que este agente **não** faz.
2. Leia `AGENTS.md`, `memory/MEMORY.md`, `memory/agents/{a['name']}.md`, o contexto da área
   em `memory/context/` e `docs/errors/README.md`.
3. Se o trabalho pertence a um ticket, leia `docs/ai/ticket-protocol.md` e o
   `tickets/TCK-NNNN-<slug>/log.md` correspondente.
4. Execute a tarefa **assumindo o papel**, respeitando o escopo exclusivo: trabalho da área
   de outro agente exige handoff, não execução direta.
5. Não valide artefato que você mesmo produziu. Apresente evidência real do resultado.
6. Ao concluir, atualize `memory/agents/{a['name']}.md` e registre lições em
   `memory/lessons/` com os índices; em ticket, registre a entrada no `log.md`.
"""


# --------------------------------------------------------------------------- #
# Renderizadores — regras por escopo
# --------------------------------------------------------------------------- #


def rule_cursor_mdc(r: dict) -> str:
    globs = "" if r["always"] else r["globs"]
    return f"""---
description: {r['title']}
globs: {globs}
alwaysApply: {str(r['always']).lower()}
---
{MD_MARKER}

{r['body']}
"""


def rule_windsurf(r: dict) -> str:
    trigger = "always_on" if r["always"] else "glob"
    glob_line = "" if r["always"] else f"globs: {r['globs']}\n"
    return f"""---
trigger: {trigger}
description: {r['title']}
{glob_line}---
{MD_MARKER}

{r['body']}
"""


def rule_antigravity(r: dict) -> str:
    activation = "Always On" if r["always"] else f"Glob — `{r['globs']}`"
    return f"""{MD_MARKER}
<!-- Ativação sugerida: {activation} (configurável na UI do Antigravity) -->

{r['body']}
"""


def pointer_file(core: dict, tool: str) -> str:
    """Arquivo de regra para ferramentas que leem um único caminho fixo.

    Zed (.rules), Cline/Roo (.clinerules) e JetBrains Junie (.junie/guidelines.md) não têm
    diretório de comandos: recebem a regra-núcleo inteira mais o ponteiro para o AGENTS.md.
    """
    return f"""{MD_MARKER}
<!-- Adaptador para {tool}. Fonte: .github/instructions/core.instructions.md -->

{core['body']}

---

**Capacidades e papéis:** este repositório define capacidades em `.claude/skills/<nome>/SKILL.md`
e papéis em `.claude/agents/<nome>.md` — Markdown legível por qualquer ferramenta. Para usar
um deles aqui, abra o arquivo correspondente e siga suas instruções. O inventário está em
`SLASH_COMMANDS.md`; a matriz de suporte por ferramenta, em `docs/ai/tool-support.md`.
"""


# --------------------------------------------------------------------------- #
# Codex
# --------------------------------------------------------------------------- #


def codex_prompt(item: dict, kind: str) -> str:
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

Não valide artefato que você mesmo produziu. Evidência > afirmação.

Aplique o papel à seguinte entrada: $ARGUMENTS"""
    return f"""---
description: [{PROJECT}] {short_desc(item['desc'], 160)}
argument-hint: [contexto, tarefa ou alvo — opcional]
---
{MD_MARKER}

{body}

Se nenhuma entrada for fornecida, pergunte ao usuário o que é necessário antes de prosseguir.
"""


# --------------------------------------------------------------------------- #
# SLASH_COMMANDS.md
# --------------------------------------------------------------------------- #

SLASH_MD = REPO_ROOT / "SLASH_COMMANDS.md"
SLASH_BEGIN = "<!-- BEGIN GENERATED COMMANDS (sync-ai-adapters.py) -->"
SLASH_END = "<!-- END GENERATED COMMANDS -->"


def commands_table(skills, agents, rules) -> str:
    lines = [
        SLASH_BEGIN,
        "### Capacidades (skills)",
        "",
        "Fonte: `.claude/skills/<nome>/SKILL.md`",
        "",
        "| Comando | O que faz |",
        "|---|---|",
    ]
    for s in skills:
        lines.append(f"| `/{s['name']}` | {short_desc(s['desc'], 130)} |")
    lines += [
        "",
        "### Papéis (agents)",
        "",
        "Fonte: `.claude/agents/<nome>.md`. No Gemini são `/agent:<nome>`; no Cursor,",
        "Antigravity e Windsurf, `/agent-<nome>`.",
        "",
        "| Comando | Papel |",
        "|---|---|",
    ]
    for a in agents:
        lines.append(f"| `/{a['name']}` | {short_desc(a['desc'], 130)} |")
    lines += [
        "",
        "### Regras por escopo",
        "",
        "Fonte: `.github/instructions/<nome>.instructions.md` (o campo `applyTo` vira o glob",
        "de cada ferramenta).",
        "",
        "| Regra | Escopo | Ativação |",
        "|---|---|---|",
    ]
    for r in rules:
        activation = "sempre ativa" if r["always"] else "por glob"
        lines.append(f"| `{r['name']}` | `{r['globs']}` | {activation} |")
    lines += ["", SLASH_END]
    return "\n".join(lines)


def render_slash_md(skills, agents, rules) -> str | None:
    if not SLASH_MD.exists():
        return None
    text = SLASH_MD.read_text(encoding="utf-8")
    begin, end = text.find(SLASH_BEGIN), text.find(SLASH_END)
    if begin == -1 or end == -1:
        return None
    return text[:begin] + commands_table(skills, agents, rules) + text[end + len(SLASH_END):]


# --------------------------------------------------------------------------- #


def write_file(path: Path, content: str, check: bool, changes: list[str]) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else None
    if existing == content:
        return
    try:
        label = str(path.relative_to(REPO_ROOT))
    except ValueError:
        label = str(path)
    changes.append(label)
    if check:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_managed(path, content, marker, check, changes, preserved) -> None:
    """Como write_file, mas nunca sobrescreve adapter escrito à mão (sem o marcador)."""
    if path.exists() and marker not in path.read_text(encoding="utf-8"):
        preserved.append(str(path))
        return
    write_file(path, content, check, changes)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--codex", action="store_true", help="instala prompts em $CODEX_HOME/prompts")
    ap.add_argument("--codex-prefix", default="", metavar="P",
                    help="prefixo dos prompts do Codex (ex.: ms → /ms-create-adr)")
    ap.add_argument("--check", action="store_true", help="não escreve; falha se desatualizado")
    args = ap.parse_args()

    skills, agents, rules = discover_skills(), discover_agents(), discover_rules()
    for label, items in (("skills", skills), ("agents", agents), ("rules", rules)):
        if not items:
            print(f"Nenhuma fonte de {label} encontrada.", file=sys.stderr)
            return 1

    changes: list[str] = []
    preserved: list[str] = []
    oversized: list[str] = []

    D = {
        "claude_cmds": REPO_ROOT / ".claude" / "commands",
        "copilot_prompts": REPO_ROOT / ".github" / "prompts",
        "chatmodes": REPO_ROOT / ".github" / "chatmodes",
        "gemini": REPO_ROOT / ".gemini" / "commands",
        "cursor_cmds": REPO_ROOT / ".cursor" / "commands",
        "cursor_rules": REPO_ROOT / ".cursor" / "rules",
        "ag_flows": REPO_ROOT / ".agents" / "workflows",
        "ag_rules": REPO_ROOT / ".agents" / "rules",
        "ws_flows": REPO_ROOT / ".windsurf" / "workflows",
        "ws_rules": REPO_ROOT / ".windsurf" / "rules",
        "codex": CODEX_HOME / "prompts",
    }

    def managed_md(path, content):
        write_managed(path, content, MD_MARKER, args.check, changes, preserved)

    def managed_toml(path, content):
        write_managed(path, content, HASH_MARKER, args.check, changes, preserved)

    # --- Capacidades -------------------------------------------------------- #
    for s in skills:
        managed_md(D["copilot_prompts"] / f"{s['name']}.prompt.md", skill_copilot_prompt(s))
        managed_toml(D["gemini"] / f"{s['name']}.toml", skill_gemini_command(s))
        managed_md(D["cursor_cmds"] / f"{s['name']}.md", skill_cursor_command(s))
        managed_md(D["ag_flows"] / f"{s['name']}.md", skill_workflow_md(s, "antigravity"))
        managed_md(D["ws_flows"] / f"{s['name']}.md", skill_workflow_md(s, "windsurf"))
        if args.codex:
            name = f"{args.codex_prefix}-{s['name']}" if args.codex_prefix else s["name"]
            write_file(D["codex"] / f"{name}.md", codex_prompt(s, "skill"), args.check, changes)

    # --- Papéis -------------------------------------------------------------- #
    missing_memory: list[str] = []
    for a in agents:
        managed_md(D["claude_cmds"] / f"{a['name']}.md", agent_claude_command(a))
        managed_md(D["chatmodes"] / f"{a['name']}.chatmode.md", agent_copilot_chatmode(a))
        managed_toml(D["gemini"] / "agent" / f"{a['name']}.toml", agent_gemini_command(a))
        managed_md(D["cursor_cmds"] / f"agent-{a['name']}.md", agent_cursor_command(a))
        managed_md(D["ag_flows"] / f"agent-{a['name']}.md", agent_workflow_md(a, "antigravity"))
        managed_md(D["ws_flows"] / f"agent-{a['name']}.md", agent_workflow_md(a, "windsurf"))
        if args.codex:
            name = f"{args.codex_prefix}-{a['name']}" if args.codex_prefix else a["name"]
            write_file(D["codex"] / f"{name}.md", codex_prompt(a, "agent"), args.check, changes)
        if not (MEMORY_AGENTS_DIR / f"{a['name']}.md").exists():
            missing_memory.append(a["name"])

    # --- Regras por escopo --------------------------------------------------- #
    for r in rules:
        for path, content in (
            (D["cursor_rules"] / f"{r['name']}.mdc", rule_cursor_mdc(r)),
            (D["ws_rules"] / f"{r['name']}.md", rule_windsurf(r)),
            (D["ag_rules"] / f"{r['name']}.md", rule_antigravity(r)),
        ):
            managed_md(path, content)
            if len(content) > RULE_CHAR_LIMIT:
                oversized.append(f"{path.relative_to(REPO_ROOT)} ({len(content)} chars)")

    # --- Ferramentas de caminho fixo (Zed, Cline/Roo, Junie) ---------------- #
    core = next((r for r in rules if r["name"] == "core"), None)
    if core is None:
        print("ERRO: falta .github/instructions/core.instructions.md (regra-núcleo).",
              file=sys.stderr)
        return 1
    for path, tool in (
        (REPO_ROOT / ".rules", "Zed"),
        (REPO_ROOT / ".clinerules", "Cline / Roo Code"),
        (REPO_ROOT / ".junie" / "guidelines.md", "JetBrains Junie"),
    ):
        content = pointer_file(core, tool)
        managed_md(path, content)
        if len(content) > RULE_CHAR_LIMIT:
            oversized.append(f"{path.name} ({len(content)} chars)")

    slash_md = render_slash_md(skills, agents, rules)
    if slash_md is None:
        print(f"AVISO: {SLASH_MD.name} sem os marcadores de seção gerada.", file=sys.stderr)
    else:
        write_file(SLASH_MD, slash_md, args.check, changes)

    label = "verificados" if args.check else "sincronizados"
    print(
        f"{len(skills)} skills + {len(agents)} agents + {len(rules)} regras → "
        f"adapters {label} (Claude, Copilot, Gemini, Cursor, Antigravity, Windsurf"
        f"{', Codex' if args.codex else ''})."
    )

    if preserved:
        print(f"{len(preserved)} adapter(s) manual(is) preservado(s) (sem marcador).")

    status = 0
    if oversized:
        print(
            f"\nERRO: {len(oversized)} regra(s) acima do limite de {RULE_CHAR_LIMIT} caracteres "
            "(Antigravity/Windsurf truncam):",
            file=sys.stderr,
        )
        for o in oversized:
            print(f"  {o}", file=sys.stderr)
        status = 1

    if missing_memory:
        print("\nERRO: agents sem memória em memory/agents/: " + ", ".join(missing_memory),
              file=sys.stderr)
        status = 1

    if args.check and changes:
        print("\nDesatualizados (rode sem --check para regenerar):", file=sys.stderr)
        for c in changes:
            print(f"  {c}", file=sys.stderr)
        status = 1
    elif changes:
        print(f"{len(changes)} arquivo(s) escrito(s)/atualizado(s).")
    else:
        print("Tudo já estava atualizado.")

    if not args.codex:
        print("Codex: rode com --codex (veja docs/ai/tool-support.md sobre colisão de nomes).")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
