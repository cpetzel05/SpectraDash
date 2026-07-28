# Incremental Release Policy

SpectraDash changes are released in small increments to protect the working web interface and display pipeline.

## Required checks

Every pull request should confirm:

- The web page opens on port 8080.
- Settings can be saved and reloaded.
- The refresh daemon starts normally.
- Preview rendering completes for the selected profile.
- Existing display profiles still report the correct resolution.
- Physical output remains disabled until preview validation succeeds.
- A rollback command is documented.

## Scope control

A release-candidate update should address one primary area. Unrelated refactors, design changes, new providers, and hardware-driver changes should not be combined in the same update.
