# Changelog

## 1.1.1 — 2026-08-24

Install and first usage must ask the user to confirm their registered PayNow mobile before any QR.

- Scripted prompts in `SKILL.md` and `references/setup.md`
- A payment request is not treated as confirmation
- Changing the number still clears confirmation and asks again

## 1.1.0 — 2026-08-24

Installer PayNow mobile is required and must be confirmed.

- Default QR payee is the installer's registered mobile (`me_mobile`)
- `setup_payee.py --confirm` sets `me_mobile_confirmed`
- `--show` reports `setup_complete` only when the number is set and confirmed
- Generator refuses default / `--to-me` QRs until setup is complete
- Changing `--mobile` clears confirmation
- Docs — README, IMPORT, SKILL, SECURITY, CONTRIBUTING, `references/setup.md`

## 1.0.0 — 2026-08-23

First public release.

- Local EMVCo / SGQR PayNow payload (no API key)
- CRC-16/CCITT-FALSE (`123456789` → `29B1`)
- Mobile (`+65` + 8 digits), UEN, open amount, bill reference, favorites
- Initiation tag `11` for open amount, `12` for a fixed amount
- 73 bundled Twemoji center stickers in `assets/icons/`
- Honest `icon_applied` reporting
- Setup script writes a local `defaults.json` that is gitignored
