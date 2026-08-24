# PayNow QR skill

**v1.1.0** &middot; public release &middot; no API key

<img width="292" height="292" alt="Sample PayNow QR" src="https://github.com/user-attachments/assets/fc7c5743-57aa-4a16-8d79-17075b245841" />

Local Singapore PayNow QR generator for Grok, Claude, and other agents.

This repository *is* the skill. `SKILL.md` sits at the repo root.

Not affiliated with MAS, PayNow, NETS, or any bank. Transfers are typically irreversible — confirm the encoded mobile or UEN, amount, and reference before anyone scans.

Repo: https://github.com/itchimi2p2qa/paynow-qr-skill

Latest zip (main): https://github.com/itchimi2p2qa/paynow-qr-skill/archive/refs/heads/main.zip

Tagged zip: https://github.com/itchimi2p2qa/paynow-qr-skill/archive/refs/tags/v1.0.0.zip

## Point an AI at this repo

Paste one of these to Grok, Claude Code, Codex, or Cursor:

```
Install the PayNow QR skill from https://github.com/itchimi2p2qa/paynow-qr-skill
```

```
npx skills add itchimi2p2qa/paynow-qr-skill
```

```
git clone https://github.com/itchimi2p2qa/paynow-qr-skill.git ~/.claude/skills/paynow-qr
```

Then set **and confirm** the installer's registered PayNow mobile. Until that is done, the skill will not generate a default QR — it would not know whose number to encode.

```
python3 scripts/setup_payee.py --mobile +65XXXXXXXX
python3 scripts/setup_payee.py --confirm
python3 scripts/setup_payee.py --show
pip install segno pillow
```

`--show` must report `setup_complete: true`. Changing the number clears confirmation.

The standard payment flow is a QR for **that installer number**. Name another mobile, a favorite, or a UEN only when you want someone else paid.

Claude.ai website skills are account settings. A chat cannot write them. There you still do:
Settings → Capabilities → Skills → Upload skill →
https://github.com/itchimi2p2qa/paynow-qr-skill/archive/refs/heads/main.zip

A folder named `paynow-qr-skill-1.0.0` is fine if `SKILL.md` is inside it.

More setup notes: [IMPORT.md](IMPORT.md) and [references/setup.md](references/setup.md)

## What it does

- Builds the EMVCo / SGQR payload on the machine
- Default payee is the installer's confirmed PayNow mobile
- CRC-16/CCITT-FALSE (`123456789` → `29B1`)
- Mobile, UEN, open amount, bill reference, favorites
- Optional center sticker from `assets/icons/`
- Confirms encoded details before showing the image

PayNow transfers are typically irreversible. The receiving bank shows the registered account name on scan.

## Safety

- No API key. Do not add one.
- `assets/defaults.json` is local and gitignored. Do not commit your number.
- State payee, amount, and reference back before showing the QR.
- Open amount uses initiation tag `11`. Fixed amount uses `12`.

See [SECURITY.md](SECURITY.md) and [NOTICE](NOTICE).

## Center stickers

73 bundled Twemoji icons. Say the name in chat (`put a burger on it`) or pass `--icon burger`.

Default is no sticker (`none` or `paynow`) so the QR stays easiest to scan. If a bank app struggles with a sticker, regenerate without one.

See [references/icons.md](references/icons.md) and the `assets/icons/` folder.

Twemoji stickers are CC-BY 4.0 Twitter, Inc.

## Docs

- [CHANGELOG.md](CHANGELOG.md)
- [SECURITY.md](SECURITY.md)
- [NOTICE](NOTICE)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [IMPORT.md](IMPORT.md)
- [references/setup.md](references/setup.md)
- [references/payload.md](references/payload.md)
- [references/icons.md](references/icons.md)

## License

[MIT](LICENSE)
