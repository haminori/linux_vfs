"""Entry point for the VFS shell emulator application."""

from __future__ import annotations

from vfs_shell.cli import format_debug_info, parse_args, window_title
from vfs_shell.gui import launch_gui
from vfs_shell.shell import Shell
from vfs_shell.startup import run_startup


def main(argv: list[str] | None = None) -> None:
    """Parse arguments, run startup actions and launch the GUI.

    Args:
        argv: Optional argument list, primarily for testing.
    """
    config = parse_args(argv)
    print(format_debug_info(config))
    shell = Shell()
    startup = run_startup(shell, config)
    for message in startup.errors:
        print(message)
    launch_gui(shell, window_title(config), startup.lines, startup.should_exit)


if __name__ == "__main__":
    main()
