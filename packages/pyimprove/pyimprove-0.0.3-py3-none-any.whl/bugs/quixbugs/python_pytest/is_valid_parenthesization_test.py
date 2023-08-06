
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.is_valid_parenthesization import is_valid_parenthesization


@pytest.mark.timeout(0.1)
def test_0():
    assert is_valid_parenthesization(*['((()()))()']) == True

@pytest.mark.timeout(0.1)
def test_1():
    assert is_valid_parenthesization(*[')()(']) == False

@pytest.mark.timeout(0.1)
def test_2():
    assert is_valid_parenthesization(*['((']) == False

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
