from dataclasses import asdict

from sqlalchemy import select

from fastapi_primeiro_projeto.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(User) as time:
        new_user = User(username='max', password='secret', email='teste@test')
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'max'))
    user_dict = asdict(user)

    assert user_dict == {
        'id': 1,
        'username': 'max',
        'password': 'secret',
        'email': 'teste@test',
        'created_at': time,
    }
