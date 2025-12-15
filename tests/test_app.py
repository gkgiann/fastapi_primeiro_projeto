from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_primeiro_projeto.app import app


def test_root_deve_retornar_hello_world():
    client = TestClient(app)
    res = client.get('/')
    assert res.json() == {'message': 'Hello World'}
    assert res.status_code == HTTPStatus.OK
