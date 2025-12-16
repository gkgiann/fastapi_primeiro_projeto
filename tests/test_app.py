from http import HTTPStatus


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


def test_get_users(client):
    request = client.get('/users/')

    assert request.status_code == HTTPStatus.OK
    assert request.json() == {
        'users': [{'username': 'gian', 'email': 'gian@email.com', 'id': 1}]
    }


def test_get_user(client):
    request = client.get('/users/1')

    assert request.status_code == HTTPStatus.OK
    assert request.json() == {
        'username': 'gian',
        'email': 'gian@email.com',
        'id': 1,
    }


def test_get_user_not_found(client):
    request = client.get('/users/567')
    assert request.status_code == HTTPStatus.NOT_FOUND
    assert request.json() == {'detail': 'User not found!'}


def test_update_user(client):
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


def test_remove_user(client):
    request_delete = client.delete('/users/1/')
    assert request_delete.status_code == HTTPStatus.NO_CONTENT


def test_remove_user_not_found(client):
    request = client.delete('/users/73')
    assert request.status_code == HTTPStatus.NOT_FOUND
    assert request.json() == {'detail': 'User not found!'}
