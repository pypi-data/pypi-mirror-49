
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.possible_change import possible_change


@pytest.mark.timeout(0.1)
def test_0():
    assert possible_change(*[[1, 5, 10, 25], 11]) == 4

@pytest.mark.timeout(0.1)
def test_1():
    assert possible_change(*[[1, 5, 10, 25], 75]) == 121

@pytest.mark.timeout(0.1)
def test_2():
    assert possible_change(*[[1, 5, 10, 25], 34]) == 18

@pytest.mark.timeout(0.1)
def test_3():
    assert possible_change(*[[1, 5, 10], 34]) == 16

@pytest.mark.timeout(0.1)
def test_4():
    assert possible_change(*[[1, 5, 10, 25], 140]) == 568

@pytest.mark.timeout(0.1)
def test_5():
    assert possible_change(*[[1, 5, 10, 25, 50], 140]) == 786

@pytest.mark.timeout(0.1)
def test_6():
    assert possible_change(*[[1, 5, 10, 25, 50, 100], 140]) == 817

@pytest.mark.timeout(0.1)
def test_7():
    assert possible_change(*[[1, 3, 7, 42, 78], 140]) == 981

@pytest.mark.timeout(0.1)
def test_8():
    assert possible_change(*[[3, 7, 42, 78], 140]) == 20

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
