
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.kth import kth


@pytest.mark.timeout(0.1)
def test_0():
    assert kth(*[[1, 2, 3, 4, 5, 6, 7], 4]) == 5

@pytest.mark.timeout(0.1)
def test_1():
    assert kth(*[[3, 6, 7, 1, 6, 3, 8, 9], 5]) == 7

@pytest.mark.timeout(0.1)
def test_2():
    assert kth(*[[3, 6, 7, 1, 6, 3, 8, 9], 2]) == 3

@pytest.mark.timeout(0.1)
def test_3():
    assert kth(*[[2, 6, 8, 3, 5, 7], 0]) == 2

@pytest.mark.timeout(0.1)
def test_4():
    assert kth(*[[34, 25, 7, 1, 9], 4]) == 34

@pytest.mark.timeout(0.1)
def test_5():
    assert kth(*[[45, 2, 6, 8, 42, 90, 322], 1]) == 6

@pytest.mark.timeout(0.1)
def test_6():
    assert kth(*[[45, 2, 6, 8, 42, 90, 322], 6]) == 322

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
