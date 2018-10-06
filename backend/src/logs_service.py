from singleton import Singleton
from logger import Logger
import os
import sqlite3
from sqlite3 import Error

class LogsService(metaclass=Singleton):
    def get_logs(self, limit, offset):
        try:
            self.connection = sqlite3.connect('../../logdb.db')
            cursor = self.connection.cursor()

            t = (limit, offset)
            cursor.execute('SELECT * FROM log LIMIT ? OFFSET ?', t)
            result = []
            for row in cursor:
                result.append({
                    'id': row[0],
                    'time': row[1],
                    'type': row[2],
                    'title': row[3],
                    'message': row[4]
                })

            cursor.execute('SELECT COUNT(*) FROM log')
            count = cursor.fetchone()[0]

            return {'code': 0, 'result': result, 'count': count}

        except Error as e:
            Logger().error_message(e)
            return {'code': 1, 'error': e}

    def __del__(self):
        self.connection.close()

