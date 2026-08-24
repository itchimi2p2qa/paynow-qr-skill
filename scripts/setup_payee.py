#!/usr/bin/env python3
"""Save and confirm the installer registered PayNow mobile."""

from __future__ import annotations

import argparse
import json
import re
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
    data.setdefault("me_mobile_confirmed", False)
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


def setup_status(data: dict) -> dict:
    me = data.get("me_mobile") or data.get("mobile_number") or ""
    confirmed = bool(me) and bool(data.get("me_mobile_confirmed"))
    return {
        "me_mobile": me or None,
        "me_mobile_confirmed": bool(data.get("me_mobile_confirmed")) if me else False,
        "setup_complete": confirmed,
        "favorites": data.get("favorites") or {},
        "path": str(DEFAULTS_PATH),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Set and confirm the installer registered PayNow mobile"
    )
    parser.add_argument(
        "--mobile",
        help="Installer registered PayNow mobile. Default QR payee after --confirm.",
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Mark me_mobile as confirmed by the user. Required before default QRs.",
    )
    parser.add_argument("--add-favorite", nargs=2, metavar=("NAME", "MOBILE"))
    parser.add_argument("--remove-favorite", metavar="NAME")
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()

    data = load_defaults()
    changed = False

    if args.mobile:
        mobile = normalize_mobile(args.mobile)
        previous = data.get("me_mobile") or ""
        data["me_mobile"] = mobile
        data["mobile_number"] = mobile
        data["payment_type"] = "mobile"
        if previous != mobile:
            data["me_mobile_confirmed"] = False
        changed = True

    if args.confirm:
        me = data.get("me_mobile") or data.get("mobile_number") or ""
        if not me:
            raise SystemExit(
                "SETUP_REQUIRED: set the registered PayNow mobile first. "
                "Run setup_payee.py --mobile +6591234567"
            )
        data["me_mobile"] = normalize_mobile(str(me))
        data["mobile_number"] = data["me_mobile"]
        data["me_mobile_confirmed"] = True
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

    out = setup_status(data)
    out["saved"] = changed

    if not changed and not args.show:
        if not out["setup_complete"]:
            if not out["me_mobile"]:
                raise SystemExit(
                    "SETUP_REQUIRED: no registered PayNow mobile. "
                    "Ask the user for their PayNow number, then "
                    "run setup_payee.py --mobile +65XXXXXXXX and --confirm"
                )
            raise SystemExit(
                "SETUP_UNCONFIRMED: stored %s has not been confirmed. "
                "Read that number back. If they agree, run setup_payee.py --confirm"
                % out["me_mobile"]
            )

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
