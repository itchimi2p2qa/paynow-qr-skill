#!/usr/bin/env python3
"""Build an EMVCo / SGQR PayNow payload locally. No API."""

from __future__ import annotations

import re
from datetime import datetime, timedelta


def crc16_ccitt_false(data: str) -> int:
    crc = 0xFFFF
    for ch in data.encode("ascii"):
        crc ^= ch << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


def crc_hex(data: str) -> str:
    return f"{crc16_ccitt_false(data):04X}"


def tlv(tag: str, value: str) -> str:
    if value is None:
        return ""
    value = str(value)
    if not value:
        return ""
    return f"{tag}{len(value):02d}{value}"


def sanitize_reference(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"[^a-zA-Z0-9]", "", value)[:25]


def normalize_mobile(raw: str) -> str:
    compact = re.sub(r"\s+", "", raw or "")
    digits = re.sub(r"\D", "", compact)
    if digits.startswith("65") and len(digits) == 10:
        digits = digits[2:]
    if len(digits) == 8 and digits[0] in "89":
        return "+65" + digits
    raise ValueError(
        "Need a Singapore mobile starting with 8 or 9, e.g. +6591234567 or 91234567"
    )


def normalize_uen(raw: str) -> str:
    uen = re.sub(r"[^A-Za-z0-9]", "", raw or "").upper()
    if not (8 <= len(uen) <= 10):
        raise ValueError("UEN must be 8 to 10 letters or digits")
    return uen


def expiry_yyyymmdd(spec: str | None) -> str:
    if not spec or spec == "none":
        return ""
    mapping = {"1h": 1, "2h": 2, "6h": 6, "12h": 12, "24h": 24}
    hours = mapping.get(spec)
    if hours is None:
        raise ValueError("expiry must be none, 1h, 2h, 6h, 12h, or 24h")
    return (datetime.utcnow() + timedelta(hours=hours)).strftime("%Y%m%d")


def build_payload(
    *,
    payment_type: str,
    amount: float | None,
    mobile: str | None = None,
    uen: str | None = None,
    merchant_name: str | None = None,
    reference: str | None = None,
    expiry: str | None = "none",
    editable: bool | None = None,
) -> str:
    payment_type = (payment_type or "mobile").lower()
    if payment_type not in ("mobile", "uen"):
        raise ValueError("payment_type must be mobile or uen")

    if payment_type == "mobile":
        proxy_type = "0"
        proxy_value = normalize_mobile(mobile or "")
    else:
        proxy_type = "2"
        proxy_value = normalize_uen(uen or "")

    amount_str = ""
    if amount is not None and float(amount) > 0:
        amount_str = f"{float(amount):.2f}"

    if editable is None:
        editable = amount_str == ""
    edit_flag = "1" if editable else "0"

    expiry_date = expiry_yyyymmdd(expiry)
    ref = sanitize_reference(reference)
    merchant = (merchant_name or "NA")[:25] or "NA"

    paynow = (
        tlv("00", "SG.PAYNOW")
        + tlv("01", proxy_type)
        + tlv("02", proxy_value)
        + tlv("03", edit_flag)
        + tlv("04", expiry_date)
    )

    additional = tlv("01", ref) if ref else ""

    payload = (
        tlv("00", "01")
        + tlv("01", "12")
        + tlv("26", paynow)
        + tlv("52", "0000")
        + tlv("53", "702")
        + tlv("54", amount_str)
        + tlv("58", "SG")
        + tlv("59", merchant)
        + tlv("60", "Singapore")
        + (tlv("62", additional) if additional else "")
        + "6304"
    )
    return payload + crc_hex(payload)


if __name__ == "__main__":
    # ISO/IEC 13239 CRC-16/CCITT-FALSE check vector
    assert crc_hex("123456789") == "29B1", crc_hex("123456789")
    sample = build_payload(
        payment_type="mobile",
        amount=5.5,
        mobile="+6591234567",
        reference="BubbleTea",
    )
    print(sample)
    print("crc_ok", sample[-4:] == crc_hex(sample[:-4]))
