# RC1 72-Hour Stability Plan

## Required configuration

Use the primary reference hardware with normal scheduled refresh enabled.

## Record every 6 hours

- CPU use
- Memory use
- Disk use
- Device temperature
- Last successful refresh
- Refresh duration
- Service status
- Daemon heartbeat
- Weather-provider status

## Injected recovery tests

- Reboot once after 12 hours.
- Disconnect network for 10 minutes after 24 hours.
- Stop and restart the display worker after 36 hours.
- Simulate provider failure after 48 hours.
- Perform a manual refresh after 60 hours.

## Pass criteria

- No unrecoverable crash.
- No configuration loss.
- Scheduler resumes after reboot.
- Network recovery is automatic.
- Provider recovery is automatic.
- Physical display refresh remains functional.
- Memory does not grow continuously without stabilizing.
