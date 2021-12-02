import pytest
import Timer


def test_scheduler_update_database():
    assert Timer.scheduler_update_database() is True
