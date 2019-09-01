from alayatodo import db
from alayatodo.model.todo import Todo


def find_todo_by_id(id):
    return Todo.query.filter_by(id=id).first()


def create_todo(user_id, description, completed):
    todo = Todo(user_id=user_id, description=description, completed=completed)
    db.session.add(todo)
    db.session.commit()


def remove_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()


def toggle_todo_completed(id):
    todo = Todo.query.filter_by(id=id).first()
    if todo:
        todo.completed = 0 if todo.completed == 1 else 1
        db.session.commit()


def find_todo_paged(last, user_id, limit=5):
    return Todo.query.filter(Todo.id > last, Todo.user_id == user_id).order_by(Todo.id).limit(limit).all()
