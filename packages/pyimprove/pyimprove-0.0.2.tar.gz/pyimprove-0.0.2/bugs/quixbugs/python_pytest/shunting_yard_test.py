
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.shunting_yard import shunting_yard


@pytest.mark.timeout(0.1)
def test_0():
    assert shunting_yard(*[[10, '-', 5, '-', 2]]) == [10, 5, '-', 2, '-']

@pytest.mark.timeout(0.1)
def test_1():
    assert shunting_yard(*[[34, '-', 12, '/', 5]]) == [34, 12, 5, '/', '-']

@pytest.mark.timeout(0.1)
def test_2():
    assert shunting_yard(*[[4, '+', 9, '*', 9, '-', 10, '+', 13]]) == [4, 9, 9, '*', '+', 10, '-', 13, '+']

@pytest.mark.timeout(0.1)
def test_3():
    assert shunting_yard(*[[7, '*', 43, '-', 7, '+', 13, '/', 7]]) == [7, 43, '*', 7, '-', 13, 7, '/', '+']

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
