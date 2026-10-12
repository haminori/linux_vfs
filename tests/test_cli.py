"""Tests for vfs_shell.cli."""

import pytest

from vfs_shell.cli import (
    derive_vfs_name,
    format_debug_info,
    parse_args,
    window_title,
)
from vfs_shell.config import DEFAULT_VFS_NAME


def test_defaults_are_none():
    """Without arguments both paths are None and the name is default."""
    config = parse_args([])
    assert config.vfs_path is None
    assert config.script_path is None
    assert config.vfs_name == DEFAULT_VFS_NAME


def test_vfs_path_is_parsed():
    """--vfs is captured into the configuration."""
    config = parse_args(["--vfs", "data/sample.csv"])
    assert config.vfs_path == "data/sample.csv"


def test_script_path_is_parsed():
    """--script is captured into the configuration."""
    config = parse_args(["--script", "scripts/demo.txt"])
    assert config.script_path == "scripts/demo.txt"


def test_both_parameters_together():
    """--vfs and --script can be combined in any order."""
    config = parse_args(["--script", "b.txt", "--vfs", "a.csv"])
    assert config.vfs_path == "a.csv"
    assert config.script_path == "b.txt"


def test_vfs_name_is_last_path_component():
    """The VFS name is the file name taken from the --vfs path."""
    assert derive_vfs_name("data/sample.csv") == "sample.csv"


def test_vfs_name_defaults_without_path():
    """Without a path the default VFS name is used."""
    assert derive_vfs_name(None) == DEFAULT_VFS_NAME


def test_window_title_contains_vfs_name():
    """The window title includes the VFS name."""
    config = parse_args(["--vfs", "data/sample.csv"])
    assert "sample.csv" in window_title(config)


def test_unknown_option_exits_with_error():
    """An unknown option makes argparse exit with a non-zero code."""
    with pytest.raises(SystemExit) as info:
        parse_args(["--unknown"])
    assert info.value.code != 0


def test_missing_option_value_exits_with_error():
    """An option without a value is reported as an error."""
    with pytest.raises(SystemExit):
        parse_args(["--vfs"])


def test_debug_info_lists_all_parameters():
    """The debug text mentions every parameter and its value."""
    config = parse_args(["--vfs", "a.csv", "--script", "b.txt"])
    text = format_debug_info(config)
    assert "--vfs" in text and "'a.csv'" in text
    assert "--script" in text and "'b.txt'" in text
    assert "None" not in text


def test_debug_info_shows_none_for_missing_parameters():
    """Parameters that were not given are shown as None."""
    text = format_debug_info(parse_args([]))
    assert text.count("None") == 2
