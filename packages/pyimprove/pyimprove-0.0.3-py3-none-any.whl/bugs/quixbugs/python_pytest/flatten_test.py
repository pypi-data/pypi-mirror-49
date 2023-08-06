
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.flatten import flatten


@pytest.mark.timeout(0.1)
def test_0():
    assert flatten(*[[[1, [], [2, 3]], [[4]], 5]]) == [1, 2, 3, 4, 5]

@pytest.mark.timeout(0.1)
def test_1():
    assert flatten(*[[[], [], [], [], []]]) == []

@pytest.mark.timeout(0.1)
def test_2():
    assert flatten(*[[[], [], 1, [], 1, [], []]]) == [1, 1]

@pytest.mark.timeout(0.1)
def test_3():
    assert flatten(*[[1, 2, 3, [[4]]]]) == [1, 2, 3, 4]

@pytest.mark.timeout(0.1)
def test_4():
    assert flatten(*[[1, 4, 6]]) == [1, 4, 6]

@pytest.mark.timeout(0.1)
def test_5():
    assert flatten(*[['moe', 'curly', 'larry']]) == ['moe', 'curly', 'larry']

@pytest.mark.timeout(0.1)
def test_6():
    assert flatten(*[['a', 'b', ['c'], ['d'], [['e']]]]) == ['a', 'b', 'c', 'd', 'e']

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
