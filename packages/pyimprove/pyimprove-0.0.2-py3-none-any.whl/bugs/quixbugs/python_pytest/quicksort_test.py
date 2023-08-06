
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.quicksort import quicksort


@pytest.mark.timeout(0.1)
def test_0():
    assert quicksort(*[[1, 2, 6, 72, 7, 33, 4]]) == [1, 2, 4, 6, 7, 33, 72]

@pytest.mark.timeout(0.1)
def test_1():
    assert quicksort(*[[3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9, 3]]) == [1, 1, 2, 3, 3, 3, 4, 5, 5, 5, 6, 7, 8, 9, 9, 9]

@pytest.mark.timeout(0.1)
def test_2():
    assert quicksort(*[[5, 4, 3, 2, 1]]) == [1, 2, 3, 4, 5]

@pytest.mark.timeout(0.1)
def test_3():
    assert quicksort(*[[5, 4, 3, 1, 2]]) == [1, 2, 3, 4, 5]

@pytest.mark.timeout(0.1)
def test_4():
    assert quicksort(*[[8, 1, 14, 9, 15, 5, 4, 3, 7, 17, 11, 18, 2, 12, 16, 13, 6, 10]]) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

@pytest.mark.timeout(0.1)
def test_5():
    assert quicksort(*[[9, 4, 5, 2, 17, 14, 10, 6, 15, 8, 12, 13, 16, 3, 1, 7, 11]]) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

@pytest.mark.timeout(0.1)
def test_6():
    assert quicksort(*[[13, 14, 7, 16, 9, 5, 24, 21, 19, 17, 12, 10, 1, 15, 23, 25, 11, 3, 2, 6, 22, 8, 20, 4, 18]]) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

@pytest.mark.timeout(0.1)
def test_7():
    assert quicksort(*[[8, 5, 15, 7, 9, 14, 11, 12, 10, 6, 2, 4, 13, 1, 3]]) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

@pytest.mark.timeout(0.1)
def test_8():
    assert quicksort(*[[4, 3, 7, 6, 5, 2, 1]]) == [1, 2, 3, 4, 5, 6, 7]

@pytest.mark.timeout(0.1)
def test_9():
    assert quicksort(*[[4, 3, 1, 5, 2]]) == [1, 2, 3, 4, 5]

@pytest.mark.timeout(0.1)
def test_10():
    assert quicksort(*[[5, 4, 2, 3, 6, 7, 1]]) == [1, 2, 3, 4, 5, 6, 7]

@pytest.mark.timeout(0.1)
def test_11():
    assert quicksort(*[[10, 16, 6, 1, 14, 19, 15, 2, 9, 4, 18, 17, 12, 3, 11, 8, 13, 5, 7]]) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

@pytest.mark.timeout(0.1)
def test_12():
    assert quicksort(*[[10, 16, 6, 1, 14, 19, 15, 2, 9, 4, 18]]) == [1, 2, 4, 6, 9, 10, 14, 15, 16, 18, 19]

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
