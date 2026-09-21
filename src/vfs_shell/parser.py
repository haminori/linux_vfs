"""Parsing of shell input lines into command name and arguments."""

from __future__ import annotations

import shlex
from dataclasses import dataclass


class ParseError(Exception):
    """Raised when an input line cannot be parsed."""


@dataclass
class ParsedCommand:
    """Result of parsing a single input line.

    Attributes:
        name: The command name, empty string for a blank line.
        args: The list of arguments following the command name.
    """

    name: str
    args: list[str]


def parse_line(line: str) -> ParsedCommand:
    """Parse a raw input line into a command name and its arguments.

    Supports single and double quoted arguments (including arguments
    that contain spaces), following POSIX shell-like quoting rules.

    Args:
        line: The raw line typed by the user.

    Returns:
        A ParsedCommand describing the command and its arguments.

    Raises:
        ParseError: If the line has unbalanced quotes and cannot be
            tokenized.
    """
    try:
        tokens = shlex.split(line, comments=False, posix=True)
    except ValueError as exc:
        raise ParseError(f"ошибка разбора команды: {exc}") from exc

    if not tokens:
        return ParsedCommand(name="", args=[])
    return ParsedCommand(name=tokens[0], args=tokens[1:])
