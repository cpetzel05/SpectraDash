#!/usr/bin/env bash
systemctl --no-pager status spectradash || true
journalctl -u spectradash -n 50 --no-pager || true
