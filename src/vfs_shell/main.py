"""Entry point for the VFS shell emulator prototype (Этап 1)."""

from __future__ import annotations

from vfs_shell.gui import launch_gui
from vfs_shell.shell import Shell


def main() -> None:
    """Create a Shell instance and launch the GUI."""
    shell = Shell()
    launch_gui(shell)


if __name__ == "__main__":
    main()
