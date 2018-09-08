from src import login, app, SettingsService, Logger, bcrypt
from flask_login import login_user, login_required, logout_user, current_user
from flask import request, redirect, url_for, jsonify, render_template, flash
from werkzeug.urls import url_parse
from src.logs_service import LogsService
from src.forms import LoginForm
from src.models import User


@login.user_loader
def load_user(user_id):
    if user_id != app.config.get('USER_AUTH_HASH'):
        Logger().critical_message('Uncorrect user id in loader {}'.format(user_id))
        return None
    return User()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        Logger().info_message('Submit login')
        user_info = '{}:{}'.format(form.username.data, form.password.data)
        user_hash = app.config.get('USER_AUTH_HASH', None)
        if not user_hash:
            Logger().critical_message('user auth hash is None!')
            flash('Auth error. Please check user hash on server side')
            return redirect(url_for('index'))
        if not bcrypt.check_password_hash(user_hash, user_info):
            Logger().critical_message('Incorrect username/password')
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(User(), remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/config', methods=['GET', 'POST'])
@login_required
def ui_config():
    if request.method == 'GET':
        return render_template('config.html', config=SettingsService().load_current_server_config())
    elif request.method == 'POST':
        result = SettingsService().load_current_server_config()
        for key in request.form:
            result[key] = request.form.get(key)
        if SettingsService().save_server_config(result)['code'] == 0:
            Logger().info_message('Saved')
        else:
            Logger().info_message('Error')
        return render_template('config.html', config=SettingsService().load_current_server_config())


@app.route('/api/logs', methods=['GET'])
def logs():
    return jsonify(LogsService().get_logs(request.args.get('limit', 1), request.args.get('offset', 0)))


def api_authorization(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('authorization', '', str)
        auth = auth_header.split(" ")[1] if auth_header else ''
        Logger().info_message('my token "{}"'.format(auth))
        if not auth:
            Logger().critical_message('unauth {}'.format(auth))
        else:
            Logger().info_message('{}:{}'.format(app.config.get('USER_AUTH_HASH'), auth))
            if bcrypt.check_password_hash(app.config.get('USER_AUTH_HASH'), auth):
                Logger().info_message('Successful login')
            else:
                Logger().info_message('Incorrect username\password')
        return func(*args, **kwargs)
    return wrapper


@app.route('/api/config', methods=['GET', 'POST'])
@api_authorization
def config():
    if request.method == 'GET':
        return jsonify(SettingsService().load_current_server_config())
    elif request.method == 'POST':
        return jsonify(SettingsService().save_server_config(request.get_json()))
