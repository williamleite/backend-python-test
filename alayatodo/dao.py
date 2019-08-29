from alayatodo import (models, db)


def row2dict(row):
    return dict([(column.name, getattr(row, column.name)) for column in row.__table__.columns])


def find_user(username, password):
    return models.User.query.filter_by(username=username, password=password).first()


def find_todo_by_id(id):
    return models.Todo.query.filter_by(id=id).first()


def create_todo(user_id, description, completed):
    todo = models.Todo(user_id=user_id, description=description, completed=completed)
    db.session.add(todo)
    db.session.commit()


def remove_todo(id):
    todo = models.Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()


def toggle_todo_completed(id):
    todo = models.Todo.query.filter_by(id=id).first()
    todo.completed = 0 if todo.completed == 1 else 1
    db.session.commit()


def find_todo_paged(last, user_id, limit=5):
    return models.Todo.query.filter(models.Todo.id > last, models.Todo.user_id == user_id).order_by(
        models.Todo.id).limit(5).all()
