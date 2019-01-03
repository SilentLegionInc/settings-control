from configuration.settings_service import SettingsService
from flask import flash
import base64
from flask_api import status


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


def check_password(password, return_token=False):
    stored_pass = SettingsService().server_config.get('password')
    if not stored_pass:
        flash('Auth error. Please check user hash on server side')
        raise ServerException('Auth error. Please check user hash on server side', status.HTTP_500_INTERNAL_SERVER_ERROR)
    if password == stored_pass:
        if return_token:
            return 'Basic ${}'.format(base64.b64encode(':${}'.format(password).encode()).decode('utf-8'))
        else:
            return True
    else:
        flash('Invalid password')
        raise ServerException('Incorrect password', status.HTTP_401_UNAUTHORIZED)

