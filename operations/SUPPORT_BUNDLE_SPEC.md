# Support Bundle Specification

A support bundle should help diagnose problems without exposing secrets.

## Include

- SpectraDash version
- Git commit when available
- Raspberry Pi model
- Operating system and architecture
- Kernel version
- Display profile
- Active layout and theme
- Refresh interval
- Last successful refresh
- Last refresh duration
- CPU, memory, disk, and temperature
- Service status
- Daemon heartbeat
- Recent sanitized application logs
- Recent sanitized display-worker logs
- Configuration schema version

## Exclude or redact

- API keys
- Passwords
- Wi-Fi credentials
- Exact street address
- Private latitude and longitude
- Public IP address
- Session cookies
- Authentication tokens
- Full environment-variable dumps

## Suggested archive name

```text
spectradash-support-YYYYMMDD-HHMMSS.zip
```

## Retention

Support bundles should be created only when needed and removed after the issue is resolved.
