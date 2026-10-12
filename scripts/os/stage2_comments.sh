#!/usr/bin/env bash
# Проверка параметров на скрипте с комментариями.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../.."

echo "== 1. Без параметров =="
./run.sh

echo "== 2. Только --vfs =="
./run.sh --vfs vfs_samples/demo.csv

echo "== 3. Только --script =="
./run.sh --script scripts/emulator/stage2_comments.txt

echo "== 4. Оба параметра: --vfs и --script =="
./run.sh --vfs vfs_samples/demo.csv --script scripts/emulator/stage2_comments.txt

