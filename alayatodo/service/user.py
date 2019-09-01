from flask_login import login_user, logout_user

from alayatodo.dao import user as dao
from alayatodo.model.user import SessionUser


def login(username, password):
    user = dao.find_user(username, password)

    if user:
        login_user(SessionUser(user))
        return True

    return False


def logout():
    logout_user()
