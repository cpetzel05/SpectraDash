# Architecture

SpectraDash is organized around several major subsystems.

## Web application

Provides configuration, previews, setup, diagnostics, theme management, plugin management, and developer tools.

## Weather services

Normalize provider-specific responses into a shared internal model used by all layouts.

## Rendering engine

Builds the dashboard image from weather data, layout rules, themes, artwork, astronomy, alerts, and environmental panels.

## Hardware worker

Owns communication with the physical display and should isolate slow or failure-prone hardware operations from the web process.

## Scheduler and watchdog

Coordinate refresh timing, detect stale processes, and recover from failures.

## Display profiles

Describe resolution, color handling, driver behavior, and refresh characteristics.

## Themes and plugins

Extend appearance and behavior without requiring changes to the core application.

## Design principles

- Shared data model across layouts
- Hardware abstraction
- Safe defaults
- Observable runtime state
- Graceful degradation
- Backward-compatible configuration
