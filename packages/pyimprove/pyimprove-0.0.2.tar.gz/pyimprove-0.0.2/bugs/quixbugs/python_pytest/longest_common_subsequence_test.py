
import time
import pytest

from bugs.quixbugs.python_pytest.python_programs.longest_common_subsequence import longest_common_subsequence


@pytest.mark.timeout(0.1)
def test_0():
    assert longest_common_subsequence(*['headache', 'pentadactyl']) == eadac

@pytest.mark.timeout(0.1)
def test_1():
    assert longest_common_subsequence(*['daenarys', 'targaryen']) == aary

@pytest.mark.timeout(0.1)
def test_2():
    assert longest_common_subsequence(*['XMJYAUZ', 'MZJAWXU']) == MJAU

@pytest.mark.timeout(0.1)
def test_3():
    assert longest_common_subsequence(*['thisisatest', 'testing123testing']) == tsitest

@pytest.mark.timeout(0.1)
def test_4():
    assert longest_common_subsequence(*['1234', '1224533324']) == 1234

@pytest.mark.timeout(0.1)
def test_5():
    assert longest_common_subsequence(*['abcbdab', 'bdcaba']) == bcba

@pytest.mark.timeout(0.1)
def test_6():
    assert longest_common_subsequence(*['TATAGC', 'TAGCAG']) == TAAG

@pytest.mark.timeout(0.1)
def test_7():
    assert longest_common_subsequence(*['ABCBDAB', 'BDCABA']) == BCBA

@pytest.mark.timeout(0.1)
def test_8():
    assert longest_common_subsequence(*['ABCD', 'XBCYDQ']) == BCD

@pytest.mark.timeout(0.1)
def test_9():
    assert longest_common_subsequence(*['acbdegcedbg', 'begcfeubk']) == begceb

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
