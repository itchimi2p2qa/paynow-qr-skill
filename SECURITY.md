# Security

This skill never needs an API key. Do not add one.

## Private data

After setup, `assets/defaults.json` holds the installer mobile and optional
favorites. That file is gitignored. Do not commit it or paste it into a public
issue.

## Payments

PayNow transfers are typically irreversible. The generator will print the
encoded mobile or UEN, amount, and sanitized reference. Read that back before
showing the QR.

Wrong number + send = money gone. The receiving bank shows the registered
account name on scan; use that as the last check.

## Reporting

Open a private report on GitHub if you find a payload or overlay bug that could
encode the wrong payee.
