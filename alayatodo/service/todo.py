from flask import render_template, flash
from flask_login import current_user

from alayatodo.dao import todo as dao, row2dict


def render_todo(index=0, limit=5):
    todos = dao.find_todo_paged(index, int(current_user.id), limit)
    if todos:
        first = todos[0].id if int(index) - limit >= 0 else 0
        last = todos[-1].id
    else:
        first = 0
        last = 1

    return render_template('todos.html', todos=todos, first=first, last=last)


def todos_success(message):
    flash(message[1])
    return render_todo()


def todos_error(message):
    flash("%s - %s" % message)
    return render_todo()


def create_todo(user, description, completed):
    dao.create_todo(user, description, completed)


def find_one(id):
    return dao.find_todo_by_id(id)


def remove(id):
    dao.remove_todo(id)


def todo_as_json(id):
    db_todo = dao.find_todo_by_id(id)
    return row2dict(db_todo)


def toggle_todo_completed(id):
    dao.toggle_todo_completed(id)
