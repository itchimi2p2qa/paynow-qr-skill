# Chatbot Tool Integration Example
# Use this pattern to register the skill with Grok, Claude, or other platforms

from paynow_skill import generate_paynow_qr

def paynow_qr_tool(instruction: str) -> dict:
    """
    Tool function that chatbots can call.
    Parses natural language instructions and generates PayNow QR.
    """
    # Simple parser - in production use a proper NLP parser or LLM extraction
    import re
    
    # Extract amount
    amount_match = re.search(r'\$?([0-9]+\.?[0-9]*)', instruction)
    amount = float(amount_match.group(1)) if amount_match else 0.0
    
    # Extract phone or UEN
    phone_match = re.search(r'(\+65[0-9]{8})', instruction)
    uen_match = re.search(r'UEN\s*([A-Z0-9]+)', instruction, re.IGNORECASE)
    
    if phone_match:
        recipient_type = "Mobile"
        recipient = phone_match.group(1)
    elif uen_match:
        recipient_type = "UEN"
        recipient = uen_match.group(1)
    else:
        return {"error": "Could not find recipient in instruction"}
    
    # Extract name (simple heuristic)
    name_match = re.search(r'to\s+([A-Za-z\s]+?)(?:\s+for|\s+amount|\s+\$)', instruction)
    name = name_match.group(1).strip() if name_match else "Recipient"
    
    # Extract reference
    ref_match = re.search(r'reference\s+([A-Za-z0-9-]+)', instruction, re.IGNORECASE)
    reference = ref_match.group(1) if ref_match else ""
    
    try:
        img_bytes = generate_paynow_qr(recipient_type, recipient, name, amount, reference)
        return {
            "success": True,
            "image_bytes": img_bytes,
            "recipient": recipient,
            "amount": amount,
            "name": name
        }
    except Exception as e:
        return {"error": str(e)}

# Example
if __name__ == "__main__":
    result = paynow_qr_tool("Create a PayNow QR for $5.50 to +6591234567 for bubble tea")
    print(result)