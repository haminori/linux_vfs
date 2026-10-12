"""Печатает транскрипт диалога с эмулятором без открытия GUI-окна.

Используется только для документации и демонстрации (реальный дисплей
доступен не всегда). Принимает те же параметры, что и эмулятор, и
выводит ровно те строки, которые показало бы окно. Сама программа
всегда запускается как GUI-приложение через ``vfs_shell.main``.
"""

from __future__ import annotations

from vfs_shell.cli import parse_args, window_title
from vfs_shell.config import PROMPT
from vfs_shell.display import format_result
from vfs_shell.shell import Shell
from vfs_shell.startup import run_startup

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


def play_interactive(shell: Shell, commands: list[str]) -> None:
    """Воспроизвести интерактивный диалог из списка команд.

    Args:
        shell: Шелл, выполняющий команды.
        commands: Команды, как если бы их вводил пользователь.
    """
    for line in commands:
        print(f"{PROMPT}{line}")
        result = shell.execute(line)
        for text in format_result(result):
            print(text)
        if result.should_exit:
            print("(окно закрывается)")


def main(argv: list[str] | None = None) -> None:
    """Напечатать транскрипт для заданных параметров запуска.

    Args:
        argv: Список аргументов; по умолчанию ``sys.argv[1:]``.
    """
    config = parse_args(argv)
    shell = Shell()
    startup = run_startup(shell, config)
    print(f"Заголовок окна: {window_title(config)}")
    print("\n".join(startup.lines))
    if startup.should_exit:
        print("(окно закрывается)")
    elif config.script_path is None:
        play_interactive(shell, DEMO_COMMANDS)


if __name__ == "__main__":
    main()
