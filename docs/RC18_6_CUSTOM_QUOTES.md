# RC18.6 Global Custom Quote Header

SpectraDash can now place a personal message at the top of every major weather layout.

## Settings

Open **Settings → Style → Custom header quote**. You can enable the feature, enter a fixed quote, or enter up to 20 rotating quotes (one per line). Controls include alignment, size, bold text, quotation marks, palette-safe accent color, and per-layout visibility.

The renderer automatically fits long messages and reserves a dedicated header ribbon. Existing weather content is proportionally inset so the quote cannot cover temperatures, alerts, forecasts, moon art, or system status.

## Rotation

Rotating mode chooses a quote deterministically from the configured list based on the scheduled refresh interval. This means the message can change naturally with display refreshes without requiring internet access.

## E-paper safety

All header colors are mapped to the Spectra six-color palette before physical output.
