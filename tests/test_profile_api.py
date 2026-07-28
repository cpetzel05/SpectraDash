import os
os.environ.setdefault("SPECTRADASH_DATA_DIR", "/tmp/spectradash-test-profile-api")

from spectradash.app import create_app


def test_profile_api_lists_verified_and_experimental():
    client = create_app().test_client()
    response = client.get("/api/display-profiles")
    assert response.status_code == 200
    payload = response.get_json()
    statuses = {item["status"] for item in payload["profiles"]}
    assert "verified" in statuses
    assert "experimental" in statuses
