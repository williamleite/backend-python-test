from alayatodo import (app, dao)
from flask import (
    redirect,
    render_template,
    request,
    session,
    flash
)

ERROR_NODESCRIPTION = "0x0001"
SUCCESS_ADD = "0x0001"
SUCCESS_REMOVE = "0x0002"


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.find_user(username, password)

    if user:
        session['user'] = dict(user)
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    return todos_paged(0)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_post():
    if not session.get('logged_in'):
        return redirect('/login')

    description = request.form.get('description', '')
    if not description:
        return todos_error(ERROR_NODESCRIPTION)

    completed = 1 if request.form.get('completed', 0) == 'on' else 0

    dao.create_todo(session['user']['id'], description, completed)

    return todos_success(SUCCESS_ADD)


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    return render_template('todo.html', todo=dao.find_todo_by_id(id))


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')

    dao.remove_todo(id)

    return todos_success(SUCCESS_REMOVE)


@app.route('/todo/<id>/json', methods=['GET'])
def todo_as_json(id):
    todo = dao.find_todo_by_id(id)
    return dao.row2dict(todo)


@app.route('/todo/page/<index>', methods=['GET'])
def todos_paged(index):
    if not session.get('logged_in'):
        return redirect('/login')

    return render_todo(index)


@app.route('/todo/toggle/<id>', methods=['POST'])
def todos_toggle_completed(id):
    if not session.get('logged_in'):
        return redirect('/login')

    dao.toggle_todo_completed(id)

    return redirect('/todo')


def render_todo(index=0, limit=5):
    todos = dao.find_todo_paged(index, session['user']['id'], limit)
    if todos:
        first = todos[0].id if int(index) - limit >= 0 else index
        last = todos[-1].id
    else:
        first = 0
        last = 1

    return render_template('todos.html', todos=todos, first=first, last=last)


def todos_success(code):
    if code == SUCCESS_ADD:
        description = "Todo added successfully"
    elif code == SUCCESS_REMOVE:
        description = "Todo removed successfully"

    flash(description)

    return render_todo()


def todos_error(code):
    if code == ERROR_NODESCRIPTION:
        description = "Description is required"

    flash("%s - %s", code, description)

    return render_todo()
