from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from support.logger import Logger
from configuration.settings_service import SettingsService
from flask_login import login_user, login_required, logout_user, current_user
from flask import request, redirect, url_for, jsonify, render_template
from werkzeug.urls import url_parse
from logs_service import LogsService
from support.forms import LoginForm
from support.models import User
from configuration.update_service import UpdateService
from configuration.core_service import CoreService
from functools import wraps
from monitoring.monitoring_data_service import MonitoringDataService
from flask_api import status
from werkzeug.exceptions import HTTP_STATUS_CODES
from support.server_exception import ServerException
import traceback
from support.mapper import Mapper
from configuration.wireless import WifiService, get_mocked_list, cmd
from monitoring.system_monitoring_service import SystemMonitoringService
from werkzeug.utils import secure_filename
import os
import zipfile
import shutil
from configuration.authoriztaion_service import AuthorizationService
from collections import OrderedDict
from configuration.core_service import ProcessStatus

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


def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            if isinstance(ex, ServerException):
                Logger().error_message('Got an exception')
                Logger().error_message('Message: {}. Code: {}'.format(ex.message, ex.status_code))
                Logger().error_message(traceback.format_exc())
                return jsonify({
                    'ok': False,
                    'errorInfo': ex.message,
                    'errorStatus': HTTP_STATUS_CODES[ex.status_code]
                }), ex.status_code
            else:
                Logger().error_message('Got an unknown exception')
                Logger().error_message(traceback.format_exc())
                return jsonify({
                    'ok': False,
                    'errorInfo': 'Серверная ошибка',
                    'errorStatus': HTTP_STATUS_CODES[status.HTTP_500_INTERNAL_SERVER_ERROR]
                }), status.HTTP_500_INTERNAL_SERVER_ERROR
    return wrapper


