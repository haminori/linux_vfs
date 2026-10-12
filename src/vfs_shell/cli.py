"""Параметры командной строки самого эмулятора (не команды шелла)."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from vfs_shell.config import DEFAULT_VFS_NAME, WINDOW_TITLE_PREFIX


@dataclass
class EmulatorConfig:
    """Конфигурация одного запуска эмулятора.

    Attributes:
        vfs_path: Путь к физическому расположению VFS или None.
        script_path: Путь к стартовому скрипту или None.
        vfs_name: Имя VFS для заголовка окна.
    """

    vfs_path: str | None
    script_path: str | None
    vfs_name: str


def build_arg_parser() -> argparse.ArgumentParser:
    """Создать разборщик параметров командной строки эмулятора."""
    parser = argparse.ArgumentParser(
        prog="vfs-shell",
        description="Эмулятор командной строки UNIX-подобной ОС.",
    )
    parser.add_argument(
        "--vfs",
        dest="vfs_path",
        default=None,
        help="путь к физическому расположению VFS",
    )
    parser.add_argument(
        "--script",
        dest="script_path",
        default=None,
        help="путь к стартовому скрипту эмулятора",
    )
    return parser


def derive_vfs_name(vfs_path: str | None) -> str:
    """Получить имя VFS для заголовка окна из пути к VFS.

    Args:
        vfs_path: Путь к VFS или None, если параметр не задан.

    Returns:
        Последний компонент пути либо имя по умолчанию.
    """
    if not vfs_path:
        return DEFAULT_VFS_NAME
    return Path(vfs_path).name or vfs_path


def parse_args(argv: list[str] | None = None) -> EmulatorConfig:
    """Разобрать параметры командной строки.

    Args:
        argv: Список аргументов; по умолчанию ``sys.argv[1:]``.

    Returns:
        Конфигурация запуска.
    """
    namespace = build_arg_parser().parse_args(argv)
    return EmulatorConfig(
        vfs_path=namespace.vfs_path,
        script_path=namespace.script_path,
        vfs_name=derive_vfs_name(namespace.vfs_path),
    )


def window_title(config: EmulatorConfig) -> str:
    """Сформировать заголовок окна, содержащий имя VFS."""
    return f"{WINDOW_TITLE_PREFIX} — {config.vfs_name}"


def format_debug_info(config: EmulatorConfig) -> str:
    """Сформировать отладочный вывод всех заданных параметров.

    Args:
        config: Конфигурация запуска.

    Returns:
        Многострочный текст со значениями всех параметров.
    """
    lines = [
        "[отладка] Параметры запуска эмулятора:",
        f"[отладка]   --vfs         = {config.vfs_path!r}",
        f"[отладка]   --script      = {config.script_path!r}",
        f"[отладка]   имя VFS       = {config.vfs_name!r}",
        f"[отладка]   заголовок окна = {window_title(config)!r}",
    ]
    return "\n".join(lines)
