# PayNow QR Code Generator Skill

Generate PayNow QR codes locally without any API key.

## Description

This skill allows chatbots like Grok or Claude to create PayNow QR codes by taking simple instructions from users. It uses the open-source PayNowQR library to handle everything locally.

## Usage

Users can say things like:
- "Create a PayNow QR for $5.50 to +6591234567 for bubble tea"
- "Make a business PayNow QR for UEN 123456789A amount 100 reference INV-001"

## Parameters

- recipient_type: "Mobile" or "UEN"
- recipient: phone number (with +65) or UEN
- name: recipient name
- amount: payment amount in SGD
- reference: optional payment reference

## Output

Returns a PNG image of the PayNow QR code.

## Dependencies

- PayNowQR (pip install PayNowQR)
- qrcode
- pillow

## License

MIT