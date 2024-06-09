from src.app import create_app
from tests.config.test_config import TestConfig
import pytest

@pytest.fixture
def app():
    app = create_app(TestConfig)
    yield app

@pytest.fixture
def client(app):
    return app.test_client()


def test_index(client):
    response = client.get('/students')
    assert response.status_code == 200
