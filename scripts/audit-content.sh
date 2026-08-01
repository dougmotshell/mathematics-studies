#!/usr/bin/env bash
# audit-content.sh — auditoria determinística do acervo em content/.
# Uso: bash scripts/audit-content.sh [caminho-relativo-dentro-de-content]
set -euo pipefail
repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$repo_dir/scripts/audit-content.py" "$@"
