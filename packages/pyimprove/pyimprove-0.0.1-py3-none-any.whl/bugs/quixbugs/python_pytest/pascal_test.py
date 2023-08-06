
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.pascal import pascal


@pytest.mark.timeout(0.1)
def test_0():
    assert pascal(*[1]) == [[1]]

@pytest.mark.timeout(0.1)
def test_1():
    assert pascal(*[2]) == [[1], [1, 1]]

@pytest.mark.timeout(0.1)
def test_2():
    assert pascal(*[3]) == [[1], [1, 1], [1, 2, 1]]

@pytest.mark.timeout(0.1)
def test_3():
    assert pascal(*[4]) == [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1]]

@pytest.mark.timeout(0.1)
def test_4():
    assert pascal(*[5]) == [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
