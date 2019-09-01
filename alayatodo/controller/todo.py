from flask import request, render_template
from flask_login import login_required, current_user

from alayatodo import app
from alayatodo.service import messages, todo as service


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
@login_required
def todos():
    return todos_paged(0)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
@login_required
def todos_post():
    description = request.form.get('description', '')
    if not description:
        return service.todos_error(messages.ERROR_NODESCRIPTION)

    completed = 1 if request.form.get('completed', 0) == 'on' else 0

    service.create_todo(int(current_user.id), description, completed)

    return service.todos_success(messages.SUCCESS_ADD)


@app.route('/todo/<int:todoid>', methods=['GET'])
@login_required
def todo(todoid):
    db_todo = service.find_one(todoid)
    return render_template('todo.html', todo=db_todo)


@app.route('/todo/<int:todoid>', methods=['POST', 'DELETE'])
@login_required
def todo_delete(todoid):
    service.remove(todoid)
    return service.todos_success(messages.SUCCESS_REMOVE)


@app.route('/todo/<int:todoid>/json', methods=['GET'])
@login_required
def todo_as_json(todoid):
    json_todo = service.todo_as_json(todoid)
    return json_todo


@app.route('/todo/page/<int:index>', methods=['GET'])
@login_required
def todos_paged(index):
    return service.render_todo(index)


@app.route('/todo/toggle/<int:todoid>', methods=['POST'])
@login_required
def todos_toggle_completed(todoid):
    service.toggle_todo_completed(todoid)
    return service.todos_success(messages.SUCCESS_COMPLETETOGGLE)
