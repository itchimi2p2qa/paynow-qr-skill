# PayNow QR Code Generator Skill

Generate PayNow QR codes locally without any API key.

## Description

This skill allows chatbots like Grok or Claude to create PayNow QR codes by taking simple instructions from users. It uses the open-source PayNowQR library to handle everything locally.

## Main Use Case

Users describe what they need and the chatbot generates the QR code:
- "Create a PayNow QR for 5.50 to +6591234567 for bubble tea"
- "Make a business PayNow QR for UEN 123456789A amount 100 reference INV-001"
- "PayNow QR 12.00 for me" or "for mum"

## Setup During Installation

When installing the skill, users can configure:
1. A default mobile number (must be +65 followed by 8 digits)
2. Favorite contacts for quick payments

Run `python paynow_skill.py` to set these up interactively.

## Parameters

- recipient_type: "Mobile" or "UEN"
- recipient: phone number (with +65) or UEN
- name: recipient name
- amount: payment amount in SGD
- reference: optional payment reference

## Output

Returns a PNG image of the PayNow QR code.

## Example Use Cases

### Restaurant Bill Split

Take a photo of the bill and say: "Split this 48 dollar bill with 4 friends"
The skill divides the amount and generates a QR code for each person's share.

### Quick Payment to Favorite

After setup, just say: "Create QR for mum 25.00" or "PayNow 8.90 for coffee shop"

## Dependencies

- PayNowQR (pip install PayNowQR)
- qrcode
- pillow

## License

MIT