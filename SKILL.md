---
name: paynow-qr
description: Generate Singapore PayNow QR codes locally with no API key. Use when the user says pay me, set my mobile, add a favorite, pay another person, create a QR for a phone number or UEN, request SGD, split a bill, add a payment note, or put a center icon sticker such as burger, beer, pizza, or plane on the QR.
metadata:
  version: "2.2"
  engine: local-emvco
  default_expiry: none
  render: local-payload
license: MIT
---

# PayNow QR

Build the EMVCo / SGQR payload on the machine. Do not call an API and do not use an API key.

## Setup (who "me" is)

Whoever installs this skill must set their own PayNow mobile once.

```bash
python3 scripts/setup_payee.py --mobile +6591234567
```

That writes `assets/defaults.json` field `me_mobile`. Use it only when the user says pay me / paying me / send it to me.

If `me_mobile` is missing, ask them to run setup. Do not guess a number.

Show current owner and favorites with `python3 scripts/setup_payee.py --show`.

Optional favorites for nicknames such as mum or coffee shop

```bash
python3 scripts/setup_payee.py --add-favorite mum +6598765432
```

## Choose the payee

- **Pay me** — use `me_mobile`. Do not ask for a number if it is already set.
- **Pay a favorite** — resolve the nickname from `favorites`. Do not overwrite `me_mobile`.
- **Pay someone else** — use the number they gave. Do not overwrite `me_mobile`.
- **Business UEN** — use `--payment-type uen --uen ... --merchant-name ...`.

Normalize Singapore mobiles to `+65` plus 8 digits starting with 8 or 9.

"For this / reference Y" is the PayNow bill note, not the phone number. Strip that note to letters and digits, max 25.

If the user wants to split a total (example only, not the main flow), divide first, then generate one QR for the share amount. Confirm the share before generating.

## Confirm before showing the image

PayNow transfers are effectively irreversible. State the encoded mobile or UEN, amount, and sanitized reference back to the user before presenting the PNG. The receiving bank shows the registered account name on scan — that is the real typo check.

## Center icon

If the user names a sticker (burger, beer, pizza, plane, karaoke, party, doge, and so on), pass `--icon <id>`. Ids and speech mapping are in `references/icons.md`.

Default is `--icon none` (no sticker, easiest scan). `paynow` also means no extra sticker.

The script encodes `qr_string` first, then paints a small bundled sticker from `assets/icons/<id>.png` on a white circle. Do not fetch stickers from the network.

If a stickered code will not scan, regenerate with `--icon none`.

## Generate

Pay me, burger sticker

```bash
python3 scripts/generate_paynow_qr.py --amount 250 --reference "Octoberfest Saturday" --to-me --icon burger --out /tmp/paynow.png
```

Pay another mobile, beer sticker

```bash
python3 scripts/generate_paynow_qr.py --amount 80 --mobile +6591234567 --reference "Lunch" --icon beer --out /tmp/paynow.png
```

Pay a favorite

```bash
python3 scripts/generate_paynow_qr.py --amount 25 --favorite mum --reference "Dinner" --out /tmp/paynow.png
```

Business UEN

```bash
python3 scripts/generate_paynow_qr.py --payment-type uen --uen 123456789A --merchant-name "ABC Pte Ltd" --amount 100 --reference INV001 --out /tmp/paynow.png
```

Open amount (payer types the amount in the bank app)

```bash
python3 scripts/generate_paynow_qr.py --to-me --out /tmp/paynow.png
```

Other flags — `--expiry none`, `--color 000000`, `--size 300`.

Needs `segno`. Sticker overlay also needs `pillow`. Install with `pip install segno pillow` if missing.

## After success

State who gets paid, amount, sanitized bill note, and which icon was applied. Return the PNG and `qr_string`. Do not reuse an old QR.

Expiry is `none` unless the user asks for a timed window.
