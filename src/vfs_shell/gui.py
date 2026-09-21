"""Tkinter-based graphical front end for the shell-emulator prototype."""

from __future__ import annotations

import tkinter as tk
from tkinter import scrolledtext

from vfs_shell.config import VFS_NAME
from vfs_shell.shell import CommandResult, Shell

PROMPT = "$ "


class ShellWindow:
    """A terminal-like Tkinter window driving a Shell instance."""

    def __init__(self, root: tk.Tk, shell: Shell, title: str) -> None:
        """Build the window widgets.

        Args:
            root: The Tkinter root window.
            shell: The Shell instance to execute commands against.
            title: Window title, expected to contain the VFS name.
        """
        self.root = root
        self.shell = shell
        self.root.title(title)

        self.output = scrolledtext.ScrolledText(
            root, state="disabled", height=24, width=90
        )
        self.output.pack(fill="both", expand=True)

        entry_frame = tk.Frame(root)
        entry_frame.pack(fill="x")
        tk.Label(entry_frame, text=PROMPT).pack(side="left")
        self.entry = tk.Entry(entry_frame)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", self._on_enter)
        self.entry.focus_set()

    def _on_enter(self, _event: tk.Event) -> None:
        """Handle the user pressing Enter in the command entry."""
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        self.print_line(f"{PROMPT}{line}")
        result = self.shell.execute(line)
        self._show_result(result)
        if result.should_exit:
            self.root.quit()

    def _show_result(self, result: CommandResult) -> None:
        """Render a CommandResult into the output pane."""
        if result.error is not None:
            self.print_line(f"ошибка: {result.error}")
        elif result.output:
            self.print_line(result.output)

    def print_line(self, text: str) -> None:
        """Append a line of text to the output pane."""
        self.output.configure(state="normal")
        self.output.insert(tk.END, text + "\n")
        self.output.configure(state="disabled")
        self.output.see(tk.END)


def launch_gui(shell: Shell) -> None:
    """Create the Tk root window and start the event loop.

    Args:
        shell: The Shell instance to drive.
    """
    root = tk.Tk()
    title = f"VFS Shell — {VFS_NAME}"
    ShellWindow(root, shell, title)
    root.mainloop()
