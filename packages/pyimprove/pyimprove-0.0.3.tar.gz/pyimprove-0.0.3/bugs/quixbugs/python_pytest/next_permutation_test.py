
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.next_permutation import next_permutation


@pytest.mark.timeout(0.1)
def test_0():
    assert next_permutation(*[[3, 2, 4, 1]]) == [3, 4, 1, 2]

@pytest.mark.timeout(0.1)
def test_1():
    assert next_permutation(*[[3, 5, 6, 2, 1]]) == [3, 6, 1, 2, 5]

@pytest.mark.timeout(0.1)
def test_2():
    assert next_permutation(*[[3, 5, 6, 2]]) == [3, 6, 2, 5]

@pytest.mark.timeout(0.1)
def test_3():
    assert next_permutation(*[[4, 5, 1, 7, 9]]) == [4, 5, 1, 9, 7]

@pytest.mark.timeout(0.1)
def test_4():
    assert next_permutation(*[[4, 5, 8, 7, 1]]) == [4, 7, 1, 5, 8]

@pytest.mark.timeout(0.1)
def test_5():
    assert next_permutation(*[[9, 5, 2, 6, 1]]) == [9, 5, 6, 1, 2]

@pytest.mark.timeout(0.1)
def test_6():
    assert next_permutation(*[[44, 5, 1, 7, 9]]) == [44, 5, 1, 9, 7]

@pytest.mark.timeout(0.1)
def test_7():
    assert next_permutation(*[[3, 4, 5]]) == [3, 5, 4]

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
