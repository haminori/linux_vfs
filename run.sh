#!/usr/bin/env bash
# Launches the VFS shell emulator prototype (stage 1).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="${SCRIPT_DIR}/src:${PYTHONPATH:-}"
python3 -m vfs_shell.main "$@"
