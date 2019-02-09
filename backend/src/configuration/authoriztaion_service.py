from support.singleton import Singleton
from configuration.settings_service import SettingsService
from flask import flash
import base64
from flask_api import status
import uuid
from support.server_exception import ServerException


class AuthorizationService(metaclass=Singleton):
    def __init__(self):
        self.token_uuid = None

    def delete_token(self):
        if self.token_uuid:
            self.token_uuid = None
            return True
        else:
            raise ServerException('Can\'t find current user token. Need to auth via log in method',
                                  status.HTTP_401_UNAUTHORIZED)

    def check_token(self, token_uuid, password):
        if self.token_uuid:
            token_correct = self.token_uuid == token_uuid
            if not token_correct:
                # TODO another error code?
                raise ServerException('Can\'t find current user token. Need to auth via log in method',
                                      status.HTTP_401_UNAUTHORIZED)

            if self.check_password(password, return_token=False):
                return True
        else:
            raise ServerException('Can\'t find current user token. Need to auth via log in method',
                                  status.HTTP_401_UNAUTHORIZED)

    # use it to auth first time, when already logged in need to use check_token
    def check_password(self, password, return_token=False):
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
                self.token_uuid = token_uuid
                return token
            else:
                return True
        else:
            flash('Invalid password')
            raise ServerException('Incorrect password', status.HTTP_401_UNAUTHORIZED)

    def change_password(self, old_password, new_password):
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
            self.token_uuid = token_uuid
            return token
        else:
            flash('Invalid current password')
            raise ServerException('Incorrect current password', status.HTTP_400_BAD_REQUEST)