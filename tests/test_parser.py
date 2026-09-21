"""Tests for vfs_shell.parser."""

import pytest

from vfs_shell.parser import ParseError, parse_line


def test_parse_simple_command():
    """A plain command with two arguments is split correctly."""
    result = parse_line("ls -la /home")
    assert result.name == "ls"
    assert result.args == ["-la", "/home"]


def test_parse_quoted_argument():
    """A double-quoted argument with spaces stays as one token."""
    result = parse_line('cd "my folder"')
    assert result.name == "cd"
    assert result.args == ["my folder"]


def test_parse_single_quoted_argument():
    """Single quotes also group an argument with spaces."""
    result = parse_line("ls 'a b'")
    assert result.args == ["a b"]


def test_parse_blank_line():
    """A blank or whitespace-only line has no command name."""
    result = parse_line("   ")
    assert result.name == ""
    assert result.args == []


def test_parse_unbalanced_quotes_raises():
    """Unbalanced quotes are reported as a parse error."""
    with pytest.raises(ParseError):
        parse_line('ls "unterminated')
