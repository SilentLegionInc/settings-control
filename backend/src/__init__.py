from flask import Flask, request, redirect, url_for, jsonify, render_template, flash
from flask_cors import CORS
from flask_login import login_user, login_required, logout_user, current_user, LoginManager, login_manager
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from werkzeug.urls import url_parse
from src.logger import Logger
from src.settings_service import SettingsService
from src.logs_service import LogsService
from src.forms import LoginForm
from src.models import User
import os


# Init flask application
app = Flask(__name__)
bcrypt = Bcrypt(app)
# Setting env variables
os.environ['settings_login'] = SettingsService().config['login']
os.environ['settings_password'] = bcrypt.generate_password_hash(SettingsService().config['password']).decode('utf-8')

os.environ['settings_secret'] = SettingsService().config['secret']
app.secret_key = os.environ.get('settings_secret')

cors = CORS(app)

bootstrap = Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

login = LoginManager(app)
login.login_view = 'login'

# Here routes starts. I can't move it to separate file


@login.user_loader
def load_user(user_id):
    # mocked!
    return User()


@app.route('/login_test')
def login_test():
    if not current_user.is_authenticated:
        user = User()
        login_user(user)


@app.route('/logout_test')
def logout_test():
    if current_user.is_authenticated:
        logout_user()


@app.route('/secure')
@login_required
def secure():
    return 'It is secret'


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
        user = os.environ.get('settings_login')
        if user is None or user != form.username.data \
                or not bcrypt.check_password_hash(os.environ['settings_password'], form.password.data):
            Logger().critical_message('Incorrect!')
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


@app.route('/api/config', methods=['GET', 'POST'])
def config():
    if request.method == 'GET':
        return jsonify(SettingsService().load_current_server_config())
    elif request.method == 'POST':
        return jsonify(SettingsService().save_server_config(request.get_json()))


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


