#!/usr/bin/env bash
set -euo pipefail
STATUS=/var/lib/spectradash/status.json
MAX_AGE=900
if [[ ! -f "$STATUS" ]]; then
  logger -t spectradash-watchdog "Status file missing; restarting daemon"
  systemctl restart spectradash-daemon.service
  exit 0
fi
AGE=$(/opt/spectradash/.venv/bin/python - "$STATUS" <<'PY'
import json, sys
from datetime import datetime
try:
    data=json.load(open(sys.argv[1], encoding='utf-8'))
    hb=datetime.fromisoformat(data['daemon_heartbeat'])
    print(max(0, int((datetime.now()-hb).total_seconds())))
except Exception:
    print(999999)
PY
)
if (( AGE > MAX_AGE )); then
  logger -t spectradash-watchdog "Heartbeat stale (${AGE}s); restarting daemon"
  systemctl restart spectradash-daemon.service
fi
