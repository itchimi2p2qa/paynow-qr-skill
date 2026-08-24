# Contributing

Keep the skill local. No API keys, no network fetch for stickers or payloads.

- Payload rules live in `scripts/paynow_payload.py` and `references/payload.md`
- Installer identity lives in gitignored `assets/defaults.json` (`me_mobile`, `me_mobile_confirmed`)
- Setup handshake is documented in `references/setup.md` and `SKILL.md`
- Stickers live only in `assets/icons/<id>.png`
- Do not track `assets/defaults.json`
- Confirm CRC vector `123456789` → `29B1` after payload changes
- Confirm a stickered QR still scans at error-correction H
- Bump `metadata.version` in `SKILL.md` and add a `CHANGELOG.md` entry on user-visible changes
