# Import PayNow QR skill (Grok and Claude)

One skill folder. No API key.

The standard QR pays **your registered PayNow mobile**. On install and first use the agent must ask you to confirm that number. Do not skip the question.

## After install

The agent should ask: "What Singapore number is registered to your PayNow?" Then it reads the number back and waits for yes.

1. Save your registered PayNow number

```bash
python3 scripts/setup_payee.py --mobile +6591234567
```

2. Confirm it is the PayNow-registered line (the agent should read it back and wait for yes)

```bash
python3 scripts/setup_payee.py --confirm
python3 scripts/setup_payee.py --show
```

`setup_complete` must be true.

3. Optional favorites (other people, not you)

```bash
python3 scripts/setup_payee.py --add-favorite mum +6598765432
```

4. Render extras

```bash
pip install segno pillow
```

## What to say

- Set my PayNow mobile to +65 9XXX XXXX
- Yes, that is my registered PayNow number
- Pay me 250 for Octoberfest Saturday  (uses your number)
- Create a QR for 80 dollars  (also your number)
- Create a QR for mobile +65 9123 4567 for 80 dollars  (someone else)
- Pay mum 25 for dinner
- Pay me 25 with a burger icon
