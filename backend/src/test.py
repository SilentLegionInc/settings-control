from flask import Flask, request, url_for, redirect
from flask_login import LoginManager, current_user, login_user, logout_user

app = Flask(__name__)
login = LoginManager(app)


@app.route('/very/very/long/path')
def to_redirect():
    return 'Now you here'


@app.route('/')
def hello_dude():
    return redirect(url_for('to_redirect'))


@app.route('/hello/<username>', methods=['GET', 'POST'])
def hello_user(username):
    return 'Hello, {}'.format(username)


@app.route('/number/<int:number>')
def send_number(number):
    return 'Your number + 1 is {}'.format(number + 1)


@app.route('/float/<float:fnum>')
def send_float(fnum):
    return 'Your float + 0.5 is {}'.format(fnum + 0.25)


@app.route('/path/<path:path_var>')
def send_path(path_var):
    return path_var

