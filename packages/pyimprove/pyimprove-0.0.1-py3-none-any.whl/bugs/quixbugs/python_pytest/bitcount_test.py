
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.bitcount import bitcount


@pytest.mark.timeout(0.1)
def test_0():
    assert bitcount(127) == 7

@pytest.mark.timeout(0.1)
def test_1():
    assert bitcount(128) == 1

@pytest.mark.timeout(0.1)
def test_2():
    assert bitcount(3005) == 9

@pytest.mark.timeout(0.1)
def test_3():
    assert bitcount(13) == 3

@pytest.mark.timeout(0.1)
def test_4():
    assert bitcount(14) == 3

@pytest.mark.timeout(0.1)
def test_5():
    assert bitcount(27) == 4

@pytest.mark.timeout(0.1)
def test_6():
    assert bitcount(834) == 4

@pytest.mark.timeout(0.1)
def test_7():
    assert bitcount(254) == 7

@pytest.mark.timeout(0.1)
def test_8():
    assert bitcount(256) == 1

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
