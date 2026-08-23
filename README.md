# PayNow QR skill

Local Singapore PayNow QR generator for Grok, Claude, and other agents. No API key.

This repository *is* the skill. `SKILL.md` sits at the repo root so installers can point at the address directly.

## Download zip

Ready-made archive of this repo (use this for Claude.ai upload):

https://github.com/itchimi2p2qa/paynow-qr-skill/archive/refs/heads/main.zip

Claude.ai — Settings → Capabilities → Skills → Upload skill → pick that zip.
If the unzipped folder is named `paynow-qr-skill-main`, that is fine as long as `SKILL.md` is inside it.

## Install from this repo

Claude Code / skills CLI

```bash
npx skills add itchimi2p2qa/paynow-qr-skill
```

or

```bash
git clone https://github.com/itchimi2p2qa/paynow-qr-skill.git ~/.claude/skills/paynow-qr
```

Then set *your* PayNow mobile (not anyone else's):

```bash
python3 scripts/setup_payee.py --mobile +65XXXXXXXX
pip install segno pillow
```

A chatbot cannot persist the skill into your account from a URL. You still upload the zip once.

## What it does

- Builds the EMVCo / SGQR payload on the machine
- CRC-16/CCITT-FALSE (`123456789` → `29B1`)
- Mobile, UEN, open amount, bill reference, favorites
- Optional center sticker
- Confirms encoded details before showing the image

PayNow transfers are effectively irreversible. The receiving bank shows the registered account name on scan.

## License

MIT
