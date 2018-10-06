# mocked user model
from main import app


class User:

    def __init__(self):
        self._id = app.config.get('USER_AUTH_HASH')

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
