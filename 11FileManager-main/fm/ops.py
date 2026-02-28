from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List
import shutil

from .safety import PathGuard


@dataclass
class FMState:
    """Holds the current virtual working directory (relative to workspace)."""

    cwd: Path = Path(".")

    def pwd_display(self) -> str:
        rel = self.cwd.as_posix().lstrip("./")
        return "/" + rel if rel else "/"


class FileManagerOps:
    """All file/folder operations. One method per required feature."""

    def __init__(self, guard: PathGuard, state: FMState):
        self.guard = guard
        self.state = state

    def _abs(self, user_path: str) -> Path:
        rel = (self.state.cwd / user_path) if user_path else self.state.cwd
        return self.guard.inside(rel)

    # ---- Folders ----
    def make_dir(self, name: str) -> str:
        p = self._abs(name)
        p.mkdir(parents=False, exist_ok=False)
        return f"OK: created folder '{name}'"

    def remove_dir(self, name: str) -> str:
        p = self._abs(name)
        p.rmdir()  # removes only empty directories
        return f"OK: removed folder '{name}'"

    def enter_dir(self, name: str) -> str:
        p = self._abs(name)
        if not p.is_dir():
            raise NotADirectoryError(name)
        self.state.cwd = p.relative_to(self.guard.workspace)
        return f"OK: entered '{name}'"

    def up_dir(self) -> str:
        if self.state.cwd in (Path("."), Path("")):
            return "OK: already at workspace root"
        parent = self.state.cwd.parent
        self.state.cwd = parent if str(parent) not in ("", ".") else Path(".")
        return "OK: moved up one level"

    def list_items(self) -> Dict[str, List[str]]:
        p = self.guard.inside(self.state.cwd)
        dirs = sorted([x.name for x in p.iterdir() if x.is_dir()])
        files = sorted([x.name for x in p.iterdir() if x.is_file()])
        return {"cwd": self.state.pwd_display(), "dirs": dirs, "files": files}

    # ---- Files ----
    def new_file(self, name: str) -> str:
        p = self._abs(name)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch(exist_ok=False)
        return f"OK: created file '{name}'"

    def put_text(self, name: str, text: str) -> str:
        p = self._abs(name)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return f"OK: wrote {len(text)} chars to '{name}'"

    def show_text(self, name: str) -> str:
        return self._abs(name).read_text(encoding="utf-8")

    def remove_file(self, name: str) -> str:
        p = self._abs(name)
        p.unlink()
        return f"OK: removed file '{name}'"

    def rename_file(self, old: str, new: str) -> str:
        p_old = self._abs(old)
        p_new = self._abs(new)
        p_new.parent.mkdir(parents=True, exist_ok=True)
        p_old.rename(p_new)
        return f"OK: renamed '{old}' -> '{new}'"

    def duplicate_file(self, src: str, dst: str) -> str:
        p_src = self._abs(src)
        if not p_src.is_file():
            raise FileNotFoundError(src)
        p_dst = self._abs(dst)
        p_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p_src, p_dst)
        return f"OK: copied '{src}' -> '{dst}'"

    def relocate(self, src: str, dst: str) -> str:
        p_src = self._abs(src)
        if not p_src.exists():
            raise FileNotFoundError(src)
        p_dst = self._abs(dst)
        p_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(p_src), str(p_dst))
        return f"OK: moved '{src}' -> '{dst}'"
