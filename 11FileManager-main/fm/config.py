from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    """Application configuration loaded from config.json."""

    workspace: Path


class ConfigError(Exception):
    """Raised when configuration is missing or invalid."""


class ConfigLoader:
    @staticmethod
    def load(path: Path) -> AppConfig:
        if not path.exists():
            raise ConfigError(f"Config file not found: {path}")

        data = json.loads(path.read_text(encoding="utf-8"))
        if "workspace" not in data:
            raise ConfigError('config.json must contain the key "workspace"')

        ws = Path(str(data["workspace"])).expanduser().resolve()
        ws.mkdir(parents=True, exist_ok=True)
        return AppConfig(workspace=ws)
