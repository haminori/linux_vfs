"""Диспетчер команд: разбирает строку и вызывает нужный обработчик.

Не зависит от Tkinter, поэтому тестируется напрямую, без GUI.
"""

from __future__ import annotations

from dataclasses import dataclass

from vfs_shell.commands import COMMANDS, CommandError, ExitRequested
from vfs_shell.parser import ParseError, parse_line


@dataclass
class CommandResult:
    """Outcome of executing a single line of input.

    Attributes:
        output: Text produced by the command, if any.
        error: Error message, if the command failed.
        should_exit: Whether the shell should terminate.
    """

    output: str | None = None
    error: str | None = None
    should_exit: bool = False


class Shell:
    """Executes parsed commands using the stub command registry."""

    def execute(self, line: str) -> CommandResult:
        """Execute a single input line and return its outcome.

        Args:
            line: Raw command line, as typed by the user.

        Returns:
            A CommandResult describing what happened.
        """
        try:
            parsed = parse_line(line)
        except ParseError as exc:
            return CommandResult(error=str(exc))

        if not parsed.name:
            return CommandResult()

        handler = COMMANDS.get(parsed.name)
        if handler is None:
            return CommandResult(error=f"{parsed.name}: команда не найдена")

        try:
            output = handler(parsed.args)
        except ExitRequested:
            return CommandResult(should_exit=True)
        except CommandError as exc:
            return CommandResult(error=str(exc))

        return CommandResult(output=output)
