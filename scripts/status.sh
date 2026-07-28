#!/usr/bin/env bash
systemctl --no-pager status spectradash || true
echo
journalctl -u spectradash -n 80 --no-pager || true
