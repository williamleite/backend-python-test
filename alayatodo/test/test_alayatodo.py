import os
import random
import tempfile

import pytest

import alayatodo
from alayatodo.service import messages
from alayatodo.service.utils import init_db


@pytest.fixture
def client():
    db_fd, alayatodo.app.config['DATABASE'] = tempfile.mkstemp()
    alayatodo.app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///%s' % alayatodo.app.config['DATABASE']

    alayatodo.app.config['TESTING'] = True
    client = alayatodo.app.test_client()

    with alayatodo.app.app_context():
        init_db()

    yield client

    os.close(db_fd)
    os.unlink(alayatodo.app.config['DATABASE'])


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def create_todo(client, description, completed):
    return client.post('/todo/', data=dict(
        description=description,
        completed=completed
    ), follow_redirects=True)


def test_login_perfect_case(client):
    rv = login(client, 'user1', 'user1')
    assert messages.SUCCESS_LOGIN[1] in rv.data


def test_login_worst_case(client):
    rv = login(client, 'user_invalid', 'invalid_password')
    assert messages.ERROR_INVALIDLOGIN[1] in rv.data


def test_login_invalid_password(client):
    rv = login(client, 'user1', 'invalid_password')
    assert messages.ERROR_INVALIDLOGIN[1] in rv.data


def test_todo_without_login(client):
    rv = client.get('/todo', follow_redirects=True)
    assert messages.ERROR_LOGINREQUIRED[1] in rv.data


def test_todo_with_login(client):
    rv = login(client, 'user1', 'user1')
    assert messages.SUCCESS_LOGIN[1] in rv.data

    rv = client.get('/todo', follow_redirects=True)
    assert messages.ERROR_LOGINREQUIRED[1] not in rv.data


def test_todo_insert_perfect_case(client):
    rv = login(client, 'user3', 'user3')
    assert messages.SUCCESS_LOGIN[1] in rv.data

    rv = create_todo(client, 'Test 1', None)
    assert messages.SUCCESS_ADD[1] in rv.data

    rv = create_todo(client, 'Test 2', 'on')
    assert messages.SUCCESS_ADD[1] in rv.data


def test_todo_insert_missing_description(client):
    rv = login(client, 'user3', 'user3')
    assert messages.SUCCESS_LOGIN[1] in rv.data

    rv = create_todo(client, None, None)
    assert messages.ERROR_NODESCRIPTION[1] in rv.data


def test_todo_insert_and_retrieve(client):
    rv = login(client, 'user3', 'user3')
    assert messages.SUCCESS_LOGIN[1] in rv.data

    random_test_name = 'Test unique %s' % random.randint(3, 999)
    rv = create_todo(client, random_test_name, 'on')
    assert messages.SUCCESS_ADD[1] in rv.data

    rv = client.get('/todo', follow_redirects=True)
    assert random_test_name in rv.data


def test_todo_remove(client):
    rv = login(client, 'user1', 'user1')
    assert messages.SUCCESS_LOGIN[1] in rv.data

    rv = client.delete('/todo/1', follow_redirects=True)
    assert messages.SUCCESS_REMOVE[1] in rv.data


def test_todo_toggle(client):
    rv = login(client, 'user1', 'user1')
    assert messages.SUCCESS_LOGIN[1] in rv.data

    rv = client.post('/todo/toggle/2', data=dict(), follow_redirects=True)
    assert messages.SUCCESS_COMPLETETOGGLE[1] in rv.data
