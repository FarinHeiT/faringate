import pytest

from api import AppFactory

@pytest.fixture
def app_factory():
    return AppFactory()


@pytest.fixture
def client(app_factory):
    return app_factory.test_client()