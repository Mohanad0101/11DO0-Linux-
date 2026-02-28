from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List
import shlex

from .ops import FileManagerOps


class CommandError(Exception):
    """Raised for command parsing/usage errors."""


@dataclass(frozen=True)
class CommandSpec:
    usage: str
    min_args: int
    handler: Callable[[List[str]], Any]
    help: str


class CommandRouter:
    """Custom command names (intentionally not duplicating shell commands)."""

    def __init__(self, ops: FileManagerOps):
        self.ops = ops
        self.cmds: Dict[str, CommandSpec] = {
            "help": CommandSpec("help [command]", 0, self._help, "Show help."),
            "where": CommandSpec("where", 0, self._where, "Show virtual current directory."),
            "show": CommandSpec("show", 0, self._show, "List folders and files."),

            "mkd": CommandSpec("mkd <dir>", 1, self._mkd, "Create a folder."),
            "rmd": CommandSpec("rmd <dir>", 1, self._rmd, "Remove an empty folder."),
            "in":  CommandSpec("in <dir>", 1, self._in, "Enter a folder."),
            "out": CommandSpec("out", 0, self._out, "Go up one level."),

            "new":  CommandSpec("new <file>", 1, self._new, "Create an empty file."),
            "put":  CommandSpec('put <file> "<text>"', 2, self._put, "Write text to a file."),
            "read": CommandSpec("read <file>", 1, self._read, "Read a text file."),
            "del":  CommandSpec("del <file>", 1, self._del, "Delete a file."),

            "dup":  CommandSpec("dup <src> <dst>", 2, self._dup, "Copy a file."),
            "move": CommandSpec("move <src> <dst>", 2, self._move, "Move a file."),
            "ren":  CommandSpec("ren <old> <new>", 2, self._ren, "Rename a file."),

            "quit": CommandSpec("quit", 0, self._quit, "Exit."),
        }

    def dispatch(self, line: str) -> Any:
        parts = shlex.split(line)
        if not parts:
            return None

        cmd, *args = parts
        spec = self.cmds.get(cmd)
        if not spec:
            return f"Unknown command: {cmd} (type 'help')"

        if len(args) < spec.min_args:
            raise CommandError(f"Usage: {spec.usage}")

        return spec.handler(args)

    def _help(self, args: List[str]) -> str:
        if args:
            name = args[0]
            spec = self.cmds.get(name)
            if not spec:
                return f"No such command: {name}"
            return f"{spec.usage}\n{spec.help}"

        lines = ["Commands:"]
        for name in sorted(self.cmds.keys()):
            lines.append(f"  {self.cmds[name].usage}")
        lines.append('Tip: put note.txt "hello world"')
        return "\n".join(lines)

    def _where(self, args: List[str]) -> str:
        return self.ops.state.pwd_display()

    def _show(self, args: List[str]) -> Any:
        return self.ops.list_items()

    def _mkd(self, args: List[str]) -> str:
        return self.ops.make_dir(args[0])

    def _rmd(self, args: List[str]) -> str:
        return self.ops.remove_dir(args[0])

    def _in(self, args: List[str]) -> str:
        return self.ops.enter_dir(args[0])

    def _out(self, args: List[str]) -> str:
        return self.ops.up_dir()

    def _new(self, args: List[str]) -> str:
        return self.ops.new_file(args[0])

    def _put(self, args: List[str]) -> str:
        return self.ops.put_text(args[0], " ".join(args[1:]))

    def _read(self, args: List[str]) -> str:
        return self.ops.show_text(args[0])

    def _del(self, args: List[str]) -> str:
        return self.ops.remove_file(args[0])

    def _dup(self, args: List[str]) -> str:
        return self.ops.duplicate_file(args[0], args[1])

    def _move(self, args: List[str]) -> str:
        return self.ops.relocate(args[0], args[1])

    def _ren(self, args: List[str]) -> str:
        return self.ops.rename_file(args[0], args[1])

    def _quit(self, args: List[str]) -> str:
        return "QUIT"
