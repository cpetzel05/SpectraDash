from spectradash.app import _parse_settings


def base():
    return {"location_name":"Phoenix, Arizona, US","latitude":33.4,"longitude":-112.0,"timezone":"America/Phoenix","units":"fahrenheit","wind_units":"mph","rotation":0,"refresh_minutes":45,"physical_display":False,"theme":"sunrise","custom_title":"SpectraDash","show_hourly":True,"show_air_quality":True,"show_moon":True}


def test_unchanged_location_does_not_geocode():
    updated, error = _parse_settings({"location":"Phoenix, Arizona, US","rotation":"90"}, base())
    assert error is None
    assert updated["rotation"] == 90
    assert updated["latitude"] == 33.4


def test_invalid_rotation_falls_back():
    updated, _ = _parse_settings({"location":"Phoenix, Arizona, US","rotation":"bad"}, base())
    assert updated["rotation"] == 0



def test_premium_lcd_mode_is_parsed():
    updated, error = _parse_settings({"location":"Phoenix, Arizona, US", "layout_preset":"premium-lcd", "premium_lcd_mode":"light"}, base())
    assert error is None
    assert updated["layout_preset"] == "premium-lcd"
    assert updated["premium_lcd_mode"] == "light"
