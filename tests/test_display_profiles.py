from PIL import Image

from spectradash.display import make_hardware_test_pattern, prepare_for_driver
from spectradash.display_profiles import DEFAULT_PROFILE_ID, PROFILES, get_profile
from spectradash.render import adapt_to_profile


def test_default_profile_is_verified_13in3():
    profile = get_profile(DEFAULT_PROFILE_ID)
    assert profile.verified is True
    assert profile.size == (1600, 1200)


def test_every_profile_has_unique_valid_dimensions():
    assert len(PROFILES) == len(set(PROFILES))
    for profile in PROFILES.values():
        assert profile.width > 0 and profile.height > 0
        assert profile.density in {"compact", "standard", "expanded"}
        assert "black" in profile.colors and "white" in profile.colors


def test_renderer_adapts_to_every_profile():
    source = Image.new("RGB", (1600, 1200), "red")
    for profile in PROFILES.values():
        rendered = adapt_to_profile(source, {"display_profile": profile.id}, fast=True)
        assert rendered.size == profile.size


def test_test_patterns_match_profiles():
    for profile in PROFILES.values():
        assert make_hardware_test_pattern(profile.id).size == profile.size


def test_driver_size_validation():
    image = Image.new("RGB", (1600, 1200), "white")
    assert prepare_for_driver(image, DEFAULT_PROFILE_ID).size == (1600, 1200)
