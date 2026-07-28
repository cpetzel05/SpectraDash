# Beta Incident Response

## Severity 1 — Critical

Examples:

- Data loss
- Secret exposure
- Boot loop
- Installer damages the operating system
- Physical display commands create a hardware safety risk

Actions:

1. Stop announcements.
2. Mark the release as affected.
3. Publish a warning in the release notes and pinned Discussion.
4. Remove or replace the release asset if necessary.
5. Open a private security report when sensitive information is involved.
6. Prepare a hotfix.
7. Document the cause and prevention.

## Severity 2 — Major

Examples:

- Primary hardware cannot install.
- Scheduled refresh fails for most users.
- Main layout is unusable.
- Upgrade fails but fresh installation works.

Actions:

1. Add a known issue.
2. Apply `beta-blocker`.
3. Publish a workaround when available.
4. Target the next beta or hotfix.

## Severity 3 — Normal

Examples:

- Secondary feature failure
- Cosmetic issue
- Unverified hardware incompatibility
- Documentation gap

Actions:

1. Triage normally.
2. Add to the appropriate milestone.
3. Document workarounds where useful.
