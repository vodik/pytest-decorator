import pytest


@pytest.fixture
def important_value():
    return 42


@pytest.fixture
def alternative_value():
    return 43


@pytest.decorator
def example_decorator(testbody, important_value):
    assert important_value == 42
    for value in testbody():
        assert value == important_value


@example_decorator
def test_example1(important_value, alternative_value):
    yield important_value
    yield alternative_value - 1


@example_decorator
def test_example2(alternative_value):
    yield alternative_value
