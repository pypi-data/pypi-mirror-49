
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.powerset import powerset


@pytest.mark.timeout(0.1)
def test_0():
    assert powerset(*[['a', 'b', 'c']]) == [[], ['c'], ['b'], ['b', 'c'], ['a'], ['a', 'c'], ['a', 'b'], ['a', 'b', 'c']]

@pytest.mark.timeout(0.1)
def test_1():
    assert powerset(*[['a', 'b']]) == [[], ['b'], ['a'], ['a', 'b']]

@pytest.mark.timeout(0.1)
def test_2():
    assert powerset(*[['a']]) == [[], ['a']]

@pytest.mark.timeout(0.1)
def test_3():
    assert powerset(*[[]]) == [[]]

@pytest.mark.timeout(0.1)
def test_4():
    assert powerset(*[['x', 'df', 'z', 'm']]) == [[], ['m'], ['z'], ['z', 'm'], ['df'], ['df', 'm'], ['df', 'z'], ['df', 'z', 'm'], ['x'], ['x', 'm'], ['x', 'z'], ['x', 'z', 'm'], ['x', 'df'], ['x', 'df', 'm'], ['x', 'df', 'z'], ['x', 'df', 'z', 'm']]

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
