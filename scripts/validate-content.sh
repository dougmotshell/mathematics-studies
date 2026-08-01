#!/usr/bin/env bash
# validate-content.sh — validador do contrato de carga de content/ (spec RF-18).
# Uso: bash scripts/validate-content.sh [--json] [--quiet] [caminho ...]
# Saída: 0 contrato íntegro · 1 violação · 2 erro de uso.
set -euo pipefail
repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$repo_dir/scripts/validate-content.py" "$@"
