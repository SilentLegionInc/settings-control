from configuration.modules_service import ModulesService
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from support.helper import allowed_file_extension
from support.logger import Logger
from configuration.settings_service import SettingsService
from flask_login import login_user, login_required, logout_user, current_user
from flask import request, redirect, url_for, jsonify, render_template
from werkzeug.urls import url_parse
from support.forms import LoginForm
from support.models import User
from functools import wraps
from monitoring.monitoring_data_service import MonitoringDataService
from flask_api import status
from werkzeug.exceptions import HTTP_STATUS_CODES
from support.server_exception import ServerException
import traceback
from support.mapper import Mapper
from configuration.wireless import NetworkService
from monitoring.system_monitoring_service import SystemMonitoringService
from werkzeug.utils import secure_filename
import os
from configuration.authoriztaion_service import AuthorizationService

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
        if SettingsService().save_core_config(result):
            Logger().info_message('Saved')
        else:
            Logger().info_message('Error')
        return render_template('config.html', config=SettingsService().get_core_config(reload_from_disk=True))

# HERE STARTS API ENDPOINTS #


@app.route('/modules', methods=['GET'])
@login_required
def modules():
    res = ModulesService().get_modules_list()
    return render_template('modules.html', core=res['core_info'], dependencies=res['mapped_dependencies'])


# ---------------------API endpoints-------------------------------
@app.route('/api/core_config', methods=['GET', 'POST'])
@handle_errors
@api_authorization
def api_config():
    if request.method == 'GET':
        return jsonify(SettingsService().get_core_config(reload_from_disk=True))
    elif request.method == 'POST':
        return jsonify(SettingsService().save_core_config(request.get_json()))

# NETWORKS API #


@app.route('/api/network', methods=['GET'])
@handle_errors
@api_authorization
def api_get_wifi_list():
    return jsonify(NetworkService().list_of_connections()), status.HTTP_200_OK


@app.route('/api/network/create_wifi_connection', methods=['POST'])
@handle_errors
@api_authorization
def api_connect_to_new_wifi():
    params = request.get_json()
    ssid = params.get('name')
    password = params.get('password')
    if NetworkService().create_wifi_connection(ssid, password):
        return jsonify({'ok': True}), status.HTTP_200_OK


@app.route('/api/network/connection/up/<string:uuid>', methods=['GET'])
@handle_errors
@api_authorization
def api_connection_up(uuid):
    # This is connect to known connection
    if NetworkService().connection_up(uuid):
        return jsonify({'ok': True}), status.HTTP_200_OK


@app.route('/api/network/connection/down/<string:uuid>', methods=['GET'])
@handle_errors
@api_authorization
def api_connection_down(uuid):
    # This is connect to known connection
    if NetworkService().connection_down(uuid):
        return jsonify({'ok': True}), status.HTTP_200_OK


@app.route('/api/network/connection/<string:uuid>', methods=['POST'])
@handle_errors
@api_authorization
def api_connection_modify(uuid):
    # modify connection
    params = request.get_json()
    if NetworkService().modify_connection_params(uuid, params):
        return jsonify({'ok': True}), status.HTTP_200_OK


@app.route('/api/network/connection/<string:uuid>', methods=['DELETE'])
@handle_errors
@api_authorization
def api_connection_delete(uuid):
    # delete connection
    if NetworkService().delete_connection(uuid):
        return jsonify({'ok': True}), status.HTTP_200_OK


@app.route('/api/network/connection/drop_all_wireless', methods=['DELETE'])
@handle_errors
@api_authorization
def api_connections_delete_all_wireless():
    # delete connection
    if NetworkService().delete_all_wireless_connections():
        return jsonify({'ok': True}), status.HTTP_200_OK


@app.route('/api/network/connection/<string:uuid>', methods=['PUT'])
@handle_errors
@api_authorization
def api_modify_connection(uuid):
    params = request.get_json()
    if NetworkService().modify_connection_params(uuid, params):
        return jsonify({'ok': True}), status.HTTP_200_OK

# AUTH API #


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
        return jsonify({'ok': True}), status.HTTP_200_OK


@app.route('/api/password', methods=['POST'])
@handle_errors
@api_authorization
def api_change_password():
    info = request.get_json()
    old_password = info.get('oldPassword', '')
    new_password = info.get('newPassword', '')
    new_token = AuthorizationService().change_password(old_password, new_password)
    return jsonify({'token': new_token}), status.HTTP_200_OK

# MONITORING API #


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


