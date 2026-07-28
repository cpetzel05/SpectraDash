# Uninstall

Keep configuration and cached data:

```bash
sudo bash /opt/spectradash/uninstall.sh
```

Remove application data as well:

```bash
sudo bash /opt/spectradash/uninstall.sh --purge-data
```

Remove application data and the shared Waveshare driver checkout:

```bash
sudo bash /opt/spectradash/uninstall.sh --purge-data --remove-driver
```

The script stops and disables SpectraDash services before removing files.
