import os
import datetime
from functools import wraps

from flask import Flask, flash, request, redirect, url_for, render_template, session, jsonify
from flask_api import status
from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt

from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from toolbelt.configuration.authorization_service import AuthorizationService
from toolbelt.api_routes import api_blueprint as api_endpoints
from toolbelt.support.helper import allowed_file_extension
from toolbelt.support.logger import Logger
from toolbelt.support.settings_service import SettingsService
from toolbelt.configuration.modules_service import ModulesService
from toolbelt.support.forms import LoginForm
from toolbelt.support.models import User
from toolbelt.support.server_exception import ServerException

# Init flask application
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = SettingsService().private_server_config['secret']
app.config['UPLOAD_FOLDER'] = os.path.expanduser(SettingsService().server_config['upload_path'])
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
app.secret_key = app.config['SECRET_KEY']

cors = CORS(app)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
# will try to save current token here
bootstrap = Bootstrap(app)

login = LoginManager(app)
login.login_view = 'login'

# registering api endpoints
app.register_blueprint(api_endpoints, url_prefix='/api')


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session['is_logged']:
            token = session.get('token', 'Basic Og==')
            token_uuid, password = AuthorizationService().parse_token(token)

            try:
                AuthorizationService().check_token(token_uuid, password)
                session['is_logged'] = True
            except ServerException:
                session['is_logged'] = False
                session['token'] = None
                raise
        else:
            session['is_logged'] = False
            session['token'] = None
            raise ServerException('Необходимо авторизироваться', status.HTTP_401_UNAUTHORIZED)

        return func(*args, **kwargs)

    return wrapper


def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            # TODO handle exception for flask and jinja (flush or redirect)
            pass
    return wrapper
# Here routes starts.


@login.user_loader
def load_user(user_id):
    if user_id != SettingsService().server_config.get('password'):
        Logger().critical_message('Incorrect user id in loader {}'.format(user_id))
        return None
    return User()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


# @app.context_processor
# def set_is_auth():
#     # TODO refactored to g?
#     return dict(is_auth=session.get('is_logged', False),
#                 user_timestamp=session.get('timestamp', None))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        Logger().info_message('Already logged')
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        Logger().info_message('Submit login')
        try:
            if not AuthorizationService().authorize(form.password.data):
                return redirect(url_for('login'))
        except Exception as ex:
            return redirect(url_for('index'))

        # if we here then out credentials is valid
        login_user(User())
        next_page = request.args.get('next')
        session['is_logged'] = True
        session['timestamp'] = datetime.datetime.utcnow()

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    session['is_logged'] = False
    return redirect(url_for('login'))


@app.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    if request.method == 'GET':
        return render_template('config.html', config=SettingsService().get_core_config(reload_from_disk=True))
    elif request.method == 'POST':
        result = SettingsService().get_core_config(reload_from_disk=True)
        for key in request.form:
            result[key] = request.form.get(key)
        if SettingsService().save_core_config(result):
            Logger().info_message('Saved')
        else:
            Logger().info_message('Error')
        return render_template('config.html', config=SettingsService().get_core_config(reload_from_disk=True))


@app.route('/networks', methods=['GET'])
@login_required
def networks():
    return render_template('networks.html')


@app.route('/modules', methods=['GET'])
@handle_errors
@login_required
def modules():
    res = ModulesService().get_modules_list()
    return render_template('modules.html', core=res['core'], dependencies=res['dependencies'])


@app.route('/core/run', methods=['POST'])
@handle_errors
@login_required
def run_core():
    if ModulesService().run_core():
        flash('Ядро успешно запущено')
        return redirect(url_for('modules'))
    else:
        raise ServerException('Не удалось запустить ядро', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/core/stop', methods=['POST'])
@handle_errors
@login_required
def stop_core():
    if ModulesService().stop_core():
        flash('Ядро успешно остановлено')
        return redirect(url_for('modules'))
    else:
        raise ServerException('Не удалось остановить ядро', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/pull_machine', methods=['POST'])
@handle_errors
@login_required
def pull_current_machine():
    if ModulesService().pull_machine():
        flash('Текущая конфигурация успешно обвнолена')
        return redirect(url_for('modules'))
    else:
        raise ServerException('Серверная ошибка', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/build_machine', methods=['POST'])
@handle_errors
@login_required
def build_current_machine():
    if ModulesService().build_machine():
        flash('Текущая конфигурация успешно собрана')
        return redirect(url_for('modules'))
    else:
        raise ServerException('Серверная ошибка', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/pull_module/<string:module_name>', methods=['POST'])
@handle_errors
@login_required
def pull_module(module_name):
    if ModulesService().pull_module(module_name):
        flash('Модуль {} успешно обновлен'.format(module_name))
        return redirect(url_for('modules'))
    else:
        raise ServerException('Серверная ошибка', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/build_module/<string:module_name>', methods=['POST'])
@handle_errors
@login_required
def build_module(module_name):
    if ModulesService().build_module(module_name):
        flash('Модуль {} успешно собран'.format(module_name))
        return redirect(url_for('modules'))
    else:
        raise ServerException('Серверная ошибка', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/manual_module_update/<string:module_name>', methods=['POST'])
@handle_errors
@login_required
def manual_update_module(module_name):
    allowed_extensions = {'zip'}

    if 'file' not in request.files:
        raise ServerException('В форме отсутсвтвуют файлы', status.HTTP_400_BAD_REQUEST)

    file = request.files['file']
    if not file or not file.filename:
        raise ServerException('Не найден файл', status.HTTP_400_BAD_REQUEST)

    if not allowed_file_extension(file.filename, allowed_extensions):
        raise ServerException('Некорректный формат файла. Разрешены только: {}'.format(allowed_extensions),
                              status.HTTP_406_NOT_ACCEPTABLE)

    file_name = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    file.save(file_path)

    if ModulesService().manual_module_update(file_path, module_name):
        flash('Модуль {} успешно обновлен из архива'.format(module_name))
        return redirect(url_for('modules'))
    else:
        raise ServerException('Серверная ошибка', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/server_config', methods=['GET'])
@handle_errors
@login_required
def server_config():
    import copy
    server_config_obj = copy.copy(SettingsService().server_config)
    del server_config_obj['need_to_auth']
    del server_config_obj['password']
    server_config_obj['possible_machines_types'] = list(SettingsService().machines_configs.keys())
    return render_template('server_settings.html', settings_dict=server_config_obj)


@app.route('/server_config', methods=['POST'])
@handle_errors
@login_required
def update_server_config():
    new_server_config = request.get_json()
    machine_type = new_server_config.get('type')
    if machine_type:
        if machine_type not in SettingsService().machines_configs.keys():
            raise ServerException('Недопустимый тип робота {}'.format(machine_type), status.HTTP_400_BAD_REQUEST)
    SettingsService().server_config.update(new_server_config)
    SettingsService().save_server_config()
    return redirect(url_for('server_config'))
