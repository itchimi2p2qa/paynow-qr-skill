# PayNow QR Code Generator Skill

A reusable skill for generating PayNow QR codes in chatbots without requiring an API key.

## Quick Start

```bash
pip install PayNowQR qrcode pillow
python paynow_skill.py
```

## For Chatbot Integration

This skill can be registered as a tool/function in Grok, Claude, or other LLM platforms. Users simply describe what they need and the chatbot generates the QR code locally.

See SKILL.md for full documentation.

## Files

- `paynow_skill.py` - Core QR generation function
- `chatbot_tool.py` - Example integration for chatbots
- `requirements.txt` - Python dependencies
- `SKILL.md` - Full skill documentation