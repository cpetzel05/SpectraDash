# RC19.1 Graphics Lab fix

The old RC19.0 icon supersampling produced almost indistinguishable results after six-color quantization. RC19.1 also varies the underlying premium icon artwork detail by quality level (cloud texture and sun rays), adds a magnified comparison crop, and offers an explicit Apply and Refresh Physical Display button.

The Apply button requires confirmation, checks physical display enablement and daemon health, persists render_quality, and queues the existing physical refresh command. It does not perform direct hardware I/O in Flask.

Test first on Pi 4. Graphics Lab renders all three previews and may take several minutes on Pi Zero 2 W. The six-ink panel cannot show continuous RGB gradients; changes remain palette-limited.
