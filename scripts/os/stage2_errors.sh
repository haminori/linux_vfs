#!/usr/bin/env bash
# Проверка параметров на скриптах с ошибками.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../.."

echo "== 1. Без параметров =="
./run.sh

echo "== 2. Только --vfs =="
./run.sh --vfs vfs_samples/demo.csv

echo "== 3. Только --script =="
./run.sh --script scripts/emulator/stage2_error_unknown.txt

echo "== 4. Оба параметра: --vfs и --script =="
./run.sh --vfs vfs_samples/demo.csv --script scripts/emulator/stage2_error_unknown.txt

echo "== 5. Скрипт с неверными аргументами команды =="
./run.sh --script scripts/emulator/stage2_error_args.txt

echo "== 6. Скрипт с командой exit =="
./run.sh --script scripts/emulator/stage2_exit.txt

echo "== 7. Несуществующий файл скрипта =="
./run.sh --script scripts/emulator/does_not_exist.txt

echo "== 8. Неизвестный параметр командной строки =="
./run.sh --unknown-option || echo "эмулятор завершился с кодом $?"
