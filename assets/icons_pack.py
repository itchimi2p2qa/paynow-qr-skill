# Bundled Twemoji 14.0.2 72x72 PNGs. CC-BY 4.0 Twitter, Inc.
from __future__ import annotations

import importlib.util
from pathlib import Path

ICONS_PNG: dict[str, str] = {}
_DIR = Path(__file__).resolve().parent / "icon_data"
if _DIR.is_dir():
    for path in sorted(_DIR.glob("*.py")):
        if path.name.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(f"paynow_icon_{path.stem}", path)
        if spec is None or spec.loader is None:
            continue
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        ICONS_PNG.update(getattr(mod, "ICONS_PNG", {}))
