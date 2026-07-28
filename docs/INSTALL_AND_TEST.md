# Install and Test

## 1. Install SpectraDash

```bash
sudo ./install.sh
```

## 2. Verify preview mode

Open port 8080, configure the location, and click **Render Preview**.

## 3. Enable SPI

```bash
sudo scripts/enable-spi.sh
sudo reboot
```

## 4. Install the official Waveshare driver

```bash
sudo scripts/install-waveshare-driver.sh
```

## 5. Run the vendor test

```bash
sudo scripts/test-waveshare-display.sh
```

## 6. Enable the physical profile

In Setup Wizard choose **Waveshare 13.3 E** and save.

The program enforces at least 180 seconds between physical refreshes.
