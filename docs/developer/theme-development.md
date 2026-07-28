# Theme Development

Themes control visual styling, artwork, typography, scene selection, and layout-specific options.

## Recommended theme contents

```text
themes/example-theme/
├── manifest.json
├── preview.png
├── artwork/
├── icons/
└── README.md
```

## Manifest fields

A theme manifest should identify:

- Name
- ID
- Version
- Author
- License
- Compatible layouts
- Minimum SpectraDash version
- Color palette
- Artwork paths
- Preview image

Example:

```json
{
  "id": "example-theme",
  "name": "Example Theme",
  "version": "1.0.0",
  "author": "Example Author",
  "license": "CC-BY-4.0",
  "layouts": ["weather-station", "premium-lcd"],
  "minimum_spectradash": "1.0.0"
}
```

## Guidelines

- Optimize images for the target resolution.
- Verify colors on the physical display.
- Include license information for all artwork.
- Avoid embedding personal data or secrets.
- Provide a preview image.
- Test light and dark text contrast.
