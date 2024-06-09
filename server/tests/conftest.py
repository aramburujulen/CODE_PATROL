from src.app import create_app
from tests.config.test_config import TestConfig
import pytest

@pytest.fixture(scope='session')
def app():
    app = create_app(TestConfig)
    yield app

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


