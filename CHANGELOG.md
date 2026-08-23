# Changelog

## 1.0.0 — 2026-08-23

First public release.

- Local EMVCo / SGQR PayNow payload (no API key)
- CRC-16/CCITT-FALSE (`123456789` → `29B1`)
- Mobile (`+65` + 8 digits), UEN, open amount, bill reference, favorites
- Initiation tag `11` for open amount, `12` for a fixed amount
- 73 bundled Twemoji center stickers in `assets/icons/`
- Honest `icon_applied` reporting
- Setup script writes a local `defaults.json` that is gitignored
