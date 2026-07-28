# Branching Strategy

## Protected baseline

`main` should contain only the latest known-good build.

## Integration

Use `develop` for tested feature integration.

## Feature branches

Examples:

```text
feature/location-search
feature/weather-icons
feature/aqi-uv
feature/astronomy
feature/themes
feature/waveshare-driver
```

Never combine unrelated features into one branch.
