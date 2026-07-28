# Roll Back to 8.0.0-rc18.1

Before testing a newer build, create and push a backup branch.

```bash
git switch main
git pull --ff-only origin main
git branch archive/pre-update-$(date +%Y%m%d-%H%M%S)
git push origin --all
```

If a newer build breaks the website or daemon, restore the known-good release tag or commit:

```bash
git fetch --all --tags
git reset --hard 8.0.0-rc18.1
git push --force-with-lease origin main
```

If the release is tagged with a leading `v`, use:

```bash
git reset --hard v8.0.0-rc18.1
```

Reinstall on the Raspberry Pi:

```bash
cd ~/SpectraDash
git fetch --all --tags
git reset --hard origin/main
sudo bash install.sh
```

Verify both services:

```bash
sudo systemctl status spectradash-web --no-pager
sudo systemctl status spectradash-daemon --no-pager
sudo journalctl -u spectradash-web -n 100 --no-pager
sudo journalctl -u spectradash-daemon -n 100 --no-pager
```
