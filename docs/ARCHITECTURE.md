# Architecture

SpectraDash is organized around:

- Weather data providers
- Configuration and Setup Wizard
- Layout rendering
- Theme engine
- Display profiles
- Physical display worker
- Scheduler and watchdog
- Diagnostics
- Plugin and theme extension points

Hardware-specific logic should remain isolated behind display profiles.
