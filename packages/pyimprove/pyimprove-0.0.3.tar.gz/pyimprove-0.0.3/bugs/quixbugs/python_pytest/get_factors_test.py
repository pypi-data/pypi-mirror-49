
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.get_factors import get_factors


@pytest.mark.timeout(0.1)
def test_0():
    assert get_factors(1) == []

@pytest.mark.timeout(0.1)
def test_1():
    assert get_factors(100) == [2, 2, 5, 5]

@pytest.mark.timeout(0.1)
def test_2():
    assert get_factors(101) == [101]

@pytest.mark.timeout(0.1)
def test_3():
    assert get_factors(104) == [2, 2, 2, 13]

@pytest.mark.timeout(0.1)
def test_4():
    assert get_factors(2) == [2]

@pytest.mark.timeout(0.1)
def test_5():
    assert get_factors(3) == [3]

@pytest.mark.timeout(0.1)
def test_6():
    assert get_factors(17) == [17]

@pytest.mark.timeout(0.1)
def test_7():
    assert get_factors(63) == [3, 3, 7]

@pytest.mark.timeout(0.1)
def test_8():
    assert get_factors(74) == [2, 37]

@pytest.mark.timeout(0.1)
def test_9():
    assert get_factors(73) == [73]

@pytest.mark.timeout(0.1)
def test_10():
    assert get_factors(9837) == [3, 3, 1093]

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
