import pytest

def test_login():
    a="selenium"
    assert a.__eq__("selenium")

@pytest.mark.login
def test_m2():
    a="selenium"
    assert False
