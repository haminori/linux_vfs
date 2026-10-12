"""Форматирование диалога с эмулятором в строки для вывода.

Используется и графическим окном, и демонстрационным транскриптом,
поэтому оба показывают диалог одинаково.
"""

from __future__ import annotations

from vfs_shell.config import PROMPT
from vfs_shell.script import ScriptEvent
from vfs_shell.shell import CommandResult


def format_result(result: CommandResult) -> list[str]:
    """Превратить результат команды в строки для вывода.

    Args:
        result: Результат выполнения команды.

    Returns:
        Строки с сообщением об ошибке или с выводом команды.
    """
    if result.error is not None:
        return [f"ошибка: {result.error}"]
    if result.output:
        return [result.output]
    return []


def script_error_message(events: list[ScriptEvent]) -> str | None:
    """Сформировать сообщение об ошибке стартового скрипта.

    Args:
        events: События выполненного скрипта.

    Returns:
        Текст сообщения либо None, если ошибок не было.
    """
    if not events:
        return None
    last = events[-1]
    if last.result.error is None:
        return None
    return (
        f"ошибка в строке {last.line_number} стартового скрипта: "
        f"{last.result.error}. Выполнение скрипта остановлено."
    )


def format_events(events: list[ScriptEvent]) -> list[str]:
    """Показать выполнение скрипта как диалог ввода и вывода.

    Args:
        events: События выполненного скрипта.

    Returns:
        Строки диалога: введённая команда, затем её вывод.
    """
    lines: list[str] = []
    for event in events:
        lines.append(f"{PROMPT}{event.command}")
        lines.extend(format_result(event.result))
    message = script_error_message(events)
    if message is not None:
        lines.append(message)
    return lines
