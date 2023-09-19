import pytest


def test_first():
    print("Hello world")
    pass


@pytest.mark.xfail(reason='1', strict=True)
def test_second():
    assert 1 == 1


class ExampleClass(object):
    class_attr = 0

    def __init__(self, instance_attr):
        self.instance_attr = instance_attr


