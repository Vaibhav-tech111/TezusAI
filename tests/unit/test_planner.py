import pytest
from brain.planner import generate_plan

def test_simple_open_app_plan():
    parsed = {"intent": "open_app", "entities": ["calculator"]}
    plan = generate_plan(parsed)
    assert isinstance(plan, list)
    assert plan[0]["plugin"] == "app_controller"
    assert plan[0]["action"] == "open"
    assert plan[0]["params"]["app"] == "calculator"
