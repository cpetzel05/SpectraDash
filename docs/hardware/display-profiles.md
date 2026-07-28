# Display Profiles

Display profiles isolate hardware-specific behavior from layout and weather logic.

A profile should define:

- Human-readable name
- Internal identifier
- Width and height
- Orientation
- Color capabilities
- Driver module or adapter
- Refresh behavior
- Image mode and conversion
- Recommended refresh interval
- Full and partial refresh support

## Profile design goals

- Avoid hard-coded panel checks in layouts.
- Keep driver imports lazy when possible.
- Provide clear validation errors.
- Include a safe test pattern.
- Document exact hardware and wiring.

## Community profiles

Community-submitted profiles should include photos, test results, operating-system version, and limitations.
