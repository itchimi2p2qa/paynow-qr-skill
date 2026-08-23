# PayNow QR skill

Local Singapore PayNow QR generator for Grok, Claude, and other agents. No API key.

This repository *is* the skill. `SKILL.md` is at the repo root.

Repo: https://github.com/itchimi2p2qa/paynow-qr-skill

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

Then, once, set the installer's own mobile:

```
python3 scripts/setup_payee.py --mobile +65XXXXXXXX
pip install segno pillow
```

Claude.ai website skills are account settings. A chat cannot write them. There you still do:
Settings → Capabilities → Skills → Upload skill →
https://github.com/itchimi2p2qa/paynow-qr-skill/archive/refs/heads/main.zip

A folder named `paynow-qr-skill-main` is fine if `SKILL.md` is inside it.

## What it does

- Builds the EMVCo / SGQR payload on the machine
- CRC-16/CCITT-FALSE (`123456789` → `29B1`)
- Mobile, UEN, open amount, bill reference, favorites
- Optional center sticker from `assets/icons/`
- Confirms encoded details before showing the image

PayNow transfers are effectively irreversible. The receiving bank shows the registered account name on scan.

Twemoji stickers are CC-BY 4.0 Twitter, Inc.

## License

MIT
