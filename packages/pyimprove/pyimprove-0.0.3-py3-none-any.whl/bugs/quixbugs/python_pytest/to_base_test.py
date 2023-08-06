
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.to_base import to_base


@pytest.mark.timeout(0.1)
def test_0():
    assert to_base(*[31, 16]) == 1F

@pytest.mark.timeout(0.1)
def test_1():
    assert to_base(*[41, 2]) == 101001

@pytest.mark.timeout(0.1)
def test_2():
    assert to_base(*[44, 5]) == 134

@pytest.mark.timeout(0.1)
def test_3():
    assert to_base(*[27, 23]) == 14

@pytest.mark.timeout(0.1)
def test_4():
    assert to_base(*[56, 23]) == 2A

@pytest.mark.timeout(0.1)
def test_5():
    assert to_base(*[8237, 24]) == E75

@pytest.mark.timeout(0.1)
def test_6():
    assert to_base(*[8237, 34]) == 749

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
