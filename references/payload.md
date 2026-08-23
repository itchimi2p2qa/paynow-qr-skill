# Local PayNow payload

No network call. Script `scripts/paynow_payload.py` builds the EMVCo string.

CRC is CRC-16/CCITT-FALSE. Check vector `123456789` must hash to `29B1`.

## Mobile template

- 00 Payload format `01`
- 01 Point of initiation `12` (dynamic)
- 26 SG.PAYNOW
  - 00 `SG.PAYNOW`
  - 01 proxy type `0` mobile or `2` UEN
  - 02 proxy value (`+65` plus 8 digits, or UEN)
  - 03 editable `1` if amount omitted else `0`
  - 04 expiry `YYYYMMDD` only when the user asked for a window
- 52 MCC `0000`
- 53 currency `702`
- 54 amount `12.50` omitted when open
- 58 country `SG`
- 59 merchant name or `NA`
- 60 city `Singapore`
- 62 additional / 01 bill number (reference, letters and digits, max 25)
- 63 CRC 4 hex

## Do not ship

- API keys or remote generate endpoints
- branded third-party PNGs as the scan target
