# RC18.7: Official NWS alerts (first-stage pilot)

- The forecast continues to come from Open-Meteo.
- For U.S. coordinates, SpectraDash also requests active alerts from `https://api.weather.gov/alerts/active?point=LAT,LON`.
- Official alerts are prioritized by NWS severity. Forecast-derived notices are labeled **ADVISORY**, not official warnings.
- `nws_alert_status` in weather data is `ok`, `unavailable`, `outside-us`, or `disabled`. A failed NWS request does not stop the forecast.
- Settings: enable/disable official NWS alerts separately from the existing display-alert toggle.
- This is a pilot: radar, refresh-rate escalation, alert details page, and comprehensive display-layout tests are deferred until the official-alert integration is tested on hardware.
- **Not a life-safety alerting device**. NWS feeds can fail and e-ink refreshes are periodic. Keep Wireless Emergency Alerts/NOAA Weather Radio for urgent warnings.
