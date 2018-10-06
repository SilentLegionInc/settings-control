from settings_service import SettingsService
from logger import Logger
from flask import flash
from main import bcrypt


def check_user_credentials(username, password):
    user_info = '{}:{}'.format(username, password)
    user_hash = SettingsService().server_config.get('USER_AUTH_HASH', None)
    if not user_hash:
        Logger().critical_message('user auth hash is None!')
        flash('Auth error. Please check user hash on server side')
        raise Exception('Auth error. Please check user hash on server side')

    if not bcrypt.check_password_hash(user_hash, user_info):
        Logger().critical_message('Incorrect username/password')
        flash('Invalid username or password')
        return False

    return True