# decorator for check authorization via token
def api_authorization(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not SettingsService().server_config.get('need_to_auth', False):
            Logger().info_message('Mocked authorization. Skip checking')
            return func(*args, **kwargs)

        if not request.authorization:
            raise ServerException('Отсутствует заголовок авторизации', status.HTTP_401_UNAUTHORIZED)

        token_uuid = request.authorization.username
        password = request.authorization.password
        AuthorizationService().check_token(token_uuid, password)
        return func(*args, **kwargs)
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        Logger().info_message('Submit login')
        try:
            if not AuthorizationService().check_password(form.password.data, False):
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


@app.route('/api/core_config', methods=['GET', 'POST'])
@handle_errors
@api_authorization
def api_config():
    if request.method == 'GET':
        return jsonify(SettingsService().get_core_config(reload_from_disk=True))
    elif request.method == 'POST':
        return jsonify(SettingsService().save_core_config(request.get_json()))


@app.route('/api/wifi', methods=['GET'])
@handle_errors
@api_authorization
def api_get_wifi_list():
    # return jsonify(WifiService().list_of_connections())
    return jsonify(get_mocked_list())


@app.route('/api/wifi/connect', methods=['POST'])
@handle_errors
@api_authorization
def api_set_wifi():
    # TODO test me, add reconnect if die here core will be isolated...
    params = request.get_json()
    ssid = params.get('name')
    password = params.get('password')
    if WifiService().connect(ssid, password):
        return jsonify({'code': 0}), status.HTTP_200_OK


@app.route('/api/core/compile', methods=['POST'])
@handle_errors
@api_authorization
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
        time.sleep(1)

    return jsonify({'code': 0, 'compile_status': CoreService().compile_status.value})


@app.route('/api/core/run', methods=['POST'])
@handle_errors
@api_authorization
def api_run_core():
    CoreService().run_core()
    is_active = CoreService().core_is_active()
    if is_active:
        return jsonify({'code': 0, 'core_status': is_active})
    else:
        return jsonify({'code': 1})


@app.route('/api/core/status', methods=['GET'])
@handle_errors
@api_authorization
def api_core_status():
    is_active = CoreService().core_is_active()
    if is_active:
        return jsonify({'code': 0, 'core_status': is_active})
    else:
        return jsonify({'code': 1, 'core_status': is_active})


@app.route('/api/core/stop', methods=['POST'])
@handle_errors
@api_authorization
def api_stop_core():
    CoreService().stop_core()
    return jsonify({'code': 0}), status.HTTP_200_OK


@app.route('/api/logs', methods=['GET'])
def api_logs():
    return jsonify(LogsService().get_logs(request.args.get('limit', 1), request.args.get('offset', 0)))


@app.route('/api/login', methods=['POST'])
@handle_errors
def api_login():
    info = request.get_json()
    result = AuthorizationService().check_password(info.get('password', ''), True)
    if result:
        return jsonify({'token': result}), status.HTTP_200_OK


@app.route('/api/logout', methods=['GET'])
@handle_errors
@api_authorization
def api_logout():
    if AuthorizationService().delete_token():
        return jsonify({'code': 0}), status.HTTP_200_OK


@app.route('/api/password', methods=['POST'])
@handle_errors
@api_authorization
def api_change_password():
    info = request.get_json()
    old_password = info.get('oldPassword', '')
    new_password = info.get('newPassword', '')
    new_token = AuthorizationService().change_password(old_password, new_password)
    return jsonify({'token': new_token}), status.HTTP_200_OK


@app.route('/api/monitoring/structure/<string:robot_name>/<string:db_name>', methods=['GET'])
@handle_errors
def api_get_monitoring_data_structure(robot_name, db_name):
    result = MonitoringDataService.get_data_structure(robot_name, db_name)
    return jsonify(Mapper.map_get_monitoring_data_structure_response(result)), status.HTTP_200_OK


@app.route('/api/monitoring/databases_info/<string:robot_name>', methods=['GET'])
@handle_errors
def api_get_monitoring_databases_info(robot_name):
    result = MonitoringDataService.get_databases_info(robot_name)
    return jsonify(Mapper.map_get_monitoring_databases_info_response(result)), status.HTTP_200_OK


@app.route('/api/monitoring/chart_data/<string:robot_name>/<string:db_name>', methods=['POST'])
@handle_errors
def api_get_monitoring_chart_data(robot_name, db_name):
    body = request.get_json()
    result = MonitoringDataService().get_chart_data(robot_name, db_name, **Mapper.map_get_monitoring_chart_data_request(body))
    return jsonify(Mapper.map_get_monitoring_chart_data_response(result)), status.HTTP_200_OK


@app.route('/api/monitoring/table_data/<string:robot_name>/<string:db_name>', methods=['POST'])
@handle_errors
def api_get_monitoring_table_data(robot_name, db_name):
    body = request.get_json()
    result = MonitoringDataService().get_table_data(robot_name, db_name, **Mapper.map_get_monitoring_table_data_request(robot_name, db_name, body))
    return jsonify(Mapper.map_get_monitoring_table_data_response(result, db_name)), status.HTTP_200_OK


@app.route('/api/monitoring/maps_data/<string:robot_name>/<string:db_name>', methods=['GET'])
@handle_errors
def api_get_monitoring_maps_data(robot_name, db_name):
    result = MonitoringDataService().get_maps_data(robot_name, db_name)
    return jsonify(Mapper.map_get_monitoring_maps_data_response(result)), status.HTTP_200_OK


@app.route('/api/monitoring/logs/<string:robot_name>', methods=['POST'])
@handle_errors
def api_get_monitoring_logs(robot_name):
    body = request.get_json()
    result = MonitoringDataService().get_logs(robot_name, **Mapper.map_get_monitoring_logs_request(body))
    return jsonify(Mapper.map_get_monitoring_logs_response(result)), status.HTTP_200_OK


@app.route('/api/monitoring/system_info', methods=['GET'])
@handle_errors
def api_get_system_info():
    if request.args.get('extended') == 'true':
        result = {
            'cpu': SystemMonitoringService().get_cpu_usage(),
            'disk': SystemMonitoringService().get_disks_usage(),
            'memory': SystemMonitoringService().get_memory_usage()
        }
    else:
        result = SystemMonitoringService().get_cpu_usage()

    return jsonify(result), status.HTTP_200_OK


@app.route('/api/build_machine', methods=['POST'])
@handle_errors
@api_authorization
def api_build_current_machine():
    with_update = request.get_json().get('with_update')
    machine_config = SettingsService().current_machine_config
    if not machine_config:
        raise ServerException('Не удалось найти конфигурацию для комплекса: {}'.format(SettingsService().server_config['type']),
                              status.HTTP_500_INTERNAL_SERVER_ERROR)

    dependencies = dict(OrderedDict(sorted(machine_config['dependencies'].items(), key=lambda x: x[1])))
    for dependency in dependencies:
        dependency_url = SettingsService().libraries['dependencies'].get(dependency)
        if not dependency_url:
            raise ServerException('Ошибка сборки. Неизвестная зависимость: {}'.format(dependency),
                                  status.HTTP_500_INTERNAL_SERVER_ERROR)
        if with_update:
            UpdateService().update_and_upgrade_lib_sync(dependency)
        else:
            UpdateService().upgrade_lib_sync(dependency)

    if with_update:
        CoreService().update_core_sync()

    CoreService().compile_core()
    return jsonify({'code': 0}), status.HTTP_200_OK


@app.route('/api/modules', methods=['GET'])
@handle_errors
@api_authorization
def api_get_modules():
    # TODO get all modules?
    machine_config = SettingsService().current_machine_config
    if not machine_config:
        raise ServerException('Не удалось найти конфигурацию для комплекса: {}'.format(SettingsService().server_config['type']),
                              status.HTTP_500_INTERNAL_SERVER_ERROR)

    mapped_dependencies = []
    dependencies = dict(OrderedDict(sorted(machine_config['dependencies'].items(), key=lambda x: x[1])))
    for dependency in dependencies:
        dependency_url = SettingsService().libraries['dependencies'].get(dependency)
        dependency_info = {
            'name': dependency,
            'url': dependency_url,
            'index': dependencies[dependency]
        }
        build_info = UpdateService().built_info(dependency)
        dependency_info['is_built'] = build_info[0]
        dependency_info['build_modify_time'] = build_info[1]

        clone_info = UpdateService().cloned_info(dependency)
        dependency_info['is_cloned'] = clone_info[0]
        dependency_info['src_modify_time'] = clone_info[1]
        mapped_dependencies.append(dependency_info)

    core_info = {
        'name': machine_config['core']['repo_name'],
        'execute': machine_config['core']['executable_name'],
        'config_path': machine_config['core']['config_path'],
        'url': SettingsService().libraries['cores'].get(machine_config['core']['repo_name'])
    }

    core_build_info = CoreService().built_info()
    core_info['is_built'] = core_build_info[0]
    core_info['build_modify_time'] = core_build_info[1]

    core_clone_info = CoreService().cloned_info()
    core_info['is_cloned'] = core_clone_info[0]
    core_info['src_modify_time'] = core_clone_info[1]

    return jsonify({'core': core_info, 'dependencies': mapped_dependencies}), status.HTTP_200_OK


@app.route('/api/update_ssh', methods=['POST'])
@handle_errors
@api_authorization
def api_update_ssh():
    allowed_extensions = {'zip'}

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions

    if 'file' not in request.files:
        raise ServerException('В форме отсутсвтвуют файлы', status.HTTP_400_BAD_REQUEST)

    file = request.files['file']
    if not file or not file.filename:
        raise ServerException('Не найден файл', status.HTTP_400_BAD_REQUEST)

    if not allowed_file(file.filename):
        raise ServerException('Некорректный формат файла. Разрешены только: {}'.format(allowed_extensions),
                              status.HTTP_406_NOT_ACCEPTABLE)

    file_name = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    file.save(file_path)
    zip_archive = zipfile.ZipFile(file_path, 'r')
    zip_archive.extractall(app.config['UPLOAD_FOLDER'])
    zip_archive.close()
    # TODO check
    ssh_path = os.path.expanduser('~/.ssh')
    # TODO need to remove ssh folder?
    cmd('cp -Rf {}/* {}'.format(file_path, ssh_path))
    hosts_file_name = os.path.join(ssh_path, 'known_hosts')
    if os.path.isfile(hosts_file_name):
        os.remove(hosts_file_name)
    os.system('ssh-keyscan ' + SettingsService().server_config['repositories_platform'] + ' >> ' + hosts_file_name)
    return jsonify({'code': 0}), status.HTTP_200_OK


@app.route('/api/utils/health', methods=['GET'])
@handle_errors
def api_get_server_health():
    return jsonify({'code': 0}), status.HTTP_200_OK


@app.route('/api/utils/machine_types', methods=['GET'])
def api_get_machine_types():
    types = list(SettingsService().machines_configs.keys())
    return jsonify({'ok': True, 'result': types}), status.HTTP_200_OK


@app.route('/api/server_config', methods=['GET'])
@handle_errors
@api_authorization
def api_get_server_config():
    import copy
    server_config = copy.copy(SettingsService().server_config)
    del server_config['need_to_auth']
    del server_config['password']
    server_config['possible_machines_types'] = list(SettingsService().machines_configs.keys())
    return jsonify(server_config), status.HTTP_200_OK


@app.route('/api/server_config', methods=['POST'])
@handle_errors
@api_authorization
def api_update_server_config():
    new_server_config = request.get_json()
    machine_type = new_server_config.get('type')
    if machine_type:
        if machine_type not in SettingsService().machines_configs.keys():
            raise ServerException('Недопустимый тип робота {}'.format(machine_type), status.HTTP_400_BAD_REQUEST)
    SettingsService().server_config.update(new_server_config)
    SettingsService().save_server_config()
    return jsonify({'ok': True}), status.HTTP_200_OK


@app.route('/api/clone_module/<string:module_name>', methods=['GET'])
@handle_errors
@api_authorization
def api_clone_module(module_name):
    if module_name in SettingsService().libraries['dependencies']:
        UpdateService().update_lib_sync(module_name)
    elif module_name in SettingsService().libraries['cores']:
        CoreService().update_core_sync()

    return jsonify({'code': 0}), status.HTTP_200_OK


@app.route('/api/build_module/<string:module_name>', methods=['GET'])
@handle_errors
@api_authorization
def api_build_module(module_name):
    (compile_status, compile_output) = (ProcessStatus.DEFAULT, None)
    if module_name in SettingsService().libraries['dependencies']:
        (is_cloned, _) = UpdateService().cloned_info(module_name)
        if not is_cloned:
            UpdateService().update_lib_sync(module_name)
        (compile_status, compile_output) = UpdateService().upgrade_lib_sync(module_name)
    elif module_name in SettingsService().libraries['cores']:
        (is_cloned, _) = CoreService().cloned_info()
        if not is_cloned:
            CoreService().update_core_sync()
        (compile_status, compile_output) = CoreService().compile_core()

    if compile_status is ProcessStatus.SUCCESS:
        return jsonify({'code': 0}), status.HTTP_200_OK
    else:
        raise ServerException('Ошибка сборки. Статус компиляции: {}. Информация о сборке: {}'
                              .format(compile_status, compile_output), status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/api/update_module/<string:module_name>', methods=['POST'])
@handle_errors
@api_authorization
def api_update_module(module_name):
    allowed_extensions = {'zip'}

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions

    if 'file' not in request.files:
        raise ServerException('В форме отсутсвтвуют файлы', status.HTTP_400_BAD_REQUEST)

    file = request.files['file']
    if not file or not file.filename:
        raise ServerException('Не найден файл', status.HTTP_400_BAD_REQUEST)

    if not allowed_file(file.filename):
        raise ServerException('Некорректный формат файла. Разрешены только: {}'.format(allowed_extensions),
                              status.HTTP_406_NOT_ACCEPTABLE)

    file_name = secure_filename(file.filename)

    # TODO refactor, move to separate manager?
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    file.save(file_path)
    zip_archive = zipfile.ZipFile(file_path, 'r')
    zip_archive.extractall(app.config['UPLOAD_FOLDER'])
    zip_archive.close()

    lib_name = module_name
    target_lib_path = os.path.join(
        os.path.expanduser(SettingsService().server_config['sources_path']),
        lib_name
    )
    source_lib_path = os.path.join(app.config['UPLOAD_FOLDER'], lib_name)
    if not os.path.isdir(target_lib_path):
        shutil.rmtree(target_lib_path, ignore_errors=True)
        os.makedirs(target_lib_path)
    cmd('cp -Rf {}/* {}'.format(source_lib_path, target_lib_path))
    # TODO get module name from post request
    if lib_name in SettingsService().libraries['dependencies']:
        UpdateService().upgrade_lib_sync(lib_name)
    elif lib_name in SettingsService().libraries['cores']:
        # TODO check
        CoreService().compile_core()
    else:
        raise ServerException('Неизвестный модуль {}'.format(lib_name), status.HTTP_400_BAD_REQUEST)
    return jsonify({'code': 0}), status.HTTP_200_OK



