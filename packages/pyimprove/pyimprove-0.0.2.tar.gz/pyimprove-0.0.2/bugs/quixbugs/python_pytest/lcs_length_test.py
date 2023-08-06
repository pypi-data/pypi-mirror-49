
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.lcs_length import lcs_length


@pytest.mark.timeout(0.1)
def test_0():
    assert lcs_length(*['witch', 'sandwich']) == 2

@pytest.mark.timeout(0.1)
def test_1():
    assert lcs_length(*['meow', 'homeowner']) == 4

@pytest.mark.timeout(0.1)
def test_2():
    assert lcs_length(*['fun', '']) == 0

@pytest.mark.timeout(0.1)
def test_3():
    assert lcs_length(*['fun', 'function']) == 3

@pytest.mark.timeout(0.1)
def test_4():
    assert lcs_length(*['cyborg', 'cyber']) == 3

@pytest.mark.timeout(0.1)
def test_5():
    assert lcs_length(*['physics', 'physics']) == 7

@pytest.mark.timeout(0.1)
def test_6():
    assert lcs_length(*['space age', 'pace a']) == 6

@pytest.mark.timeout(0.1)
def test_7():
    assert lcs_length(*['flippy', 'floppy']) == 3

@pytest.mark.timeout(0.1)
def test_8():
    assert lcs_length(*['acbdegcedbg', 'begcfeubk']) == 3

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
