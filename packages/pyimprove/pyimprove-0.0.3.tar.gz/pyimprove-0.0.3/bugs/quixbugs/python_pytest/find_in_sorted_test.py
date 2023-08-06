
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.find_in_sorted import find_in_sorted


@pytest.mark.timeout(0.1)
def test_0():
    assert find_in_sorted(*[[3, 4, 5, 5, 5, 5, 6], 5]) == 3

@pytest.mark.timeout(0.1)
def test_1():
    assert find_in_sorted(*[[1, 2, 3, 4, 6, 7, 8], 5]) == -1

@pytest.mark.timeout(0.1)
def test_2():
    assert find_in_sorted(*[[1, 2, 3, 4, 6, 7, 8], 4]) == 3

@pytest.mark.timeout(0.1)
def test_3():
    assert find_in_sorted(*[[2, 4, 6, 8, 10, 12, 14, 16, 18, 20], 18]) == 8

@pytest.mark.timeout(0.1)
def test_4():
    assert find_in_sorted(*[[3, 5, 6, 7, 8, 9, 12, 13, 14, 24, 26, 27], 0]) == -1

@pytest.mark.timeout(0.1)
def test_5():
    assert find_in_sorted(*[[3, 5, 6, 7, 8, 9, 12, 12, 14, 24, 26, 27], 12]) == 6

@pytest.mark.timeout(0.1)
def test_6():
    assert find_in_sorted(*[[24, 26, 28, 50, 59], 101]) == -1

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
