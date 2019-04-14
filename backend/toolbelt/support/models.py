from toolbelt.support.settings_service import SettingsService


# mocked user model
class User:
    def __init__(self):
        self._id = SettingsService().server_config.get('password')

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
