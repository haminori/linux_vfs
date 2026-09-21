"""Заглушки команд для Этапа 1.

Команды `ls` и `cd` пока не работают с реальной файловой системой —
они лишь выводят своё имя и полученные аргументы, подтверждая, что
парсер и диспетчер команд работают корректно. `exit` завершает
работу эмулятора.
"""

from __future__ import annotations

LS_MAX_ARGS = 1
CD_REQUIRED_ARGS = 1


class CommandError(Exception):
    """Raised when a command receives invalid arguments or fails."""


class ExitRequested(Exception):
    """Raised by the ``exit`` command to signal shell termination."""


def _format_stub(name: str, args: list[str]) -> str:
    """Render a stub command's name and arguments for display."""
    if not args:
        return f"{name}: вызвана без аргументов"
    joined = ", ".join(repr(arg) for arg in args)
    return f"{name}: вызвана с аргументами [{joined}]"


def cmd_ls(args: list[str]) -> str:
    """Stub for ``ls``: echoes its own name and arguments.

    Args:
        args: At most one path argument.

    Returns:
        A text description of the call.
    """
    if len(args) > LS_MAX_ARGS:
        raise CommandError("ls: слишком много аргументов")
    return _format_stub("ls", args)


def cmd_cd(args: list[str]) -> str:
    """Stub for ``cd``: echoes its own name and arguments.

    Args:
        args: Exactly one target-path argument.

    Returns:
        A text description of the call.
    """
    if len(args) != CD_REQUIRED_ARGS:
        raise CommandError("cd: требуется ровно один аргумент")
    return _format_stub("cd", args)


def cmd_exit(args: list[str]) -> str:
    """Terminate the emulator session.

    Args:
        args: Must be empty.

    Raises:
        ExitRequested: Always, to unwind the REPL loop.
    """
    if args:
        raise CommandError("exit: команда не принимает аргументы")
    raise ExitRequested()


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "exit": cmd_exit,
}
