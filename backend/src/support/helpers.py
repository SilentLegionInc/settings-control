from configuration.settings_service import SettingsService
from support.logger import Logger
from flask import flash


class ServerException(Exception):
    def __init__(self, message, status_code, exception=Exception()):
        super(ServerException, self).__init__(exception)
        self._message = message
        self._status_code = status_code
        pass

    @property
    def message(self):
        return self._message

    @property
    def status_code(self):
        return self._status_code


def check_user_credentials(username, password):
    from main import bcrypt
    user_info = '{}:{}'.format(username, password)
    user_hash = SettingsService().server_config.get('authorization', None)
    if not user_hash:
        Logger().critical_message('user auth hash is None!')
        flash('Auth error. Please check user hash on server side')
        raise Exception('Auth error. Please check user hash on server side')

    if not bcrypt.check_password_hash(user_hash, user_info):
        Logger().critical_message('Incorrect username/password')
        flash('Invalid username or password')
        return False

    return True
