from flask import (
    redirect,
    render_template,
    request,
    flash
)

from alayatodo import app
from alayatodo.service import messages, user as service


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    result = service.login(username, password)
    if result:
        flash(messages.SUCCESS_LOGIN[1])
        return redirect('/todo')
    else:
        flash(messages.ERROR_INVALIDLOGIN[1])
        return redirect('/login')


@app.route('/logout')
def logout():
    service.logout()
    return redirect('/')
