from __future__ import annotations

import json
from pathlib import Path

from fm.app import FileManagerApp


def ensure_default_config(cfg_path: Path) -> None:
    """Create a default config.json if it does not exist."""
    if cfg_path.exists():
        return
    cfg_path.write_text(
        json.dumps({"workspace": str((Path.cwd() / "workspace").resolve())}, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    cfg_path = Path("config.json")
    ensure_default_config(cfg_path)
    FileManagerApp(cfg_path).run_forever()


if __name__ == "__main__":
    main()
