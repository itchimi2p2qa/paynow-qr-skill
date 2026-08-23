# PayNow QR Code Generator Skill

A reusable skill for generating PayNow QR codes in chatbots without requiring an API key.

## Quick Start

```bash
pip install PayNowQR qrcode pillow
python paynow_skill.py
```

## Setup

During first run, you'll be asked for:
- Your default mobile number (validated as +65 followed by 8 digits)
- Any favorite contacts for quick access

## For Chatbot Integration

This skill can be registered as a tool/function in Grok, Claude, or other LLM platforms. Users simply describe what they need and the chatbot generates the QR code locally.

See SKILL.md for full documentation and examples.

## Example Commands

- "Create a PayNow QR for 5.50 to +6591234567 for bubble tea"
- "PayNow QR 12.00 for me"
- "Create QR for mum 8.90"
- "Split bill 48.00 with 4 friends at the restaurant"
- "Business PayNow for UEN 123456789A amount 100 reference INV-001"

## Files

- `paynow_skill.py` - Core QR generation with setup and validation
- `chatbot_tool.py` - Example integration for chatbots
- `requirements.txt` - Python dependencies
- `SKILL.md` - Full skill documentation