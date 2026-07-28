#!/usr/bin/env bash
systemctl --no-pager status spectradash spectradash-worker || true
echo
journalctl -u spectradash -u spectradash-worker -n 100 --no-pager || true
