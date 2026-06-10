# tests/test_main.py

def test_main_runs_without_error():
    """Test that main() can be imported and called"""
    from src.main import main
    # This should not raise any exception
    try:
        main()
        assert True
    except Exception as e:
        assert False, f"main() raised an exception: {e}"


def test_planner_exists():
    """Test that planner module can be imported"""
    from src.planner import plan_task
    assert callable(plan_task)
