"""Чтение и выполнение стартовых скриптов эмулятора.

Комментарии в скрипте используют синтаксис языка реализации (Python):
символ ``#`` вне кавычек начинает комментарий до конца строки.
"""

from __future__ import annotations

from dataclasses import dataclass

from vfs_shell.shell import CommandResult, Shell

COMMENT_CHAR = "#"
QUOTE_CHARS = "'\""
SCRIPT_ENCODING = "utf-8-sig"


class ScriptError(Exception):
    """Ошибка чтения стартового скрипта."""


@dataclass
class ScriptEvent:
    """Результат выполнения одной команды стартового скрипта.

    Attributes:
        line_number: Номер строки в файле скрипта (с единицы).
        command: Текст команды без комментария.
        result: Результат выполнения команды.
    """

    line_number: int
    command: str
    result: CommandResult


def _starts_comment(line: str, index: int) -> bool:
    """Проверить, что ``#`` в позиции index начинает комментарий."""
    if line[index] != COMMENT_CHAR:
        return False
    return not index or line[index - 1].isspace()


def strip_comment(line: str) -> str:
    """Удалить комментарий из строки скрипта.

    Символ ``#`` внутри кавычек комментарием не считается.

    Args:
        line: Исходная строка скрипта.

    Returns:
        Строка без комментария и без крайних пробелов.
    """
    quote = None
    for index, char in enumerate(line):
        if quote is not None:
            if char == quote:
                quote = None
        elif char in QUOTE_CHARS:
            quote = char
        elif _starts_comment(line, index):
            return line[:index].strip()
    return line.strip()


def read_script(path: str) -> list[str]:
    """Прочитать стартовый скрипт с диска.

    Args:
        path: Путь к файлу скрипта.

    Returns:
        Список строк файла.

    Raises:
        ScriptError: Если файл не найден или не читается.
    """
    try:
        with open(path, encoding=SCRIPT_ENCODING) as handle:
            return handle.read().splitlines()
    except OSError as exc:
        reason = exc.strerror or str(exc)
        raise ScriptError(
            f"не удалось открыть стартовый скрипт {path!r}: {reason}"
        ) from exc
    except UnicodeDecodeError as exc:
        raise ScriptError(
            f"стартовый скрипт {path!r} не является текстом UTF-8"
        ) from exc


def run_script(shell: Shell, lines: list[str]) -> list[ScriptEvent]:
    """Выполнить команды скрипта по порядку.

    Пустые строки и комментарии пропускаются. Выполнение прекращается
    на первой ошибке или команде ``exit``.

    Args:
        shell: Шелл, выполняющий команды.
        lines: Строки скрипта.

    Returns:
        События для каждой фактически выполненной команды.
    """
    events: list[ScriptEvent] = []
    for number, raw_line in enumerate(lines, start=1):
        command = strip_comment(raw_line)
        if not command:
            continue
        result = shell.execute(command)
        events.append(ScriptEvent(number, command, result))
        if result.error is not None or result.should_exit:
            break
    return events
