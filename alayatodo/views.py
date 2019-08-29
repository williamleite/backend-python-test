from alayatodo import app
from flask import (
    g,
    redirect,
    render_template,
    request,
    session
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
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s'";
    cur = g.db.execute(sql % (username, password))
    user = cur.fetchone()
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


def find_by_id(id):
    cur = g.db.execute("SELECT * FROM todos WHERE id ='%s'" % id)
    return cur.fetchone()


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    return render_template('todo.html', todo=find_by_id(id))


def fetch_all():
    cur = g.db.execute("SELECT * FROM todos")
    return cur.fetchall()


def fetch_paged(last, limit=5):
    cur = g.db.execute("SELECT * FROM todos WHERE id > %s AND user_id = %s ORDER BY id ASC LIMIT %s" %
                       (last, session['user']['id'], limit))
    return cur.fetchall()


@app.route('/todo/<id>/json', methods=['GET'])
def todo_as_json(id):
    todo = find_by_id(id)
    return dict((k, todo[k]) for k in todo.keys())


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    return todos_paged(0)


def render_todo(index=0, success=None, error=None):
    limit = 5
    todos = fetch_paged(index, limit)
    if todos:
        first = todos[0]['id'] if int(index) - limit >= 0 else index
        last = todos[-1]['id']
    else:
        first = 0
        last = 1

    return render_template('todos.html', todos=todos, first=first, last=last, success=success, error=error)


@app.route('/todo/page/<index>', methods=['GET'])
def todos_paged(index):
    if not session.get('logged_in'):
        return redirect('/login')

    return render_todo(index)


@app.route('/todo/toggle/<id>', methods=['POST'])
def todos_toggle_completed(id):
    if not session.get('logged_in'):
        return redirect('/login')

    g.db.execute("UPDATE todos SET completed = CASE WHEN completed = 0 THEN 1 ELSE 0 END WHERE id = %s" % id)
    g.db.commit()

    return redirect('/todo')


def todos_success(code):
    if code == SUCCESS_ADD:
        description = "Todo added successfully"
    elif code == SUCCESS_REMOVE:
        description = "Todo removed successfully"

    return render_todo(success=(code, description))


def todos_error(code):
    if code == ERROR_NODESCRIPTION:
        description = "Description is required"

    return render_todo(error=(code, description))


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')

    description = request.form.get('description', '')
    if not description:
        return todos_error(ERROR_NODESCRIPTION)

    completed = 1 if request.form.get('completed', 0) == 'on' else 0

    g.db.execute(
        "INSERT INTO todos (user_id, description, completed) VALUES ('%s', '%s', %s)"
        % (session['user']['id'], description, completed)
    )
    g.db.commit()
    return todos_success(SUCCESS_ADD)


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    g.db.execute("DELETE FROM todos WHERE id ='%s'" % id)
    g.db.commit()
    return todos_success(SUCCESS_REMOVE)
