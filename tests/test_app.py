from http import HTTPStatus

from fastapi_primeiro_projeto.schemas import UserPublic


def test_create_user(client):
    request = client.post(
        '/users/',
        json={'username': 'gian', 'email': 'gian@email.com', 'password': '13'},
    )

    assert request.status_code == HTTPStatus.CREATED
    assert request.json() == {
        'id': 1,
        'username': 'gian',
        'email': 'gian@email.com',
    }


def test_create_user_username_conflict(client, user):
    request = client.post(
        '/users/',
        json={'username': 'test', 'email': 'gian@email.com', 'password': '13'},
    )

    assert request.status_code == HTTPStatus.CONFLICT
    assert request.json() == {'detail': 'Username already exists'}


def test_create_user_email_conflict(client, user):
    request = client.post(
        '/users/',
        json={'username': 'gian', 'email': 'test@test.com', 'password': '13'},
    )

    assert request.status_code == HTTPStatus.CONFLICT
    assert request.json() == {'detail': 'Email already exists'}


def test_get_users(client):
    request = client.get('/users/')

    assert request.status_code == HTTPStatus.OK
    assert request.json() == {'users': []}


def test_get_users_with_one_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_get_user(client, user):
    request = client.get('/users/1')

    assert request.status_code == HTTPStatus.OK
    assert request.json() == {
        'username': 'test',
        'email': 'test@test.com',
        'id': 1,
    }


def test_get_user_not_found(client):
    request = client.get('/users/567')
    assert request.status_code == HTTPStatus.NOT_FOUND
    assert request.json() == {'detail': 'User not found!'}


def test_update_user(client, user):
    request = client.put(
        '/users/1',
        json={
            'username': 'geraldo',
            'email': 'geraldo@email.com',
            'password': 'snehaboa',
        },
    )

    assert request.status_code == HTTPStatus.OK
    assert request.json() == {
        'username': 'geraldo',
        'email': 'geraldo@email.com',
        'id': 1,
    }


def test_update_integrity_error(client, user):
    client.post(
        '/users/',
        json={
            'username': 'test2',
            'email': 'test2@test2.com',
            'password': 'snehaboa',
        },
    )

    request = client.put(
        f'/users/{user.id}',
        json={
            'username': 'test2',
            'email': 'wlh@email.com',
            'password': 'snehaboaweg',
        },
    )

    assert request.status_code == HTTPStatus.CONFLICT
    assert request.json() == {'detail': 'Username or email already exists'}


def test_update_user_not_found(client):
    request = client.put(
        '/users/7',
        json={
            'username': 'geraldo',
            'email': 'geraldo@email.com',
            'password': 'snehaboa',
        },
    )

    assert request.status_code == HTTPStatus.NOT_FOUND
    assert request.json() == {'detail': 'User not found!'}


def test_remove_user(client, user):
    request_delete = client.delete('/users/1/')
    assert request_delete.status_code == HTTPStatus.NO_CONTENT


def test_remove_user_not_found(client):
    request = client.delete('/users/73')
    assert request.status_code == HTTPStatus.NOT_FOUND
    assert request.json() == {'detail': 'User not found!'}
