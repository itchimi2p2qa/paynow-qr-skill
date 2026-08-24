# Installer PayNow mobile

The standard QR pays **the installer**. That number must be their registered PayNow mobile.

## Required handshake

1. Ask for the Singapore mobile registered to their PayNow (8 or 9 after `+65`).
2. Save it.

```bash
python3 scripts/setup_payee.py --mobile +6591234567
```

3. Read the number back and ask them to confirm it is the PayNow-registered line.
4. Only after they say yes:

```bash
python3 scripts/setup_payee.py --confirm
```

5. Check any time with:

```bash
python3 scripts/setup_payee.py --show
```

`setup_complete` is true only when `me_mobile` is set **and** `me_mobile_confirmed` is true.

## Rules

- Do not generate a "pay me" / default QR until `setup_complete` is true.
- Do not guess a number from chat history, email, or a previous project.
- Changing `--mobile` clears confirmation. Confirm again.
- Someone else's number, a favorite, or a UEN is an override. It does not replace `me_mobile`.
- `assets/defaults.json` is local and gitignored. Never commit or paste it.
