# -*- coding: utf-8 -*-

import pytest
from polecat.test import fixture


@pytest.fixture
def server():
    with fixture.server() as f:
        yield f


@pytest.fixture
def immutabledb():
    with fixture.immutabledb() as f:
        yield f


@pytest.fixture
def testdb():
    with fixture.testdb() as f:
        yield f


@pytest.fixture(scope='session')
def migrateddb():
    with fixture.migrateddb() as f:
        yield f


@pytest.fixture
def db(migrateddb):
    with fixture.db(migrateddb) as f:
        yield f


@pytest.fixture(scope='session')
def factory():
    with fixture.factory() as f:
        yield f
