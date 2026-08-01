#!/usr/bin/env bash
# precompact-snapshot.sh — hook PreCompact (matcher `auto`) de TCK-0012.
#
# A compactação automática do Claude Code é lossy: o detalhe se perde quando ela dispara.
# Este wrapper escreve o snapshot de handoff ANTES da compactação e avisa o usuário.
# Ele nunca falha: um hook que quebra a sessão é pior que nenhum hook.
#
# Entrada: payload JSON do hook no stdin (drenado, nunca impresso — contém metadados da
# sessão). Saída: uma linha JSON com `systemMessage`. Exit code: sempre 0.

set -uo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
cat > /dev/null 2>&1 || true   # drena o stdin do hook

msg="[handoff] compactação automática detectada, mas o snapshot não pôde ser escrito — rode: bash tools/agent-handoff.sh snapshot --force"
if bash "$ROOT/tools/agent-handoff.sh" snapshot --force --quiet < /dev/null > /dev/null 2>&1; then
  msg="[handoff] compactação automática a caminho (lossy): estado do repositório salvo em .agent-handoff.md antes da perda de detalhe. Preencha as seções <preencher> e valide com: bash tools/agent-handoff.sh validate"
fi

printf '{"systemMessage":"%s"}\n' "$msg"
exit 0
