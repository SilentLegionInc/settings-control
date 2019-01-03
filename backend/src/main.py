from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from support.logger import Logger
from configuration.settings_service import SettingsService
from flask_login import login_user, login_required, logout_user, current_user
from flask import request, redirect, url_for, jsonify, render_template, Response
from werkzeug.urls import url_parse
from logs_service import LogsService
from support.forms import LoginForm
from support.models import User
from support.helpers import check_user_credentials
from configuration.update_service import UpdateService
from configuration.core_service import CoreService
from functools import wraps
from monitoring.monitoring_data_service import MonitoringDataService
from flask_api import status
from werkzeug.exceptions import HTTP_STATUS_CODES
from support.helpers import ServerException
import traceback
from support.mapper import Mapper
from wireless.wifi_service import WifiService, get_mocked_list


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


# decorator for check authorization via token
# TODO fix (need to pair username\pass)
def api_authorization(func):
    @wraps(func)
    def my_wrapper(*args, **kwargs):
        Logger().info_message('Auth wrapper')
        if not SettingsService().server_config.get('need_to_auth', False):
            Logger().info_message('Mocked authorization. Skip checking')
            return func(*args, **kwargs)
        # TODO use basic auth + request.authorization to get login and password or change it to token...
        auth_header = request.headers.get('authorization', '', str)
        auth = auth_header.split(" ")[1] if auth_header else ''
        if not auth:
            Logger().critical_message('No auth token in header: {}'.format(auth))
            return Response('You need to authorize to access this url', 401)
        else:
            Logger().info_message('{}:{}'.format(app.config.get('USER_AUTH_HASH'), auth))
            if bcrypt.check_password_hash(app.config.get('USER_AUTH_HASH'), auth):
                Logger().info_message('Successful login')
            else:
                Logger().info_message('Incorrect username\password')
                return Response('Incorrect username or password', 401)
        return func(*args, **kwargs)
    return my_wrapper


@app.route('/api/config', methods=['GET', 'POST'])
@api_authorization
def api_config():
    if request.method == 'GET':
        return jsonify(SettingsService().get_core_config(reload_from_disk=True))
    elif request.method == 'POST':
        return jsonify(SettingsService().save_core_config(request.get_json()))


@app.route('/api/wifi', methods=['GET'])
@api_authorization
def api_get_wifi_list():
    # return jsonify(WifiService().list_of_connections())
    return jsonify(get_mocked_list())


@app.route('/api/core/compile', methods=['POST'])
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
        print('wait')
        time.sleep(1)

    return jsonify({'code': 0, 'compile_status': CoreService().compile_status.value})


@app.route('/api/core/run', methods=['POST'])
@api_authorization
def api_run_core():
    CoreService().run_core()
    is_active = CoreService().core_is_active()
    if is_active:
        return jsonify({'code': 0, 'core_status': is_active})
    else:
        return jsonify({'code': 1})


@app.route('/api/core/status', methods=['GET'])
@api_authorization
def api_core_status():
    is_active = CoreService().core_is_active()
    if is_active:
        return jsonify({'code': 0, 'core_status': is_active})
    else:
        return jsonify({'code': 1, 'core_status': is_active})


@app.route('/api/core/stop', methods=['POST'])
@api_authorization
def api_stop_core():
    # TODO add try/catch
    CoreService().stop_core()
    return jsonify({'code': 0})


@app.route('/api/login', methods=['POST'])
def api_login():
    info = request.get_json()
    if check_user_credentials(info.get('login', ''), info.get('password', '')):
        return Response('Success', 200)
    else:
        return Response('Incorrect username or password', 401)


@app.route('/api/logs', methods=['GET'])
def api_logs():
    return jsonify(LogsService().get_logs(request.args.get('limit', 1), request.args.get('offset', 0)))


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
                return Response(HTTP_STATUS_CODES[ex.status_code], ex.status_code)
            else:
                Logger().error_message('Got an unknown exception')
                Logger().error_message(traceback.format_exc())
                return Response(HTTP_STATUS_CODES[status.HTTP_500_INTERNAL_SERVER_ERROR], status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper


@app.route('/api/monitoring/structure/<string:robot_name>', methods=['GET'])
@handle_errors
def api_get_monitoring_data_structure(robot_name):
    return jsonify(MonitoringDataService().get_data_structure(robot_name)), status.HTTP_200_OK


@app.route('/api/monitoring/data/<string:robot_name>', methods=['POST'])
@handle_errors
def api_get_monitoring_data(robot_name):
    body = request.get_json()
    result = MonitoringDataService().get_data(robot_name, **Mapper.map_get_monitoring_data_request(body))
    return jsonify(Mapper.map_get_monitoring_data_response(result)), status.HTTP_200_OK


@app.route('/api/monitoring/logs/<string:robot_name>', methods=['POST'])
@handle_errors
def api_get_monitoring_logs(robot_name):
    body = request.get_json()
    result = MonitoringDataService().get_logs(robot_name, **Mapper.map_get_monitoring_logs_request(body))
    return jsonify(Mapper.map_get_monitoring_logs_response(result)), status.HTTP_200_OK
