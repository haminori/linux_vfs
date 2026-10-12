"""Подготовка стартового вывода: отладка параметров и скрипт."""

from __future__ import annotations

from dataclasses import dataclass

from vfs_shell.cli import EmulatorConfig, format_debug_info
from vfs_shell.display import (
    format_events,
    script_error_message,
)
from vfs_shell.script import ScriptError, read_script, run_script
from vfs_shell.shell import Shell


@dataclass
class StartupOutput:
    """Вывод, который показывается сразу после запуска эмулятора.

    Attributes:
        lines: Строки для окна: отладка параметров и диалог скрипта.
        errors: Сообщения об ошибках для дублирования в консоль.
        should_exit: Нужно ли закрыть эмулятор после скрипта.
    """

    lines: list[str]
    errors: list[str]
    should_exit: bool


def run_startup(shell: Shell, config: EmulatorConfig) -> StartupOutput:
    """Выполнить стартовые действия согласно конфигурации.

    Args:
        shell: Шелл, в котором выполняется стартовый скрипт.
        config: Конфигурация запуска.

    Returns:
        Строки для отображения, ошибки и признак завершения.
    """
    lines = format_debug_info(config).splitlines()
    if config.script_path is None:
        return StartupOutput(lines, [], False)
    try:
        script_lines = read_script(config.script_path)
    except ScriptError as exc:
        message = f"ошибка: {exc}"
        return StartupOutput(lines + [message], [message], False)
    events = run_script(shell, script_lines)
    lines.extend(format_events(events))
    error = script_error_message(events)
    errors = [error] if error is not None else []
    should_exit = bool(events) and events[-1].result.should_exit
    return StartupOutput(lines, errors, should_exit)
