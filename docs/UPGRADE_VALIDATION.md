# Upgrade Validation

Test every supported upgrade path.

## Paths

- v1.0.0-beta.1 → v1.0.0-beta.2
- v1.0.0-beta.2 → v1.0.0-rc1
- v1.0.0-rc1 → v1.0.0

## Validate

- Configuration retained
- Provider settings retained
- Location retained
- Units retained
- Layout retained
- Theme retained
- Refresh interval retained
- Display profile retained
- Services restarted correctly
- Browser assets updated
- Scheduler resumes
- Physical display refresh succeeds

## Failure handling

Document backup, rollback, and manual recovery steps before publishing the release.
