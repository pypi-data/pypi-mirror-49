
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.sqrt import sqrt


@pytest.mark.timeout(0.1)
def test_0():
    assert sqrt(*[2, 0.01]) == 1.4166666666666665

@pytest.mark.timeout(0.1)
def test_1():
    assert sqrt(*[2, 0.5]) == 1.5

@pytest.mark.timeout(0.1)
def test_2():
    assert sqrt(*[2, 0.3]) == 1.5

@pytest.mark.timeout(0.1)
def test_3():
    assert sqrt(*[4, 0.2]) == 2

@pytest.mark.timeout(0.1)
def test_4():
    assert sqrt(*[27, 0.01]) == 5.196164639727311

@pytest.mark.timeout(0.1)
def test_5():
    assert sqrt(*[33, 0.05]) == 5.744627526262464

@pytest.mark.timeout(0.1)
def test_6():
    assert sqrt(*[170, 0.03]) == 13.038404876679632

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
