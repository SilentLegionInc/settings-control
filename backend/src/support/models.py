# mocked user model
from configuration.settings_service import SettingsService


class User:

    def __init__(self):
        self._id = SettingsService().server_config.get('USER_AUTH_HASH')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self._id
