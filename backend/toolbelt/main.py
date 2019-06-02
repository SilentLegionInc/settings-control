import os
import traceback
from functools import wraps

from flask import Flask, flash, request, redirect, url_for, render_template, session
from flask_api import status
from flask_cors import CORS
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
from toolbelt.support.server_exception import ServerException

# Init flask application
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = SettingsService().private_server_config['secret']
app.secret_key = app.config['SECRET_KEY']

cors = CORS(app)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
# will try to save current token here
bootstrap = Bootstrap(app)

# registering api endpoints
app.register_blueprint(api_endpoints, url_prefix='/api')


class FlashCategoriesClasses:
    info = 'alert-info'
    warning = 'alert-warning'
    error = 'alert-danger'
    success = 'alert-success'


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('is_logged'):
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


def handle_errors(redirect_path, no_401_redirect=False):
    def _handle_errors(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                if isinstance(ex, ServerException):
                    Logger().error_message('Got an exception')
                    Logger().error_message('Message: {}. Code: {}'.format(ex.message, ex.status_code))
                    Logger().error_message(traceback.format_exc())
                    flash(ex.message, FlashCategoriesClasses.error)
                    if ex.status_code is status.HTTP_401_UNAUTHORIZED and not no_401_redirect:
                        return redirect(url_for('login'))
                    else:
                        return redirect(redirect_path)
                else:
                    Logger().error_message('Got an unknown exception')
                    Logger().error_message(traceback.format_exc())
                    flash('Серверная ошибка', FlashCategoriesClasses.error)
                    return redirect(request.path)
        return wrapper
    return _handle_errors
# Here routes starts.


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
@handle_errors(redirect_path='/login')
def login():
    if session.get('is_logged'):
        Logger().info_message('Already logged')
        flash('Уже авторизован', FlashCategoriesClasses.info)
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        Logger().info_message('Submit login')
        token = AuthorizationService().authorize(form.password.data)

        # if we here then out credentials is valid
        next_page = request.args.get('next')

        session['is_logged'] = True
        session['token'] = token

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        flash('Успешно авторизован', FlashCategoriesClasses.success)
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@handle_errors(redirect_path='/')
@auth_required
def logout():
    session['is_logged'] = False
    session['token'] = None
    flash('Успешно деавторизован')
    return redirect(url_for('index'))


@app.route('/config', methods=['GET', 'POST'])
@handle_errors(redirect_path='/config')
@auth_required
def config():
    import json
    if request.method == 'GET':
        configuration = json.dumps(SettingsService().get_core_config(reload_from_disk=True), indent=4)
        return render_template('config.html', config=configuration)
    elif request.method == 'POST':
        new_config_str = request.form['config']
        try:
            parsed = json.loads(new_config_str)
        except Exception as e:
            Logger().error_message('Cant parse config json {}'.format(e))
            raise ServerException('Некорректный формат конфигурации', status.HTTP_400_BAD_REQUEST, e)

        if SettingsService().save_core_config(parsed):
            Logger().info_message('Config successfully saved')

        configuration = json.dumps(SettingsService().get_core_config(reload_from_disk=True), indent=4)
        return render_template('config.html', config=configuration)


@app.route('/networks', methods=['GET'])
@handle_errors(redirect_path='/networks')
@auth_required
def networks():
    return render_template('networks.html')


@app.route('/modules', methods=['GET'])
@handle_errors(redirect_path='/modules')
@auth_required
def modules():
    res = ModulesService().get_modules_list()
    return render_template('modules.html', core=res['core'], dependencies=res['dependencies'])


@app.route('/core/run', methods=['POST'])
@handle_errors(redirect_path='/modules')
@auth_required
def run_core():
    cmd_params = request.form.get('cmd_params') or ''
    if ModulesService().run_core(cmd_params=cmd_params):
        flash('Ядро успешно запущено')
        return redirect(url_for('modules'))
    else:
        raise ServerException('Не удалось запустить ядро', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/core/stop', methods=['POST'])
@handle_errors(redirect_path='/modules')
@auth_required
def stop_core():
    if ModulesService().stop_core():
        flash('Ядро успешно остановлено')
        return redirect(url_for('modules'))
    else:
        raise ServerException('Не удалось остановить ядро', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/pull_machine', methods=['POST'])
@handle_errors(redirect_path='/modules')
@auth_required
def pull_current_machine():
    if ModulesService().pull_machine():
        flash('Текущая конфигурация успешно обвнолена')
        return redirect(url_for('modules'))
    else:
        raise ServerException('Серверная ошибка', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/build_machine', methods=['POST'])
@handle_errors(redirect_path='/modules')
@auth_required
def build_current_machine():
    if ModulesService().build_machine():
        flash('Текущая конфигурация успешно собрана')
        return redirect(url_for('modules'))
    else:
        raise ServerException('Серверная ошибка', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/pull_module/<string:module_name>', methods=['POST'])
@handle_errors(redirect_path='/modules')
@auth_required
def pull_module(module_name):
    if ModulesService().pull_module(module_name):
        flash('Модуль {} успешно обновлен'.format(module_name))
        return redirect(url_for('modules'))
    else:
        raise ServerException('Серверная ошибка', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/build_module/<string:module_name>', methods=['POST'])
@handle_errors(redirect_path='/modules')
@auth_required
def build_module(module_name):
    if ModulesService().build_module(module_name):
        flash('Модуль {} успешно собран'.format(module_name))
        return redirect(url_for('modules'))
    else:
        raise ServerException('Серверная ошибка', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/manual_module_update/<string:module_name>', methods=['POST'])
@handle_errors(redirect_path='/modules')
@auth_required
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
    download_path = os.path.expanduser(SettingsService().server_config['upload_path'])
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    file_path = os.path.join(download_path, file_name)
    file.save(file_path)

    if ModulesService().manual_module_update(file_path, module_name):
        flash('Модуль {} успешно обновлен из архива'.format(module_name))
        return redirect(url_for('modules'))
    else:
        raise ServerException('Серверная ошибка', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/server_config', methods=['GET'])
@handle_errors(redirect_path='/server_config')
@auth_required
def server_config():
    import copy
    server_config_obj = copy.copy(SettingsService().server_config)
    del server_config_obj['need_to_auth']
    del server_config_obj['password']
    server_config_obj['possible_machines_types'] = list(SettingsService().machines_configs.keys())
    return render_template('server_settings.html', settings_dict=server_config_obj)


@app.route('/server_config', methods=['POST'])
@handle_errors(redirect_path='/server_config')
@auth_required
def update_server_config():
    new_server_config = request.form
    machine_type = new_server_config.get('type')
    if machine_type:
        if machine_type not in SettingsService().machines_configs.keys():
            raise ServerException('Недопустимый тип робота {}'.format(machine_type), status.HTTP_400_BAD_REQUEST)
    SettingsService().server_config.update(new_server_config)
    SettingsService().save_server_config()
    return redirect(url_for('server_config'))


@app.route('/password', methods=['POST'])
@handle_errors(redirect_path='/server_config', no_401_redirect=True)
@auth_required
def change_password():
    info = request.form
    old_password = info.get('old_password', '')
    new_password = info.get('new_password', '')
    check_new_pass = info.get('new_password_again', '')
    if not new_password:
        raise ServerException('Пароль не может быть пустым', status.HTTP_400_BAD_REQUEST)
    if not (new_password == check_new_pass):
        raise ServerException('Пароли не совпадают', status.HTTP_400_BAD_REQUEST)

    new_token = AuthorizationService().change_password(old_password, new_password)
    session['is_logged'] = True
    session['token'] = new_token
    flash('Пароль успешно изменен', FlashCategoriesClasses.success)
    return redirect(url_for('server_config'))


@app.route('/update_ssh', methods=['POST'])
@handle_errors(redirect_path='/server_config')
@auth_required
def update_ssh():
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
    download_path = os.path.expanduser(SettingsService().server_config['upload_path'])
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    file_path = os.path.join(download_path, file_name)
    file.save(file_path)
    # if ModulesService().update_ssh_key(file_path):
    flash('Ключи успешно обновлены')
    return redirect(url_for('server_config'))
    # else:
    #     raise ServerException('Серверная ошибка', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/test', methods=['POST'])
def test():
    flash('Инфо', FlashCategoriesClasses.info)
    flash('Ошибка', FlashCategoriesClasses.error)
    flash('Успех', FlashCategoriesClasses.success)
    flash('Внимание', FlashCategoriesClasses.warning)
    flash('Дефолт')
    return redirect(url_for('modules'))
