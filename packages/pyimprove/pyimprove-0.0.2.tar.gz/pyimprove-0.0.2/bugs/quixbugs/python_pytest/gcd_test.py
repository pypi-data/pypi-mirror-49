
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.gcd import gcd


@pytest.mark.timeout(0.1)
def test_0():
    assert gcd(*[13, 13]) == 13

@pytest.mark.timeout(0.1)
def test_1():
    assert gcd(*[37, 600]) == 1

@pytest.mark.timeout(0.1)
def test_2():
    assert gcd(*[20, 100]) == 20

@pytest.mark.timeout(0.1)
def test_3():
    assert gcd(*[624129, 2061517]) == 18913

@pytest.mark.timeout(0.1)
def test_4():
    assert gcd(*[3, 12]) == 3

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
