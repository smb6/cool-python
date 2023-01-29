import pytest


def test_first():
    print("Hello world")
    pass


@pytest.mark.xfail(reason='1', strict=True)
def test_second():
    assert 1 == 1
