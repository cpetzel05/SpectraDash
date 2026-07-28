from spectradash.config import DEFAULT_CONFIG
from spectradash.render import _forecast_date_text, _forecast_day_label, _resolved_forecast_date_style


def test_default_forecast_date_settings():
    assert DEFAULT_CONFIG["forecast_date_style"] == "auto"
    assert DEFAULT_CONFIG["forecast_first_day_label"] == "today"
    assert DEFAULT_CONFIG["show_forecast_updated"] is True


def test_forecast_date_formats():
    day = {"date": "2026-07-23"}
    assert _forecast_date_text(day, "expanded") == "JUL 23"
    assert _forecast_date_text(day, "compact") == "7/23"


def test_auto_style_uses_profile_size():
    assert _resolved_forecast_date_style({"forecast_date_style":"auto", "layout_density":"auto", "display_profile":"waveshare-13in3e"}) == "expanded"
    assert _resolved_forecast_date_style({"forecast_date_style":"auto", "layout_density":"compact", "display_profile":"waveshare-13in3e"}) == "compact"

def test_explicit_style_wins():
    assert _resolved_forecast_date_style({"forecast_date_style":"off", "layout_density":"expanded"}) == "off"


def test_first_forecast_card_can_say_today():
    day = {"label": "Wednesday", "date": "2026-07-22"}
    assert _forecast_day_label(day, 0, {"forecast_first_day_label": "today"}) == "TODAY"
    assert _forecast_day_label(day, 0, {"forecast_first_day_label": "weekday"}) == "WEDNESDAY"
    assert _forecast_day_label(day, 1, {"forecast_first_day_label": "today"}) == "WEDNESDAY"
