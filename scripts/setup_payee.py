#!/usr/bin/env python3
"""Save installer PayNow mobile and optional favorite nicknames."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULTS_PATH = SKILL_DIR / "assets" / "defaults.json"
EXAMPLE_PATH = SKILL_DIR / "assets" / "defaults.example.json"
MOBILE_RE = re.compile(r"^\+65[89]\d{7}$")


def normalize_mobile(raw: str) -> str:
    digits = re.sub(r"\D", "", raw or "")
    if digits.startswith("65") and len(digits) == 10:
        digits = digits[2:]
    if len(digits) == 8 and digits[0] in "89":
        return "+65" + digits
    raise SystemExit(
        "Need a Singapore mobile starting with 8 or 9, e.g. +6591234567 or 91234567"
    )


def load_defaults() -> dict:
    path = DEFAULTS_PATH if DEFAULTS_PATH.is_file() else EXAMPLE_PATH
    data = json.loads(path.read_text()) if path.is_file() else {}
    data.setdefault("payment_type", "mobile")
    data.setdefault("me_mobile", "")
    data.setdefault("mobile_number", data.get("me_mobile", ""))
    data.setdefault("favorites", {})
    data.setdefault("uen", "")
    data.setdefault("merchant_name", "")
    data.setdefault("expiry", "none")
    data.setdefault("qr_size", 300)
    data.setdefault("qr_color", "000000")
    return data


def save_defaults(data: dict) -> dict:
    DEFAULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    DEFAULTS_PATH.write_text(json.dumps(data, indent=2) + "\n")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Configure PayNow payee defaults")
    parser.add_argument("--mobile", help="Installer mobile used when the user says pay me")
    parser.add_argument("--add-favorite", nargs=2, metavar=("NAME", "MOBILE"))
    parser.add_argument("--remove-favorite", metavar="NAME")
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()

    data = load_defaults()
    changed = False

    if args.mobile:
        mobile = normalize_mobile(args.mobile)
        data["me_mobile"] = mobile
        data["mobile_number"] = mobile
        data["payment_type"] = "mobile"
        changed = True

    if args.add_favorite:
        name, number = args.add_favorite
        key = re.sub(r"\s+", " ", name).strip().lower()
        if not key:
            raise SystemExit("Favorite name cannot be empty")
        data.setdefault("favorites", {})
        data["favorites"][key] = normalize_mobile(number)
        changed = True

    if args.remove_favorite:
        key = args.remove_favorite.strip().lower()
        data.setdefault("favorites", {}).pop(key, None)
        changed = True

    if changed:
        save_defaults(data)

    me = data.get("me_mobile") or data.get("mobile_number") or ""
    out = {
        "me_mobile": me or None,
        "favorites": data.get("favorites") or {},
        "path": str(DEFAULTS_PATH),
        "saved": changed,
    }
    if args.show or not changed:
        if not me and not out["favorites"] and not args.show:
            raise SystemExit(
                "me_mobile is not set. Run setup_payee.py --mobile +6591234567"
            )
    json.dump(out, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
