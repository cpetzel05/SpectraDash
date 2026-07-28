# Plugin Development

Plugins extend SpectraDash with data sources, panels, integrations, actions, or services.

## Plugin goals

- Clear lifecycle
- Explicit permissions
- Safe failure behavior
- Version compatibility
- Discoverable configuration
- Isolated logs

## Suggested structure

```text
plugins/example-plugin/
├── manifest.json
├── plugin.py
├── templates/
├── static/
├── tests/
└── README.md
```

## Manifest fields

- ID
- Name
- Version
- Author
- License
- Entry point
- Minimum SpectraDash version
- Configuration schema
- Declared capabilities

## Security

Plugins run with the permissions of the SpectraDash process unless sandboxing is introduced. Install only trusted plugins and review their source code.

## Reliability

A plugin must not block dashboard rendering indefinitely. Use timeouts, catch provider failures, and return safe fallback data.
