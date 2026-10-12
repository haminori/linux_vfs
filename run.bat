@echo off
chcp 65001 >nul
rem Запуск эмулятора VFS Shell в Windows: все аргументы передаются дальше.
set "PYTHONPATH=%~dp0src;%PYTHONPATH%"
set "PYTHONIOENCODING=utf-8"
python -m vfs_shell.main %*
