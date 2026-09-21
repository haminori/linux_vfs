"""Tests for vfs_shell.commands and vfs_shell.shell."""

from vfs_shell.shell import Shell


def test_ls_stub_no_args():
    """ls with no arguments reports that it was called without args."""
    result = Shell().execute("ls")
    assert result.error is None
    assert "ls" in result.output
    assert "без аргументов" in result.output


def test_ls_stub_with_args():
    """ls echoes back the argument it received."""
    result = Shell().execute("ls /home")
    assert result.error is None
    assert "'/home'" in result.output


def test_ls_too_many_args_errors():
    """ls with more than one argument is a usage error."""
    result = Shell().execute("ls a b")
    assert result.error is not None
    assert "слишком много" in result.error


def test_cd_stub_echoes_target():
    """cd echoes back its single target argument."""
    result = Shell().execute("cd /home")
    assert result.error is None
    assert "'/home'" in result.output


def test_cd_without_argument_errors():
    """cd without an argument reports a usage error."""
    result = Shell().execute("cd")
    assert result.error is not None


def test_cd_with_quoted_argument():
    """cd accepts a single quoted argument containing spaces."""
    result = Shell().execute('cd "my folder"')
    assert result.error is None
    assert "'my folder'" in result.output


def test_unknown_command_reports_error():
    """An unrecognized command name produces an error result."""
    result = Shell().execute("frobnicate")
    assert result.error is not None
    assert "не найдена" in result.error


def test_exit_signals_termination():
    """exit sets should_exit without raising to the caller."""
    result = Shell().execute("exit")
    assert result.should_exit is True
    assert result.error is None


def test_exit_with_arguments_errors():
    """exit does not accept any arguments."""
    result = Shell().execute("exit now")
    assert result.error is not None
    assert result.should_exit is False


def test_blank_line_is_noop():
    """An empty input line produces no output and no error."""
    result = Shell().execute("   ")
    assert result.output is None
    assert result.error is None
