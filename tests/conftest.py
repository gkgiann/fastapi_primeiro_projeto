from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from fastapi_primeiro_projeto import app
from fastapi_primeiro_projeto.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    yield session

    session.close()
    table_registry.metadata.drop_all(engine)
    engine.dispose()


@contextmanager
def _mock_db_time(model, time=datetime(2025, 12, 18)):

    def hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time

    event.listen(model, 'before_insert', hook)

    yield time

    event.remove(model, 'before_insert', hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time
