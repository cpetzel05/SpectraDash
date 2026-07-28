# Recovery Runbook

## When the website stops loading

1. Check the service:

```bash
sudo systemctl status spectradash
```

2. Read recent logs:

```bash
sudo journalctl -u spectradash -n 100 --no-pager
```

3. Confirm the local port:

```bash
curl -I http://127.0.0.1:8080
```

4. Return to the RC1 baseline:

```bash
cd ~/SpectraDash
git fetch --all --tags
git reset --hard v1.0.0-rc1
sudo ./install.sh
```

5. Confirm the service and dashboard before adding any new feature.
