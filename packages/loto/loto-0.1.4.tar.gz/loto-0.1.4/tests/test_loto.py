
import pytest
from src.loto import LockoutTagout
from time import sleep
from threading import Thread

# fixture for managing the LockoutTagout class variables
@pytest.fixture
def loto_fixture():
    LockoutTagout.locks.clear()

def test_tags_different_locks(loto_fixture):
    # Test if making 2 loto functions with different tags results
    # in different locks being made
    @LockoutTagout('tag1')
    def f():
        pass
    
    @LockoutTagout('tag2')
    def g():
        pass

    assert len(LockoutTagout.locks) == 2
    assert f._loto_tag is not g._loto_tag


def test_tags_same_lock(loto_fixture):
    # test that making 2 loto functions with the same tag
    # will associate the same lock with each
    @LockoutTagout('tag1')
    def f():
        pass

    @LockoutTagout('tag1')
    def g():
        pass
    assert len(LockoutTagout.locks) == 1
    assert f._loto_tag is g._loto_tag

def test_same_tags_locked_out(loto_fixture):
    # Make 2 threads. On lasts a long time but 
    # starts first. THe other thread tries to finish
    # immediately but starts after the first.
    # We test that the first thread actually finishes first
    # because they share a lock
    report = []

    @LockoutTagout('tag1')
    def slowFunc():
        sleep(1)
        report.append('slow')
        return

    @LockoutTagout('tag1')
    def fastFunc():
        report.append('fast')
        return

    slowThread = Thread(target=slowFunc)
    fastThread = Thread(target=fastFunc)

    slowThread.start()
    fastThread.start()

    fastThread.join()
    slowThread.join()

    assert report[0] == 'slow' and report[1] == 'fast'
