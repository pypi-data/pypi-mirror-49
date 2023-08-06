
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.find_first_in_sorted import find_first_in_sorted


@pytest.mark.timeout(0.1)
def test_0():
    assert find_first_in_sorted(*[[3, 4, 5, 5, 5, 5, 6], 5]) == 2

@pytest.mark.timeout(0.1)
def test_1():
    assert find_first_in_sorted(*[[3, 4, 5, 5, 5, 5, 6], 7]) == -1

@pytest.mark.timeout(0.1)
def test_2():
    assert find_first_in_sorted(*[[3, 4, 5, 5, 5, 5, 6], 2]) == -1

@pytest.mark.timeout(0.1)
def test_3():
    assert find_first_in_sorted(*[[3, 6, 7, 9, 9, 10, 14, 27], 14]) == 6

@pytest.mark.timeout(0.1)
def test_4():
    assert find_first_in_sorted(*[[0, 1, 6, 8, 13, 14, 67, 128], 80]) == -1

@pytest.mark.timeout(0.1)
def test_5():
    assert find_first_in_sorted(*[[0, 1, 6, 8, 13, 14, 67, 128], 67]) == 6

@pytest.mark.timeout(0.1)
def test_6():
    assert find_first_in_sorted(*[[0, 1, 6, 8, 13, 14, 67, 128], 128]) == 7

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
