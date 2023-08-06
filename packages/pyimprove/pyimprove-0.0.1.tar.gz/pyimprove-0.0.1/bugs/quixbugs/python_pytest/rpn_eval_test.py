
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.rpn_eval import rpn_eval


@pytest.mark.timeout(0.1)
def test_0():
    assert rpn_eval(*[[3.0, 5.0, '+', 2.0, '/']]) == 4.0

@pytest.mark.timeout(0.1)
def test_1():
    assert rpn_eval(*[[2.0, 2.0, '+']]) == 4.0

@pytest.mark.timeout(0.1)
def test_2():
    assert rpn_eval(*[[7.0, 4.0, '+', 3.0, '-']]) == 8.0

@pytest.mark.timeout(0.1)
def test_3():
    assert rpn_eval(*[[1.0, 2.0, '*', 3.0, 4.0, '*', '+']]) == 14.0

@pytest.mark.timeout(0.1)
def test_4():
    assert rpn_eval(*[[5.0, 9.0, 2.0, '*', '+']]) == 23.0

@pytest.mark.timeout(0.1)
def test_5():
    assert rpn_eval(*[[5.0, 1.0, 2.0, '+', 4.0, '*', '+', 3.0, '-']]) == 14.0

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
