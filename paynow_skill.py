from paynowqr import PayNowQR
import io
from PIL import Image
import re

# User configuration - set during skill installation
DEFAULT_MOBILE = None  # e.g. "+6591234567"
FAVORITES = {}  # e.g. {"mum": "+6598765432", "coffee shop": "+6512345678"}

def validate_mobile(number: str) -> bool:
    """Check if number is +65 followed by 8 digits."""
    return bool(re.match(r'^\+65\d{8}$', number))

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
    if recipient_type == "Mobile" and not validate_mobile(recipient):
        raise ValueError("Mobile number must be +65 followed by 8 digits")
    
    qr = PayNowQR(recipient_type, recipient, name, amount, reference)
    
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()


def setup_skill():
    """Interactive setup for default number and favorites."""
    global DEFAULT_MOBILE, FAVORITES
    
    print("=== PayNow QR Skill Setup ===")
    
    # Default mobile number
    while True:
        default = input("Enter your default mobile number (with +65, or press Enter to skip): ").strip()
        if not default:
            break
        if validate_mobile(default):
            DEFAULT_MOBILE = default
            print(f"Default set to {default}")
            break
        else:
            print("Invalid format. Must be +65 followed by 8 digits, e.g. +6591234567")
    
    # Favorites
    print("\nAdd favorite contacts (press Enter on name to finish):")
    while True:
        name = input("Favorite name: ").strip().lower()
        if not name:
            break
        number = input(f"Mobile number for {name} (with +65): ").strip()
        if validate_mobile(number):
            FAVORITES[name] = number
            print(f"Added {name}")
        else:
            print("Invalid format, skipping.")
    
    print(f"\nSetup complete. Default: {DEFAULT_MOBILE or 'none'}, Favorites: {list(FAVORITES.keys()) or 'none'}")


def resolve_recipient(user_input: str):
    """Resolve 'me', 'for me', or favorite name to actual number."""
    user_input = user_input.lower().strip()
    
    if user_input in ("me", "for me", "myself") and DEFAULT_MOBILE:
        return DEFAULT_MOBILE, "Me"
    
    if user_input in FAVORITES:
        return FAVORITES[user_input], user_input.title()
    
    return None, None


# Example usage
if __name__ == "__main__":
    setup_skill()
    
    # Test resolution
    if DEFAULT_MOBILE:
        num, nm = resolve_recipient("for me")
        print(f"'for me' resolves to: {num} ({nm})")
    
    for fav in FAVORITES:
        num, nm = resolve_recipient(fav)
        print(f"'{fav}' resolves to: {num} ({nm})")