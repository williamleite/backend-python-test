from alayatodo.model.user import User, SessionUser


def find_user(username, password):
    return User.query.filter_by(username=username, password=password).first()


def load_user(user_id):
    user = User.query.filter_by(id=int(user_id)).first()
    return SessionUser(user) if user else None
