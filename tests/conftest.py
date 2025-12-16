import pytest
from fastapi.testclient import TestClient

from fastapi_primeiro_projeto import app


@pytest.fixture
def client():
    return TestClient(app)
