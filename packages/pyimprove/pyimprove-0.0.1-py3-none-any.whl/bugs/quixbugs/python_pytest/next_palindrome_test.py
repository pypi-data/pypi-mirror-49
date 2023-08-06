
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.next_palindrome import next_palindrome


@pytest.mark.timeout(0.1)
def test_0():
    assert next_palindrome(*[[1, 4, 9, 4, 1]]) == [1, 5, 0, 5, 1]

@pytest.mark.timeout(0.1)
def test_1():
    assert next_palindrome(*[[1, 3, 1]]) == [1, 4, 1]

@pytest.mark.timeout(0.1)
def test_2():
    assert next_palindrome(*[[4, 7, 2, 5, 5, 2, 7, 4]]) == [4, 7, 2, 6, 6, 2, 7, 4]

@pytest.mark.timeout(0.1)
def test_3():
    assert next_palindrome(*[[4, 7, 2, 5, 2, 7, 4]]) == [4, 7, 2, 6, 2, 7, 4]

@pytest.mark.timeout(0.1)
def test_4():
    assert next_palindrome(*[[9, 9, 9]]) == [1, 0, 0, 1]

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
