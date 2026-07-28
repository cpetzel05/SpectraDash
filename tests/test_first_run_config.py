from spectradash.config import default_config, location_is_configured


def test_default_has_no_location():
    config = default_config()
    assert config["location_name"] == ""
    assert config["latitude"] is None
    assert config["longitude"] is None
    assert not location_is_configured(config)


def test_configured_location_requires_setup_and_coordinates():
    config = default_config()
    config.update({"setup_complete": True, "location_name": "Test, US", "latitude": 1.0, "longitude": 2.0})
    assert location_is_configured(config)
