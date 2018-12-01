from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from logger import Logger
from settings_service import SettingsService
from flask_login import login_user, login_required, logout_user, current_user
from flask import request, redirect, url_for, jsonify, render_template, flash, Response
from werkzeug.urls import url_parse
from logs_service import LogsService
from forms import LoginForm
from models import User
from helpers import check_user_credentials
from update_service import UpdateService
from core_service import CoreService


# Init flask application
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = SettingsService().private_server_config['secret']
app.secret_key = app.config['SECRET_KEY']
app.config['USER_AUTH_HASH'] = SettingsService().server_config['authorization']

cors = CORS(app)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap(app)

login = LoginManager(app)
login.login_view = 'login'

# Here routes starts.


@login.user_loader
def load_user(user_id):
    if user_id != SettingsService().server_config.get('USER_AUTH_HASH'):
        Logger().critical_message('Incorrect user id in loader {}'.format(user_id))
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
        try:
            if not check_user_credentials(form.username.data, form.password.data):
                return redirect(url_for('login'))
        except Exception as ex:
            return redirect(url_for('index'))

        # if we here then out credentials is valid
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
def config():
    if request.method == 'GET':
        return render_template('config.html', config=SettingsService().get_core_config(reload_from_disk=True))
    elif request.method == 'POST':
        result = SettingsService().get_core_config(reload_from_disk=True)
        for key in request.form:
            result[key] = request.form.get(key)
        if SettingsService().save_core_config(result)['code'] == 0:
            Logger().info_message('Saved')
        else:
            Logger().info_message('Error')
        return render_template('config.html', config=SettingsService().get_core_config(reload_from_disk=True))


@app.route('/api/logs', methods=['GET'])
def api_logs():
    return jsonify(LogsService().get_logs(request.args.get('limit', 1), request.args.get('offset', 0)))


# decorator for check authorization via token
# TODO fix (need to pair username\pass)
def api_authorization(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('authorization', '', str)
        auth = auth_header.split(" ")[1] if auth_header else ''
        if not auth:
            Logger().critical_message('No auth token: {}'.format(auth))
            return Response('You need to authorize to access this url', 401)
        else:
            Logger().info_message('{}:{}'.format(app.config.get('USER_AUTH_HASH'), auth))
            if bcrypt.check_password_hash(app.config.get('USER_AUTH_HASH'), auth):
                Logger().info_message('Successful login')
            else:
                Logger().info_message('Incorrect username\password')
                return Response('Incorrect username or password', 401)
        return func(*args, **kwargs)
    return wrapper


@app.route('/api/config', methods=['GET', 'POST'])
@api_authorization
def api_config():
    if request.method == 'GET':
        return jsonify(SettingsService().get_core_config(reload_from_disk=True))
    elif request.method == 'POST':
        return jsonify(SettingsService().save_core_config(request.get_json()))


@app.route('/api/compile_core', methods=['POST'])
# @api_authorization
def api_compile_core():
    import time
    params = request.get_json()
    if params.get('with_dependencies', False):
        dependencies = SettingsService().current_machine_config.get('dependencies', [])
        for dep in dependencies:
            Logger().info_message('Updating lib: {}'.format(dep), 'Compile Core: ')
            UpdateService().update_and_upgrade_lib_sync(dep)

    CoreService().compile_core()
    while CoreService().compile_status is None:
        print('wait')
        time.sleep(1)

    return jsonify({'compile_status': CoreService().compile_status.value})


@app.route('/api/login', methods=['POST'])
def api_login():
    info = request.get_json()
    if check_user_credentials(info.get('login', ''), info.get('password', '')):
        return Response('Success', 200)
    else:
        return Response('Incorrect username or password', 401)