@app.route('/api/monitoring/chart_data/<string:robot_name>/<string:db_name>/<string:field_name>', methods=['GET', 'POST'])
@handle_errors
def api_get_monitoring_chart_data(robot_name, db_name, field_name):
    if request.method == 'POST':
        if request.args.get('page') == 'true':
            body = request.get_json()
            result = MonitoringDataService().get_page_chart_data(
                robot_name, db_name, field_name, **Mapper.map_get_monitoring_page_chart_data_request(body)
            )
            return jsonify(Mapper.map_monitoring_chart_data_result(result)), status.HTTP_200_OK
        else:
            body = request.get_json()
            result = MonitoringDataService().get_filter_chart_data(
                robot_name, db_name, field_name, **Mapper.map_get_monitoring_filter_chart_data_request(body)
            )
            return jsonify(Mapper.map_get_monitoring_filter_chart_data_response(result)), status.HTTP_200_OK
    if request.method == 'GET':
        interval_size = int(request.args.get('interval_size'))
        result = MonitoringDataService().get_init_chart_data(robot_name, db_name, field_name, interval_size)
        return jsonify(Mapper.map_get_monitoring_init_chart_data_response(result)), status.HTTP_200_OK


@app.route('/api/monitoring/table_data/<string:robot_name>/<string:db_name>', methods=['POST'])
@handle_errors
def api_get_monitoring_table_data(robot_name, db_name):
    body = request.get_json()
    result = MonitoringDataService().get_table_data(robot_name, db_name, **Mapper.map_get_monitoring_table_data_request(robot_name, db_name, body))
    return jsonify(Mapper.map_get_monitoring_table_data_response(result, db_name)), status.HTTP_200_OK


@app.route('/api/monitoring/maps_data/<string:robot_name>/<string:db_name>', methods=['GET', 'POST'])
@handle_errors
def api_get_monitoring_maps_data(robot_name, db_name):
    if request.method == 'GET':
        result = MonitoringDataService().get_numeric_fields(robot_name, db_name)
        return jsonify(Mapper.map_get_numeric_fields_response(result)), status.HTTP_200_OK
    elif request.method == 'POST':
        body = request.get_json()
        result = MonitoringDataService().get_maps_data(robot_name, db_name, **Mapper.map_get_monitoring_maps_data_request(body))
        return jsonify(Mapper.map_get_monitoring_maps_data_response(result)), status.HTTP_200_OK
    else:
        return None, status.HTTP_404_NOT_FOUND


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


@app.route('/api/utils/info', methods=['GET'])
@handle_errors
def api_get_server_info():
    response_body = {
        'robot_type': SettingsService().server_config['type'],
        'ok': True
    }
    return jsonify(response_body), status.HTTP_200_OK

# CONFIG API #


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

# MODULES API #


@app.route('/api/pull_machine', methods=['POST'])
@handle_errors
@api_authorization
def api_clone_current_machine():
    if ModulesService().pull_machine():
        return jsonify({'ok': True}), status.HTTP_200_OK
    else:
        raise ServerException('Серверная ошибка', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/api/build_machine', methods=['POST'])
@handle_errors
@api_authorization
def api_build_current_machine():
    if ModulesService().build_machine():
        return jsonify({'ok': True}), status.HTTP_200_OK
    else:
        raise ServerException('Серверная ошибка', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/api/modules', methods=['GET'])
@handle_errors
@api_authorization
def api_get_modules():
    result = ModulesService().get_modules_list()
    return jsonify(result), status.HTTP_200_OK


@app.route('/api/update_ssh', methods=['POST'])
@handle_errors
@api_authorization
def api_update_ssh():
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
    if ModulesService().update_ssh_key:
        return jsonify({'ok': True}), status.HTTP_200_OK
    else:
        raise ServerException('Серверная ошибка', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/api/core/run', methods=['POST'])
@handle_errors
@api_authorization
def api_run_core():
    if ModulesService().run_core():
        return jsonify({'ok': True}), status.HTTP_200_OK
    else:
        raise ServerException('Не удалось запустить ядро', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/api/core/status', methods=['GET'])
@handle_errors
@api_authorization
def api_core_status():
    is_active = ModulesService().core_is_active()
    return jsonify({'ok': True, 'core_status': is_active}), status.HTTP_200_OK


@app.route('/api/core/stop', methods=['POST'])
@handle_errors
@api_authorization
def api_stop_core():
    if ModulesService().stop_core():
        return jsonify({'ok': True}), status.HTTP_200_OK
    else:
        raise ServerException('Не удалось остановить ядро', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/api/pull_module/<string:module_name>', methods=['GET'])
@handle_errors
@api_authorization
def api_pull_module(module_name):
    if ModulesService().pull_module(module_name):
        return jsonify({'ok': True}), status.HTTP_200_OK
    else:
        raise ServerException('Серверная ошибка', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/api/build_module/<string:module_name>', methods=['GET'])
@handle_errors
@api_authorization
def api_build_module(module_name):
    if ModulesService().build_module(module_name):
        return jsonify({'ok': True}), status.HTTP_200_OK
    else:
        raise ServerException('Серверная ошибка', status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route('/api/manual_module_update/<string:module_name>', methods=['POST'])
@handle_errors
@api_authorization
def api_manual_module_update(module_name):
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
        return jsonify({'ok': True}), status.HTTP_200_OK
    else:
        raise ServerException('Серверная ошибка', status.HTTP_500_INTERNAL_SERVER_ERROR)



