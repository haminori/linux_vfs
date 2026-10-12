"""Tests for vfs_shell.script."""

import pytest

from vfs_shell.script import (
    ScriptError,
    read_script,
    run_script,
    strip_comment,
)
from vfs_shell.shell import Shell


def test_strip_full_line_comment():
    """A line made only of a comment becomes empty."""
    assert strip_comment("# just a comment") == ""


def test_strip_indented_comment():
    """A comment preceded by spaces is removed as well."""
    assert strip_comment("   # indented") == ""


def test_strip_trailing_comment():
    """Text after a space and '#' is dropped."""
    assert strip_comment("ls /home   # list") == "ls /home"


def test_hash_inside_double_quotes_is_kept():
    """A '#' inside double quotes is part of the argument."""
    assert strip_comment('cd "a # b"  # tail') == 'cd "a # b"'


def test_hash_inside_single_quotes_is_kept():
    """A '#' inside single quotes is part of the argument."""
    assert strip_comment("cd 'a # b'") == "cd 'a # b'"


def test_hash_inside_word_is_not_a_comment():
    """A '#' glued to a word does not start a comment."""
    assert strip_comment("cd a#b") == "cd a#b"


def test_line_without_comment_is_stripped():
    """Plain lines only lose surrounding whitespace."""
    assert strip_comment("  cd /home  ") == "cd /home"


def test_read_script_returns_lines(tmp_path):
    """read_script returns every line of the file."""
    path = tmp_path / "s.txt"
    path.write_text("ls\ncd /home\n", encoding="utf-8")
    assert read_script(str(path)) == ["ls", "cd /home"]


def test_read_script_accepts_utf8_bom(tmp_path):
    """A UTF-8 byte order mark does not end up in the first line."""
    path = tmp_path / "s.txt"
    path.write_bytes(b"\xef\xbb\xbfls\n")
    assert read_script(str(path)) == ["ls"]


def test_read_script_missing_file_raises(tmp_path):
    """A missing script file is reported as ScriptError."""
    with pytest.raises(ScriptError):
        read_script(str(tmp_path / "missing.txt"))


def test_read_script_invalid_encoding_raises(tmp_path):
    """A file that is not UTF-8 text is reported as ScriptError."""
    path = tmp_path / "s.txt"
    path.write_bytes(b"\xff\xfe\x00\x80\x81")
    with pytest.raises(ScriptError):
        read_script(str(path))


def test_run_script_skips_comments_and_blanks():
    """Only real commands produce events, with correct line numbers."""
    lines = ["# comment", "", "ls /home", "   ", "cd /tmp  # go"]
    events = run_script(Shell(), lines)
    assert [e.command for e in events] == ["ls /home", "cd /tmp"]
    assert [e.line_number for e in events] == [3, 5]


def test_run_script_stops_on_error():
    """Execution halts at the first failing command."""
    events = run_script(Shell(), ["ls", "frobnicate", "ls"])
    assert len(events) == 2
    assert events[-1].result.error is not None


def test_run_script_stops_on_exit():
    """Execution halts after the exit command."""
    events = run_script(Shell(), ["ls", "exit", "ls"])
    assert len(events) == 2
    assert events[-1].result.should_exit is True


def test_run_empty_script_has_no_events():
    """A script with no commands produces no events."""
    assert run_script(Shell(), ["# only a comment"]) == []
