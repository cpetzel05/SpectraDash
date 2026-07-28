# RC1 Rollback Plan

Before installation or upgrade:

1. Back up the SpectraDash configuration.
2. Record the current version.
3. Preserve the previous release archive.
4. Record service names and paths.

If RC1 fails:

1. Stop SpectraDash services.
2. Restore the previous application files.
3. Restore the saved configuration.
4. Reload service definitions.
5. Restart services.
6. Verify browser preview.
7. Verify physical display refresh.
8. Open a regression report with sanitized logs.

The exact commands must match the actual SpectraDash installer and service names before publication.
