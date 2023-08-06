
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.sieve import sieve


@pytest.mark.timeout(0.1)
def test_0():
    assert sieve(*[1]) == []

@pytest.mark.timeout(0.1)
def test_1():
    assert sieve(*[2]) == [2]

@pytest.mark.timeout(0.1)
def test_2():
    assert sieve(*[4]) == [2, 3]

@pytest.mark.timeout(0.1)
def test_3():
    assert sieve(*[7]) == [2, 3, 5, 7]

@pytest.mark.timeout(0.1)
def test_4():
    assert sieve(*[20]) == [2, 3, 5, 7, 11, 13, 17, 19]

@pytest.mark.timeout(0.1)
def test_5():
    assert sieve(*[50]) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
