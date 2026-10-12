#!/usr/bin/env bash
# Проверка параметров --vfs и --script на корректном скрипте.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../.."

echo "== 1. Без параметров =="
./run.sh

echo "== 2. Только --vfs =="
./run.sh --vfs vfs_samples/demo.csv

echo "== 3. Только --script =="
./run.sh --script scripts/emulator/stage2_basic.txt

echo "== 4. Оба параметра: --vfs и --script =="
./run.sh --vfs vfs_samples/demo.csv --script scripts/emulator/stage2_basic.txt

