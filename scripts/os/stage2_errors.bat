@echo off
chcp 65001 >nul
rem Проверка параметров на скриптах с ошибками.
cd /d "%~dp0..\.."

echo == 1. Без параметров ==
call run.bat

echo == 2. Только --vfs ==
call run.bat --vfs vfs_samples\demo.csv

echo == 3. Только --script ==
call run.bat --script scripts\emulator\stage2_error_unknown.txt

echo == 4. Оба параметра: --vfs и --script ==
call run.bat --vfs vfs_samples\demo.csv --script scripts\emulator\stage2_error_unknown.txt

echo == 5. Скрипт с неверными аргументами команды ==
call run.bat --script scripts\emulator\stage2_error_args.txt

echo == 6. Скрипт с командой exit ==
call run.bat --script scripts\emulator\stage2_exit.txt

echo == 7. Несуществующий файл скрипта ==
call run.bat --script scripts\emulator\does_not_exist.txt

echo == 8. Неизвестный параметр командной строки ==
call run.bat --unknown-option
