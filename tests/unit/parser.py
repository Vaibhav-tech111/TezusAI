import pytest
from brain.parser import parse_intent

@pytest.mark.parametrize("text, expected_intent", [
    ("open calculator", "open_app"),
    ("shutdown my pc", "shutdown_system"),
    ("what's the weather", "get_weather"),
])
def test_intent_detection(text, expected_intent):
    result = parse_intent(text)
    assert result["intent"] == expected_intent
    assert 0.0 <= result["confidence"] <= 1.0
