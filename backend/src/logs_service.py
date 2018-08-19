from src.singleton import Singleton
from src.logger import Logger
import os
import sqlite3
from sqlite3 import Error

class LogsService(metaclass=Singleton):
    def __init__(self):
        try:
            self.connection = sqlite3.connect('../../logdb.db')
        except Error as e:
            Logger().error_message(e)

    def get_logs(self, limit, offset):
        cursor = self.connection.cursor()

        t = (limit, offset)
        try:
            cursor.execute('SELECT * FROM log LIMIT ? OFFSET ?', t)
        except Error as e:
            Logger().error_message(e)
            return {'code': 1, 'error': e}

        result = []
        for row in cursor:
            result.append({
                'id': row[0],
                'time': row[1],
                'type': row[2],
                'title': row[3],
                'message': row[4]
            })

        try:
            cursor.execute('SELECT COUNT(*) FROM log')
        except Error as e:
            Logger().error_message(e)
            return {'code': 1, 'error': e}

        count = cursor.fetchone()

        return {'code': 0, 'result': result, 'count': count}

