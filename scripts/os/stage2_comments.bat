@echo off
chcp 65001 >nul
rem Проверка параметров на скрипте с комментариями.
cd /d "%~dp0..\.."

echo == 1. Без параметров ==
call run.bat

echo == 2. Только --vfs ==
call run.bat --vfs vfs_samples\demo.csv

echo == 3. Только --script ==
call run.bat --script scripts\emulator\stage2_comments.txt

echo == 4. Оба параметра: --vfs и --script ==
call run.bat --vfs vfs_samples\demo.csv --script scripts\emulator\stage2_comments.txt

