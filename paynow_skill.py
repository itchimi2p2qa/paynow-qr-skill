from paynowqr import PayNowQR
import io
from PIL import Image

def generate_paynow_qr(recipient_type: str, recipient: str, name: str, amount: float, reference: str = "") -> bytes:
    """
    Generate a PayNow QR code.
    
    Args:
        recipient_type: "Mobile" or "UEN"
        recipient: Phone number with +65 or UEN
        name: Recipient name
        amount: Amount in SGD
        reference: Optional payment reference
    
    Returns:
        PNG image as bytes
    """
    qr = PayNowQR(recipient_type, recipient, name, amount, reference)
    
    # Save to bytes buffer
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()

# Example usage for chatbot integration
if __name__ == "__main__":
    # Personal mobile example
    img_bytes = generate_paynow_qr("Mobile", "+6591234567", "John Lim", 5.50, "Bubble Tea")
    print(f"Generated QR code: {len(img_bytes)} bytes")
    
    # Business UEN example
    img_bytes = generate_paynow_qr("UEN", "123456789A", "ABC Pte Ltd", 100.00, "INV-001")
    print(f"Generated business QR: {len(img_bytes)} bytes")