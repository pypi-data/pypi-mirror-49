
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.kheapsort import kheapsort


@pytest.mark.timeout(0.1)
def test_0():
    assert kheapsort(*[[1, 2, 3, 4, 5], 0]) == [1, 2, 3, 4, 5]

@pytest.mark.timeout(0.1)
def test_1():
    assert kheapsort(*[[3, 2, 1, 5, 4], 2]) == [1, 2, 3, 4, 5]

@pytest.mark.timeout(0.1)
def test_2():
    assert kheapsort(*[[5, 4, 3, 2, 1], 4]) == [1, 2, 3, 4, 5]

@pytest.mark.timeout(0.1)
def test_3():
    assert kheapsort(*[[3, 12, 5, 1, 6], 3]) == [1, 3, 5, 6, 12]

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
