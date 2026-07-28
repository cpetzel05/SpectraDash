# SpectraDash Plugin SDK

A plugin is a ZIP containing `manifest.json` and a Python entry file. Install it from **Plugins** in the web interface, then add its widget in **Screen Designer**.

## manifest.json

```json
{
  "id": "hello-weather",
  "name": "Hello Weather",
  "version": "1.0.0",
  "author": "Your Name",
  "description": "A simple dashboard widget.",
  "widget_name": "Hello Weather",
  "entry": "plugin.py",
  "default_size": [4, 3]
}
```

## Entry point

Export a function:

```python
def render(image, box, context):
    ...
```

`image` is the full Pillow image, `box` is `(x1, y1, x2, y2)`, and `context` contains `weather`, `config`, `system`, `theme`, `theme_colors`, and the six-color `palette`.

Plugins execute as Python code under the SpectraDash service account. Only install trusted plugins.
