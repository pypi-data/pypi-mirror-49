
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.levenshtein import levenshtein


@pytest.mark.timeout(0.1)
def test_0():
    assert levenshtein(*['electron', 'neutron']) == 3

@pytest.mark.timeout(0.1)
def test_1():
    assert levenshtein(*['kitten', 'sitting']) == 3

@pytest.mark.timeout(0.1)
def test_2():
    assert levenshtein(*['rosettacode', 'raisethysword']) == 8

@pytest.mark.timeout(0.1)
def test_3():
    assert levenshtein(*['amanaplanacanalpanama', 'docnoteidissentafastneverpreventsafatnessidietoncod']) == 42

@pytest.mark.timeout(0.1)
def test_4():
    assert levenshtein(*['abcdefg', 'gabcdef']) == 2

@pytest.mark.timeout(0.1)
def test_5():
    assert levenshtein(*['', '']) == 0

@pytest.mark.timeout(0.1)
def test_6():
    assert levenshtein(*['hello', 'olleh']) == 4

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
