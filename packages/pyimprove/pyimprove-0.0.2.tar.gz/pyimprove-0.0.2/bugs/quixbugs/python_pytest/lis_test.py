
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.lis import lis


@pytest.mark.timeout(0.1)
def test_0():
    assert lis(*[[4, 1, 5, 3, 7, 6, 2]]) == 3

@pytest.mark.timeout(0.1)
def test_1():
    assert lis(*[[10, 22, 9, 33, 21, 50, 41, 60, 80]]) == 6

@pytest.mark.timeout(0.1)
def test_2():
    assert lis(*[[7, 10, 9, 2, 3, 8, 1]]) == 3

@pytest.mark.timeout(0.1)
def test_3():
    assert lis(*[[9, 11, 2, 13, 7, 15]]) == 4

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
