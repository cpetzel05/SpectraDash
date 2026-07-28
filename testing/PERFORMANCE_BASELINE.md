# Performance Baseline

Record baseline values on every supported configuration.

| Hardware | Layout | Theme | Render time | Physical refresh | Memory | CPU peak | Temperature | Version |
|---|---|---|---:|---:|---:|---:|---:|---|
| Raspberry Pi Zero 2 W | Weather Station | Default | | | | | | |
| Raspberry Pi Zero 2 W | Premium LCD Dark | Default | | | | | | |
| Raspberry Pi Zero 2 W | Premium LCD Light | Default | | | | | | |

## Regression thresholds

Investigate when a new release causes:

- Browser render time to increase by more than 25%.
- Memory use to increase by more than 20%.
- Physical refresh preparation time to increase by more than 25%.
- Repeated CPU saturation during idle operation.
- Device temperature to rise unexpectedly under the same workload.

These thresholds are investigation triggers, not automatic release failures.
