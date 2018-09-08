# mocked user model
from src import db


class User(db.Model):

    def __init__(self):
        self._id = 1
        self._login = 'Silence'
        self._password = 'Silent'

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
