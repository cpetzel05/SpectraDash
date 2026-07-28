from datetime import datetime

from spectradash.render import _resolved_premium_lcd_mode


def test_premium_lcd_explicit_modes():
    assert _resolved_premium_lcd_mode({}, {"premium_lcd_mode": "light"}) == "light"
    assert _resolved_premium_lcd_mode({}, {"premium_lcd_mode": "dark"}) == "dark"


def test_premium_lcd_automatic_tracks_day_night():
    config = {"premium_lcd_mode": "automatic"}
    assert _resolved_premium_lcd_mode({"is_night": False}, config) == "light"
    assert _resolved_premium_lcd_mode({"is_night": True}, config) == "dark"
