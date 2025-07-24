import pytest
from brain import parser, planner
from executor.executor import TaskExecutor
from database.manager import DatabaseManager

@pytest.fixture(scope="module")
def db():
    mgr = DatabaseManager()
    yield mgr
    mgr.close()

def test_full_cycle(tmp_path, db, monkeypatch):
    # step 1: parse
    text = "open calculator"
    parsed = parser.parse_intent(text)

    # step 2: plan
    plan = planner.generate_plan(parsed)

    # step 3: mock plugin execution
    class DummyPlugin:
        def open(self, app):
            return f"opened {app}"
    monkeypatch.setitem(TaskExecutor(db).loaded_plugins, "app_controller", DummyPlugin)

    # step 4: run
    executor = TaskExecutor(db)
    result = executor.run(plan)

    assert "opened calculator" in result
    # step 5: log in DB
    db.log_task(parsed["intent"], "app_controller", "open", result)
    history = db.fetch_user_profile()  # assume this returns some memory
    assert isinstance(history, dict)
