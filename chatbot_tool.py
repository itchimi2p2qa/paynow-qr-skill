from paynow_skill import generate_paynow_qr, resolve_recipient, validate_mobile, DEFAULT_MOBILE, FAVORITES
import re


def paynow_qr_tool(user_instruction: str) -> dict:
    """
    Chatbot tool: Generate PayNow QR from natural language instruction.
    
    Supports:
    - "Create QR for 12.50 to +6591234567 for lunch"
    - "PayNow QR 5.50 for me" or "for mum"
    - "Split bill 48.00 with 4 friends" (uses default or asks)
    - Business: "UEN 123456789A amount 100 reference INV-001"
    """
    text = user_instruction.lower()
    
    # Extract amount
    amount_match = re.search(r'(\d+\.?\d*)', text)
    amount = float(amount_match.group(1)) if amount_match else 0.0
    
    # Check for split bill use case
    if 'split' in text or 'friends' in text or 'divide' in text:
        split_match = re.search(r'(\d+)\s*(friend|way|people|divide)', text)
        if split_match:
            num_people = int(split_match.group(1))
            if num_people > 0:
                amount = round(amount / num_people, 2)
    
    # Resolve recipient
    recipient = None
    name = None
    recipient_type = "Mobile"
    
    # Try 'for me' or favorite name
    for phrase in ['for me', 'to me', 'myself']:
        if phrase in text:
            recipient, name = resolve_recipient('me')
            break
    
    if not recipient:
        for fav in FAVORITES:
            if fav in text:
                recipient, name = resolve_recipient(fav)
                break
    
    # Extract explicit number or UEN
    if not recipient:
        mobile_match = re.search(r'(\+65\d{8})', user_instruction)
        if mobile_match:
            recipient = mobile_match.group(1)
            name = "Recipient"
        else:
            uen_match = re.search(r'([A-Z0-9]{9,10})', user_instruction.upper())
            if uen_match:
                recipient = uen_match.group(1)
                recipient_type = "UEN"
                name = "Business"
    
    # Extract reference
    ref_match = re.search(r'(?:for|ref|reference)\s+([\w\s-]+)', text)
    reference = ref_match.group(1).strip() if ref_match else ""
    
    if not recipient or not amount:
        return {"error": "Could not parse recipient or amount. Try: 'Create QR for 12.50 to +6591234567 for lunch' or 'PayNow 5.50 for me'"}
    
    try:
        img_bytes = generate_paynow_qr(recipient_type, recipient, name or "Recipient", amount, reference)
        return {
            "success": True,
            "image_bytes": img_bytes,
            "amount": amount,
            "recipient": recipient,
            "name": name,
            "reference": reference
        }
    except Exception as e:
        return {"error": str(e)}


# Example calls for documentation
if __name__ == "__main__":
    examples = [
        "Create a PayNow QR for 5.50 to +6591234567 for bubble tea",
        "PayNow QR 12.00 for me",
        "Create QR for mum 8.90",
        "Split bill 48.00 with 4 friends at the restaurant",
        "Business PayNow for UEN 123456789A amount 100 reference INV-001"
    ]
    for ex in examples:
        print(f"Input: {ex}")
        result = paynow_qr_tool(ex)
        print(f"Result: {result}\n")