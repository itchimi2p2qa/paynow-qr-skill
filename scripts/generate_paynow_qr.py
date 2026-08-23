#!/usr/bin/env python3
"""Generate a PayNow QR locally from an EMVCo / SGQR payload. No API key."""

from __future__ import annotations

import argparse
import json
import re
import sys
from io import BytesIO
from pathlib import Path

from paynow_payload import build_payload, normalize_mobile, sanitize_reference

SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULTS_PATH = SKILL_DIR / "assets" / "defaults.json"
EXAMPLE_PATH = SKILL_DIR / "assets" / "defaults.example.json"
ICONS_DIR = SKILL_DIR / "assets" / "icons"

ICONS = {
    "beer": "\U0001F37A",
    "cheers": "\U0001F37B",
    "wine": "\U0001F377",
    "cocktail": "\U0001F378",
    "tropical": "\U0001F379",
    "champagne": "\U0001F942",
    "whisky": "\U0001F943",
    "sake": "\U0001F376",
    "boba": "\U0001F9CB",
    "coffee": "\u2615",
    "tea": "\U0001F375",
    "pizza": "\U0001F355",
    "burger": "\U0001F354",
    "fries": "\U0001F35F",
    "taco": "\U0001F32E",
    "sushi": "\U0001F363",
    "ramen": "\U0001F35C",
    "hotpot": "\U0001F372",
    "chickenwing": "\U0001F357",
    "steak": "\U0001F969",
    "curry": "\U0001F35B",
    "icecream": "\U0001F366",
    "donut": "\U0001F369",
    "cake": "\U0001F382",
    "chocolate": "\U0001F36B",
    "banana": "\U0001F34C",
    "plane": "\u2708\ufe0f",
    "island": "\U0001F3DD\ufe0f",
    "beach": "\U0001F3D6\ufe0f",
    "luggage": "\U0001F9F3",
    "taxi": "\U0001F695",
    "train": "\U0001F686",
    "ship": "\U0001F6A2",
    "hotel": "\U0001F3E8",
    "map": "\U0001F5FA\ufe0f",
    "ticket": "\U0001F3AB",
    "mountain": "\u26f0\ufe0f",
    "sunset": "\U0001F305",
    "dancer": "\U0001F483",
    "groove": "\U0001F57A",
    "ballet": "\U0001FA70",
    "disco": "\U0001FAA9",
    "party": "\U0001F389",
    "confetti": "\U0001F38A",
    "clapper": "\U0001F3AC",
    "popcorn": "\U0001F37F",
    "mic": "\U0001F3A4",
    "headphones": "\U0001F3A7",
    "notes": "\U0001F3B6",
    "game": "\U0001F3AE",
    "joystick": "\U0001F579\ufe0f",
    "slots": "\U0001F3B0",
    "masks": "\U0001F3AD",
    "magic": "\U0001FA84",
    "circus": "\U0001F3AA",
    "darts": "\U0001F3AF",
    "joy": "\U0001F602",
    "moai": "\U0001F5FF",
    "skull": "\U0001F480",
    "clown": "\U0001F921",
    "frog": "\U0001F438",
    "duck": "\U0001F986",
    "chicken": "\U0001F414",
    "cat": "\U0001F431",
    "dog": "\U0001F436",
    "cool": "\U0001F60E",
    "nerd": "\U0001F913",
    "alien": "\U0001F47D",
    "fire": "\U0001F525",
    "poop": "\U0001F4A9",
    "goat": "\U0001F410",
    "melt": "\U0001FAE0",
    "peek": "\U0001FAE3",
}

ALIASES = {
    "none": "",
    "paynow": "",
    "official": "",
    "officialpaynow": "",
    "nologo": "",
    "hamburger": "burger",
    "beers": "cheers",
    "wineglass": "wine",
    "bubbletea": "boba",
    "milo": "coffee",
    "flight": "plane",
    "airplane": "plane",
    "travel": "plane",
    "karaoke": "mic",
    "movie": "clapper",
    "film": "clapper",
    "music": "notes",
    "doge": "dog",
    "pepe": "frog",
    "octoberfest": "beer",
    "oktoberfest": "beer",
}


def load_defaults() -> dict:
    path = DEFAULTS_PATH if DEFAULTS_PATH.is_file() else EXAMPLE_PATH
    if path.is_file():
        return json.loads(path.read_text())
    return {
        "payment_type": "mobile",
        "me_mobile": "",
        "favorites": {},
        "expiry": "none",
        "qr_size": 300,
        "qr_color": "000000",
    }


def me_mobile(defaults: dict) -> str:
    raw = defaults.get("me_mobile") or defaults.get("mobile_number") or ""
    if not raw or "X" in str(raw):
        raise SystemExit(
            "Installer mobile is not set. Run scripts/setup_payee.py --mobile +6591234567"
        )
    return normalize_mobile(str(raw))


def resolve_favorite(defaults: dict, name: str) -> str:
    favorites = defaults.get("favorites") or {}
    key = re.sub(r"\s+", " ", name).strip().lower()
    if key not in favorites:
        raise SystemExit(
            f"Unknown favorite {name!r}. Known: {', '.join(favorites) or '(none)'}"
        )
    return normalize_mobile(str(favorites[key]))


