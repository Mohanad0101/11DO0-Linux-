from __future__ import annotations

from pathlib import Path

from .cli import CommandError, CommandRouter
from .config import ConfigLoader
from .ops import FMState, FileManagerOps
from .safety import PathEscapeError, PathGuard


class FileManagerApp:
    def __init__(self, config_path: Path):
        cfg = ConfigLoader.load(config_path)
        self.state = FMState()
        self.guard = PathGuard(cfg.workspace)
        self.ops = FileManagerOps(self.guard, self.state)
        self.router = CommandRouter(self.ops)

    def run_once(self, line: str):
        return self.router.dispatch(line)

    def run_forever(self) -> None:
        print("FileManager started. Type 'help' for commands.")
        while True:
            try:
                line = input("fm> ")
                out = self.run_once(line)

                if out is None:
                    continue

                print(out)
                if out == "QUIT":
                    break

            except (CommandError, PathEscapeError) as e:
                print("ERROR:", e)
            except FileNotFoundError as e:
                print("ERROR: file not found:", e)
            except NotADirectoryError as e:
                print("ERROR: not a directory:", e)
            except IsADirectoryError as e:
                print("ERROR: is a directory:", e)
            except PermissionError as e:
                print("ERROR: permission denied:", e)
            except Exception as e:
                print("ERROR:", type(e).__name__, e)
