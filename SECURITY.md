# Security

This skill never needs an API key. Do not add one.

## Private data

After setup, `assets/defaults.json` holds the installer registered PayNow
mobile, whether they confirmed it, and optional favorites. That file is
gitignored. Do not commit it or paste it into a public issue.

## Payments

The default QR pays the installer number. Wrong number + send = money gone.

Do not generate a default / pay-me QR until `setup_complete` is true.

The generator prints the encoded mobile or UEN, amount, and sanitized
reference. Read that back before showing the QR. The receiving bank shows
the registered account name on scan; use that as the last check.

## Reporting

Open a private report on GitHub if you find a payload or overlay bug that could
encode the wrong payee.
