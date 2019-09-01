from flask_login import UserMixin

from alayatodo import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class SessionUser(UserMixin):
    """Flask-login User class"""

    def __init__(self, db_user=None):
        if db_user:
            self.id = db_user.id
            self.username = db_user.username
        else:
            self.id = 0
            self.username = ""

    def get_id(self):
        return unicode(self.id)
