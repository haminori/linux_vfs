"""Печатает транскрипт диалога с эмулятором без открытия GUI-окна.

Используется только для документации/демонстрации (реальный дисплей
доступен не всегда). Логика форматирования "$ команда / результат"
идентична той, что использует ``vfs_shell.gui`` — сама программа
всегда запускается как GUI-приложение через ``vfs_shell.main``.
"""

from __future__ import annotations

from vfs_shell.config import VFS_NAME
from vfs_shell.shell import Shell

PROMPT = "$ "

DEMO_COMMANDS = [
    "ls",
    'ls "my folder"',
    'ls -la /home "my folder"',
    'cd "my folder"',
    "cd",
    "cd a b",
    "frobnicate --unknown",
    "exit",
    "exit now",
]


def main() -> None:
    """Play a fixed sequence of demo commands through the shell."""
    print(f"Заголовок окна: VFS Shell — {VFS_NAME}\n")
    shell = Shell()
    for line in DEMO_COMMANDS:
        print(f"{PROMPT}{line}")
        result = shell.execute(line)
        if result.error is not None:
            print(f"ошибка: {result.error}")
        elif result.output:
            print(result.output)
        if result.should_exit:
            print("(окно закрывается)")


if __name__ == "__main__":
    main()
