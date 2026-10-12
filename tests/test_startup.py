"""Tests for vfs_shell.display and vfs_shell.startup."""

from vfs_shell.cli import parse_args
from vfs_shell.config import PROMPT
from vfs_shell.display import (
    format_events,
    format_result,
    script_error_message,
)
from vfs_shell.script import run_script
from vfs_shell.shell import CommandResult, Shell
from vfs_shell.startup import run_startup


def _write_script(tmp_path, text):
    """Write a startup script and return its path as a string."""
    path = tmp_path / "script.txt"
    path.write_text(text, encoding="utf-8")
    return str(path)


def _only(items):
    """Return the single item of ``items``; fail if there is not one."""
    (item,) = items
    return item


def test_format_result_for_output_and_error():
    """Output and errors are rendered as separate kinds of lines."""
    assert format_result(CommandResult(output="text")) == ["text"]
    assert format_result(CommandResult(error="boom")) == ["ошибка: boom"]
    assert format_result(CommandResult()) == []


def test_format_events_shows_input_and_output():
    """The dialog contains the typed command followed by its output."""
    events = run_script(Shell(), ["ls /home"])
    typed, shown = format_events(events)
    assert typed == f"{PROMPT}ls /home"
    assert "'/home'" in shown


def test_format_events_reports_error_line_number():
    """A failing script ends with a message naming the line."""
    events = run_script(Shell(), ["ls", "", "frobnicate"])
    message = script_error_message(events)
    assert message is not None
    assert "строке 3" in message
    *_, last_line = format_events(events)
    assert last_line == message


def test_no_error_message_for_successful_script():
    """A successful script has no error message."""
    assert script_error_message(run_script(Shell(), ["ls"])) is None


def test_startup_without_script_has_only_debug_lines():
    """Without --script only the debug parameters are shown."""
    output = run_startup(Shell(), parse_args([]))
    assert output.errors == []
    assert output.should_exit is False
    assert all(line.startswith("[отладка]") for line in output.lines)


def test_startup_runs_script_and_shows_dialog(tmp_path):
    """The script dialog follows the debug lines."""
    path = _write_script(tmp_path, "# c\nls\n")
    output = run_startup(Shell(), parse_args(["--script", path]))
    assert f"{PROMPT}ls" in output.lines
    assert output.errors == []


def test_startup_reports_script_error(tmp_path):
    """An error inside the script is returned for the console."""
    path = _write_script(tmp_path, "ls\ncd\nls\n")
    output = run_startup(Shell(), parse_args(["--script", path]))
    assert "строке 2" in _only(output.errors)
    ran = [line for line in output.lines if line == f"{PROMPT}ls"]
    assert ran == [f"{PROMPT}ls"]


def test_startup_reports_missing_script(tmp_path):
    """A missing script file produces an error and no dialog."""
    missing = str(tmp_path / "missing.txt")
    output = run_startup(Shell(), parse_args(["--script", missing]))
    *_, last_line = output.lines
    assert last_line == _only(output.errors)


def test_startup_requests_exit(tmp_path):
    """An exit command in the script asks the GUI to close."""
    path = _write_script(tmp_path, "ls\nexit\nls\n")
    output = run_startup(Shell(), parse_args(["--script", path]))
    assert output.should_exit is True
    ran = [line for line in output.lines if line == f"{PROMPT}ls"]
    assert ran == [f"{PROMPT}ls"]
