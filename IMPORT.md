# Import PayNow QR skill (Grok and Claude)

One skill folder. No API key.

## After install

1. Your number (used only when you say pay me)

```bash
python3 scripts/setup_payee.py --mobile +6591234567
```

2. Optional favorites

```bash
python3 scripts/setup_payee.py --add-favorite mum +6598765432
```

3. Render extras

```bash
pip install segno pillow
```

## What to say

- Pay me 250 for Octoberfest Saturday
- Create a QR for mobile +65 9123 4567 for 80 dollars
- Pay 40 to 91234567 for lunch
- Pay mum 25 for dinner
- Pay me 25 with a burger icon
- QR for pizza night, 60 dollars, beer icon
- Split 48 dollars with 4 friends (example — generate one QR for 12.00)
