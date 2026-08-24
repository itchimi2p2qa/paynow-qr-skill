---
name: paynow-qr
description: Generate Singapore PayNow QR codes locally with no API key. Default payee is the installer's registered PayNow mobile after they set and confirm it. Use when the user says set my mobile, confirm my PayNow number, pay me, request SGD, pay another person, pay a UEN, split a bill, add a payment note, or put a center icon sticker such as burger, beer, pizza, or plane on the QR.
metadata:
  version: "1.1.0"
  engine: local-emvco
  default_payee: installer-mobile
  default_expiry: none
  render: local-payload
license: MIT
---

# PayNow QR

Build the EMVCo / SGQR payload on the machine. Do not call an API and do not use an API key.

## Standard payee

Every ordinary request (pay me, create a QR, request 25 dollars) encodes **the installer's registered PayNow mobile**. That is the default. Other people or a UEN only when the user names them.

## Setup before any QR

On first use in a session, run:

```bash
python3 scripts/setup_payee.py --show
```

If `setup_complete` is not true, stop. Do not invent a number and do not generate.

Missing number — ask for the mobile they registered with PayNow. Save it, read it back, wait for an explicit yes, then confirm.

```bash
python3 scripts/setup_payee.py --mobile +6591234567
python3 scripts/setup_payee.py --confirm
```

Number stored but `me_mobile_confirmed` is false — show that exact number and ask "Is this your registered PayNow mobile?" Only `--confirm` after they agree.

Full handshake is in `references/setup.md`.

Optional favorites (nicknames such as mum) never replace the installer number.

```bash
python3 scripts/setup_payee.py --add-favorite mum +6598765432
```

## Choose the payee

- **Default / pay me** — `me_mobile` after setup is complete. Pass `--to-me` (or omit other payee flags).
- **Pay a favorite** — `--favorite mum`. Does not change `me_mobile`.
- **Pay someone else** — `--mobile +6591234567` when they name another number.
- **Business UEN** — `--payment-type uen --uen ... --merchant-name ...`.

Normalize Singapore mobiles to `+65` plus 8 digits starting with 8 or 9.

"For this / reference Y" is the bill note, not the phone number. Letters and digits only, max 25.

If they want to split a total, divide first, then generate one QR for the share. Confirm the share before generating.

## Confirm before showing the image

PayNow transfers are typically irreversible. Always state the encoded mobile or UEN, amount, and sanitized reference before presenting the PNG. The receiving bank shows the registered account name on scan — that is the real typo check.

## Center icon

If they name a sticker, pass `--icon <id>`. See `references/icons.md`.

Default is `--icon none`. The script paints a bundled `assets/icons/<id>.png` on a white circle. No network fetch.

If a stickered code will not scan, regenerate with `--icon none`.

## Generate

Default — installer mobile, after setup is complete

```bash
python3 scripts/generate_paynow_qr.py --amount 250 --reference "Octoberfest Saturday" --to-me --out /tmp/paynow.png
```

Someone else

```bash
python3 scripts/generate_paynow_qr.py --amount 80 --mobile +6591234567 --reference "Lunch" --out /tmp/paynow.png
```

Favorite

```bash
python3 scripts/generate_paynow_qr.py --amount 25 --favorite mum --reference "Dinner" --out /tmp/paynow.png
```

Business UEN

```bash
python3 scripts/generate_paynow_qr.py --payment-type uen --uen 123456789A --merchant-name "ABC Pte Ltd" --amount 100 --reference INV001 --out /tmp/paynow.png
```

Open amount on the installer number

```bash
python3 scripts/generate_paynow_qr.py --to-me --out /tmp/paynow.png
```

Other flags — `--icon burger`, `--expiry none`, `--color 000000`, `--size 300`.

Needs `segno`. Stickers also need `pillow`. `pip install segno pillow` if missing.

## After success

Say who is paid (installer number vs other vs UEN), amount, bill note, and icon. Return the PNG and `qr_string`. Do not reuse an old QR.

Expiry is `none` unless they ask for a timed window.
