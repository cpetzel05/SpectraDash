# RC18.8: Enhanced official weather alert details

- New **Weather Alerts** navigation link opens `/weather-alerts` in the web interface.
- The page requests current NWS active point alerts when loaded, independent of the periodic display refresh.
- Displays the full NWS description and instructions, effective and expiration timestamps, issuing office, urgency and certainty, plus original source link.
- Official alerts remain distinct from local forecast-derived advisories. No layout changes to the e-paper image in this release.
- Network errors are explicitly shown as **unavailable**, never as "no alerts".
- The page is intended for information only, not life safety. Use WEA / NOAA Weather Radio.
- Radar integration is deferred to a separate optional release to avoid introducing external map imagery or service instability into this verified alerts baseline.
