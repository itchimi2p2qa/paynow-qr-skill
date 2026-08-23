# PayNow QR skill

Local Singapore PayNow QR generator for Grok, Claude, and other agents. No API key.

This repository *is* the skill. `SKILL.md` sits at the repo root so installers can point at the address directly.

## Install from this repo

Claude Code / skills CLI

```bash
npx skills add itchimi2p2qa/paynow-qr-skill
```

or

```bash
git clone https://github.com/itchimi2p2qa/paynow-qr-skill.git ~/.claude/skills/paynow-qr
```

Claude.ai chat — Settings, Capabilities, Skills, upload a zip of this folder.

Grok — give the agent this URL and ask it to install the skill from the repo.

Then set *your* PayNow mobile (not anyone else's):

```bash
python3 scripts/setup_payee.py --mobile +65XXXXXXXX
pip install segno pillow
```

## What it does

- Builds the EMVCo / SGQR payload on the machine
- CRC-16/CCITT-FALSE (`123456789` → `29B1`)
- Mobile, UEN, open amount, bill reference, favorites
- Optional center sticker
- Confirms encoded details before showing the image

PayNow transfers are effectively irreversible. The receiving bank shows the registered account name on scan.

## License

MIT
