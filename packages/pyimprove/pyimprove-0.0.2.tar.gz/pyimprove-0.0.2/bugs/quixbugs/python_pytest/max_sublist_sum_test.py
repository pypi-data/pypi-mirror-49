
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.max_sublist_sum import max_sublist_sum


@pytest.mark.timeout(0.1)
def test_0():
    assert max_sublist_sum(*[[4, -5, 2, 1, -1, 3]]) == 5

@pytest.mark.timeout(0.1)
def test_1():
    assert max_sublist_sum(*[[0, -1, 2, -1, 3, -1, 0]]) == 4

@pytest.mark.timeout(0.1)
def test_2():
    assert max_sublist_sum(*[[3, 4, 5]]) == 12

@pytest.mark.timeout(0.1)
def test_3():
    assert max_sublist_sum(*[[4, -2, -8, 5, -2, 7, 7, 2, -6, 5]]) == 19

@pytest.mark.timeout(0.1)
def test_4():
    assert max_sublist_sum(*[[-4, -4, -5]]) == 0

@pytest.mark.timeout(0.1)
def test_5():
    assert max_sublist_sum(*[[-2, 1, -3, 4, -1, 2, 1, -5, 4]]) == 6

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
