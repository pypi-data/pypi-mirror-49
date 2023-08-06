
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.hanoi import hanoi


@pytest.mark.timeout(0.1)
def test_0():
    assert hanoi(*[1, 1, 3]) == [[1, 3]]

@pytest.mark.timeout(0.1)
def test_1():
    assert hanoi(*[2, 1, 3]) == [[1, 2], [1, 3], [2, 3]]

@pytest.mark.timeout(0.1)
def test_2():
    assert hanoi(*[3, 1, 3]) == [[1, 3], [1, 2], [3, 2], [1, 3], [2, 1], [2, 3], [1, 3]]

@pytest.mark.timeout(0.1)
def test_3():
    assert hanoi(*[4, 1, 3]) == [[1, 2], [1, 3], [2, 3], [1, 2], [3, 1], [3, 2], [1, 2], [1, 3], [2, 3], [2, 1], [3, 1], [2, 3], [1, 2], [1, 3], [2, 3]]

@pytest.mark.timeout(0.1)
def test_4():
    assert hanoi(*[2, 1, 2]) == [[1, 3], [1, 2], [3, 2]]

@pytest.mark.timeout(0.1)
def test_5():
    assert hanoi(*[2, 1, 1]) == [[1, 2], [1, 1], [2, 1]]

@pytest.mark.timeout(0.1)
def test_6():
    assert hanoi(*[2, 3, 1]) == [[3, 2], [3, 1], [2, 1]]

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
