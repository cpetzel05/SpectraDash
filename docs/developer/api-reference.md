# API Reference

The public API surface may change during beta. Treat undocumented endpoints as internal.

## Developer status

```http
GET /api/developer/status
```

Expected response sections include:

- `config`
- `daemon`
- `status`
- `system`
- `version`

The endpoint is used by Developer Mode to refresh live diagnostics.

## API design guidance

New endpoints should:

- Return structured JSON
- Validate inputs
- Avoid returning secrets
- Use clear error messages
- Preserve compatibility where practical
- Require appropriate authentication when remote access is supported

## Future documentation

As the API stabilizes, this page should list request bodies, response schemas, status codes, and authentication requirements for every supported public endpoint.
