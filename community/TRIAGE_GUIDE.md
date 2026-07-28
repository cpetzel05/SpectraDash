# Issue Triage Guide

## First response goals

- Thank the reporter.
- Confirm the issue is understandable.
- Check for secrets or private information.
- Identify version, hardware, display, and operating system.
- Determine whether the issue is reproducible.
- Link duplicates rather than splitting investigation.
- Avoid promising a fix date before scope is understood.

## Suggested labels

- `bug`
- `enhancement`
- `documentation`
- `hardware`
- `compatibility`
- `needs-triage`
- `needs-info`
- `confirmed`
- `cannot-reproduce`
- `duplicate`
- `good first issue`
- `help wanted`
- `beta-blocker`
- `security`
- `wontfix`

## Priority

### Beta blocker

- Prevents installation on the primary target.
- Prevents all display refreshes.
- Causes configuration loss.
- Exposes secrets or private information.
- Causes repeated crashes or boot loops.

### High

- Breaks a primary layout.
- Breaks scheduled refresh.
- Prevents reboot recovery.
- Produces consistently incorrect weather data.

### Normal

- Affects a secondary feature.
- Has a practical workaround.
- Is limited to an unverified hardware configuration.

### Low

- Cosmetic issue.
- Documentation polish.
- Minor enhancement.
