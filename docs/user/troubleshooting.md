# Troubleshooting

## Dashboard does not load

- Confirm the SpectraDash service is running.
- Verify the Raspberry Pi IP address.
- Check firewall or network isolation settings.
- Review the application log in Developer Mode.

## Weather data is missing

- Test the weather API in Developer Mode.
- Confirm the API key and location.
- Verify system time and internet access.
- Check provider rate limits or service status.

## Browser shows an old interface

Perform a hard refresh or clear site data. Cached JavaScript and styles can remain after an upgrade.

## Physical display does not update

- Confirm the correct display profile.
- Check power and ribbon connections.
- Run the physical display test.
- Review daemon heartbeat and scheduler status.
- Reboot the Raspberry Pi.

## Colors or layout look wrong

- Confirm the panel model and profile.
- Verify expected resolution and orientation.
- Disable custom themes or plugins.
- Switch to a bundled layout and render again.

## High CPU or memory usage

- Use Lite performance mode.
- Increase the refresh interval.
- Disable animated browser previews.
- Review plugins and custom artwork.

## Support bundle

Create a support bundle from Developer Mode, inspect it for secrets, and attach it to a private or public report as appropriate.
