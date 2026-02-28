from __future__ import annotations

from pathlib import Path


class PathEscapeError(Exception):
    """Raised when a path tries to escape the workspace sandbox."""


class PathGuard:
    """Ensures all resolved paths remain inside the workspace directory."""

    def __init__(self, workspace: Path):
        self.workspace = workspace.resolve()

    def inside(self, user_rel_path: Path) -> Path:
        candidate = (self.workspace / user_rel_path).resolve()
        try:
            candidate.relative_to(self.workspace)
        except ValueError as e:
            raise PathEscapeError(
                f"Forbidden: attempted to escape workspace via '{user_rel_path}'"
            ) from e
        return candidate