def resolve_icon(raw: str | None) -> str:
    if not raw:
        return ""
    key = re.sub(r"[^a-z0-9]", "", raw.lower())
    if key in ("", "none", "paynow", "official", "officialpaynow", "nologo"):
        return ""
    if key in ICONS:
        return key
    if key in ALIASES:
        return ALIASES[key] or ""
    for icon_id in ICONS:
        if icon_id in key or key in icon_id:
            return icon_id
    raise SystemExit("Unknown icon %s. See references/icons.md" % raw)


def write_clean_png(qr_string: str, out: Path, hex_color: str, size: int) -> Path:
    try:
        import segno
    except ImportError as exc:
        raise SystemExit("segno is required. Install it with: pip install segno") from exc
    out.parent.mkdir(parents=True, exist_ok=True)
    color = "#" + hex_color.replace("#", "")
    qr = segno.make(qr_string, error="h")
    scale = max(4, int(size / max(qr.symbol_size()[0], 1)))
    qr.save(str(out), scale=scale, border=4, dark=color, light="white")
    return out


def load_sticker(icon_id: str):
    """Load a bundled sticker. No network."""
    if not icon_id:
        return None
    local = ICONS_DIR / f"{icon_id}.png"
    if local.is_file():
        return local.read_bytes()
    try:
        sys.path.insert(0, str(SKILL_DIR / "assets"))
        from icons_pack import ICONS_PNG  # type: ignore

        raw = ICONS_PNG.get(icon_id)
        if not raw:
            return None
        import base64

        return base64.b64decode(raw)
    except Exception:
        return None


def overlay_icon(qr_path: Path, icon_id: str) -> bool:
    if not icon_id:
        return False
    raw = load_sticker(icon_id)
    if not raw:
        return False
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return False

    qr = Image.open(qr_path).convert("RGBA")
    sticker = Image.open(BytesIO(raw)).convert("RGBA")
    width, height = qr.size
    radius = int(min(width, height) * 0.16)
    cx, cy = width // 2, height // 2
    draw = ImageDraw.Draw(qr)
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=(255, 255, 255, 255))
    size = max(16, int(radius * 1.3))
    sticker = sticker.resize((size, size), Image.Resampling.LANCZOS)
    qr.paste(sticker, (cx - size // 2, cy - size // 2), sticker)
    qr.convert("RGB").save(qr_path)
    return True


def main() -> None:
    defaults = load_defaults()
    parser = argparse.ArgumentParser(description="Generate a PayNow QR locally")
    parser.add_argument("--amount", type=float, default=0.0)
    parser.add_argument("--reference", default="")
    parser.add_argument("--to-me", action="store_true")
    parser.add_argument("--favorite", help="Nickname from assets/defaults.json favorites")
    parser.add_argument("--payment-type", choices=["mobile", "uen"])
    parser.add_argument("--mobile", help="Someone else's Singapore mobile")
    parser.add_argument("--uen")
    parser.add_argument("--merchant-name")
    parser.add_argument("--expiry", default="none")
    parser.add_argument("--color")
    parser.add_argument("--size", type=int)
    parser.add_argument("--icon", default="none")
    parser.add_argument("--out", default="paynow-qr.png")
    args = parser.parse_args()

    payment_type = args.payment_type or defaults.get("payment_type") or "mobile"
    mobile = None
    uen = args.uen
    merchant = args.merchant_name or defaults.get("merchant_name") or "NA"
    payee = "other"

    if payment_type == "uen":
        if not uen:
            raise SystemExit("uen is required for payment_type=uen")
        payee = "uen"
    elif args.to_me:
        mobile = me_mobile(defaults)
        payee = "me"
    elif args.favorite:
        mobile = resolve_favorite(defaults, args.favorite)
        payee = f"favorite:{args.favorite.strip().lower()}"
    elif args.mobile:
        mobile = normalize_mobile(args.mobile)
        payee = "other"
    else:
        raise SystemExit("Give --to-me, --favorite NAME, --mobile +65..., or --uen")

    amount = float(args.amount) if args.amount else None
    reference = sanitize_reference(args.reference)
    icon_id = resolve_icon(args.icon)
    color = (args.color or defaults.get("qr_color") or "000000").replace("#", "")
    size = int(args.size or defaults.get("qr_size") or 300)

    qr_string = build_payload(
        payment_type=payment_type,
        amount=amount,
        mobile=mobile,
        uen=uen,
        merchant_name=merchant,
        reference=reference,
        expiry=args.expiry or defaults.get("expiry") or "none",
    )

    out = Path(args.out)
    write_clean_png(qr_string, out, color, size)
    render = "local-payload"
    icon_applied = False
    if icon_id:
        icon_applied = overlay_icon(out, icon_id)
        if icon_applied:
            render = "local-payload+icon"
        else:
            sys.stderr.write(
                "warning: requested icon %r was not applied "
                "(bundled sticker missing or pillow missing). QR is still valid without sticker.\n" % icon_id
            )

    summary = {
        "success": True,
        "payee": payee,
        "mobile_number": mobile,
        "uen": uen,
        "amount": None if amount is None else f"{amount:.2f}",
        "currency": "SGD",
        "payment_type": payment_type,
        "reference": reference or None,
        "expiry": args.expiry or "none",
        "icon_requested": icon_id or "none",
        "icon": icon_id if icon_applied else "none",
        "icon_applied": icon_applied,
        "qr_string": qr_string,
        "image_path": str(out),
        "image_render": render,
        "api_used": False,
    }
    json.dump(summary, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
