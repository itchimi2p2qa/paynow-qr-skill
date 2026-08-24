---
name: paynow-qr
description: Generate Singapore PayNow QR codes locally with no API key. Default payee is the installer's registered PayNow mobile after they set and confirm it. Use when the user says set my mobile, confirm my PayNow number, pay me, request SGD, pay another person, pay a UEN, split a bill, add a payment note, or put a center icon sticker such as burger, beer, pizza, or plane on the QR.
metadata:
  version: "1.1.1"
  engine: local-emvco
  default_payee: installer-mobile
  default_expiry: none
  render: local-payload
  ask_confirm_on_first_use: true
license: MIT
---

# PayNow QR

Build the EMVCo / SGQR payload on the machine. Do not call an API and do not use an API key.

## Standard payee

Every ordinary request (pay me, create a QR, request 25 dollars) encodes **the installer's registered PayNow mobile**. That is the default. Other people or a UEN only when the user names them.

## Ask on install and first use (required)

Do this before the first QR in a conversation. Do not skip it even if a number is already on disk.

1. Run `python3 scripts/setup_payee.py --show`.
2. Speak to the user. Use one of these prompts.

No number yet

> This skill pays your registered PayNow mobile by default. What Singapore number is registered to your PayNow? I will read it back and wait for you to confirm before I save it.

Number stored

> I have +65XXXXXXXX as your PayNow mobile. Is that the number registered to your PayNow? Reply yes to confirm, or send a different number.

3. Wait for an explicit yes, or a replacement number. Do not treat silence, a payment request, or a previous chat as confirmation.
4. Save and confirm only after that yes.

```bash
python3 scripts/setup_payee.py --mobile +6591234567
python3 scripts/setup_payee.py --confirm
```

5. If they send a new number, save it, read it back, and ask again. Changing `--mobile` clears confirmation.

Until `setup_complete` is true, stop. Do not invent a number and do not generate.

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
