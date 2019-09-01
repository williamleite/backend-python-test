from alayatodo import db


class Todo(db.Model):
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255))
    completed = db.Column(db.Integer)

    def __repr__(self):
        return '<Todo %r>' % self.description
