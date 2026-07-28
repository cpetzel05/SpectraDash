# Roll Back to RC1

## Inspect available tags

```bash
git fetch --all --tags
git tag --list
```

Confirm that `v1.0.0-rc1` exists.

## Preserve the current broken state

```bash
git switch main
git branch archive/sprint8-broken
git push origin archive/sprint8-broken
```

## Restore main to the RC1 tag

```bash
git reset --hard v1.0.0-rc1
git push --force-with-lease origin main
```

## Reinstall on Raspberry Pi

```bash
cd ~/SpectraDash
git fetch --all --tags
git reset --hard origin/main
chmod +x install.sh scripts/*.sh
sudo ./install.sh
```

## Verify

```bash
sudo systemctl status spectradash
curl -I http://127.0.0.1:8080
```

Only use the reset command after verifying that the RC1 tag points to the actual known-good application.
