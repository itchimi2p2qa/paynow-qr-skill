# Installer PayNow mobile

The standard QR pays **the installer**. That number must be their registered PayNow mobile.

## Ask on install and first use

The agent must ask. Do not assume. Do not generate first.

**Install / no number**

Ask: "This skill pays your registered PayNow mobile by default. What Singapore number is registered to your PayNow?"

**First usage / number already stored**

Ask: "I have +65XXXXXXXX as your PayNow mobile. Is that the number registered to your PayNow?"

Wait for yes (or a different number). A request like "pay me 25" is not confirmation.

## Required handshake

1. `python3 scripts/setup_payee.py --show`
2. Ask using the prompts above.
3. Save the number they gave.

```bash
python3 scripts/setup_payee.py --mobile +6591234567
```

4. Read that exact number back. Wait for yes.
5. Only then:

```bash
python3 scripts/setup_payee.py --confirm
```

`setup_complete` is true only when `me_mobile` is set **and** `me_mobile_confirmed` is true.

## Rules

- Do not generate a "pay me" / default QR until `setup_complete` is true.
- Do not guess a number from chat history, email, or a previous project.
- Changing `--mobile` clears confirmation. Ask and confirm again.
- Someone else's number, a favorite, or a UEN is an override. It does not replace `me_mobile`.
- `assets/defaults.json` is local and gitignored. Never commit or paste it.
