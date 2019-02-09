from configuration.settings_service import SettingsService
from flask import flash
import base64
from flask_api import status
import uuid


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


def delete_token():
    from main import app
    current_token_uuid = app.config.get('token_uuid')
    if current_token_uuid:
        del app.config['token_uuid']
        return True
    else:
        raise ServerException('Can\'t find current user token. Need to auth via log in method',
                              status.HTTP_401_UNAUTHORIZED)


# TODO move it to auth manager?
def check_token(token_uuid, password):
    from main import app
    current_token_uuid = app.config.get('token_uuid')
    if current_token_uuid:
        token_correct = current_token_uuid == token_uuid
        if not token_correct:
            # TODO another error code?
            raise ServerException('Can\'t find current user token. Need to auth via log in method',
                                  status.HTTP_401_UNAUTHORIZED)

        if check_password(password, return_token=False):
            return True
    else:
        raise ServerException('Can\'t find current user token. Need to auth via log in method',
                              status.HTTP_401_UNAUTHORIZED)


# use it to auth first time, when already logged in need to use check_token
def check_password(password, return_token=False):
    from main import app
    stored_pass = SettingsService().server_config.get('password')
    if not stored_pass:
        flash('Auth error. Please check user password on server side')
        raise ServerException('Auth error. Please check user password on server side',
                              status.HTTP_500_INTERNAL_SERVER_ERROR)
    if password == stored_pass:
        if return_token:
            token_uuid = str(uuid.uuid4())
            token = 'Basic {}'.format(base64.b64encode('{}:{}'.format(token_uuid,
                                                                      password).encode()).decode('utf-8'))
            app.config['token_uuid'] = token_uuid
            return token
        else:
            return True
    else:
        flash('Invalid password')
        raise ServerException('Incorrect password', status.HTTP_401_UNAUTHORIZED)


def change_password(old_password, new_password):
    from main import app
    stored_pass = SettingsService().server_config.get('password')
    if not stored_pass:
        flash('Auth error. Please check user password on server side')
        raise ServerException('Auth error. Please check user password on server side',
                              status.HTTP_500_INTERNAL_SERVER_ERROR)

    if old_password == stored_pass:
        SettingsService().server_config['password'] = new_password
        SettingsService().save_server_config()
        token_uuid = str(uuid.uuid4())
        token = 'Basic {}'.format(base64.b64encode('{}:{}'.format(token_uuid,
                                                                  new_password).encode()).decode('utf-8'))
        app.config['token_uuid'] = token_uuid
        return token
    else:
        flash('Invalid current password')
        raise ServerException('Incorrect current password', status.HTTP_400_BAD_REQUEST)


