from singleton import Singleton
from logger import Logger
from monitoring.monitoring_config_service import MonitoringConfigService
import sqlite3
import datetime


class MonitoringDataService(metaclass=Singleton):

    def __init__(self):
        self.connections = {}
        robot_names = MonitoringConfigService().get_robots_list()

        try:
            for robot_name in robot_names:
                self.connections[robot_name] = {
                    'logs': {},
                    'sensors': {}
                }

                logs_db_file_path = MonitoringConfigService().get_logs_data_config(robot_name)['file_path']
                logs_collection_name = MonitoringConfigService().get_logs_data_config(robot_name)['collection_name']
                self.connections[robot_name]['logs']['connection'] = _connection = sqlite3.connect(logs_db_file_path)
                self.connections[robot_name]['logs']['collection_name'] = logs_collection_name

                sensors_db_file_path = MonitoringConfigService().get_sensors_data_config(robot_name)['file_path']
                sensors_collection_name = MonitoringConfigService().get_sensors_data_config(robot_name)['collection_name']
                self.connections[robot_name]['sensors']['connection'] = sqlite3.connect(sensors_db_file_path)
                self.connections[robot_name]['sensors']['collection_name'] = sensors_collection_name
        except Exception as ex:
            Logger().error_message('Monitoring create connections error: {}'.format(str(ex)))

    def get_data_structure(self, robot_name):
        fields_descr = MonitoringConfigService().get_sensors_data_config(robot_name)["fields_to_retrieve"]
        result = []
        for key, value in fields_descr.items():
            result.append({
                "system_name": key,
                "name": value["name"],
                "type": value["type"]
            })
        return result

    def get_logs(self):
        pass

    # Запеканий нет, потому что их нет в sqlite3, а то, что есть, - фигня
    def get_data(self, robot_name, field_name, start_time=None, end_time=None, limit=None, offset=None):
        cursor = self.connections[robot_name]['sensors']['connection'].cursor()
        collection_name = self.connections[robot_name]['sensors']['collection_name']

        try:
            sensors_config = MonitoringConfigService().get_sensors_data_config(robot_name)
            needed_column_name = sensors_config['fields_to_retrieve'][field_name]["column_name"]
            time_column_name = sensors_config['time_column']

            main_query = 'SELECT {},{} FROM {}'.format(time_column_name, needed_column_name, collection_name)

            condition_query = ''
            if start_time and end_time:
                if isinstance(start_time, datetime.datetime):
                    start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(end_time, datetime.datetime):
                    end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
                condition_query = ' WHERE datetime({}) >= datetime("{}") AND datetime({}) <= datetime("{}")'.format(time_column_name, start_time, time_column_name, end_time)
            elif start_time:
                if isinstance(start_time, datetime.datetime):
                    start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
                condition_query = ' WHERE datetime({}) >= datetime("{}")'.format(time_column_name, start_time)
            elif end_time:
                if isinstance(end_time, datetime.datetime):
                    end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
                condition_query = ' WHERE datetime({}) <= datetime("{}")'.format(time_column_name, end_time)

            sort_query = ' ORDER BY datetime({}) DESC'.format(time_column_name)

            additional_query = ''
            if limit:
                additional_query += ' LIMIT {}'.format(limit)

            if offset:
                additional_query += ' OFFSET {}'.format(offset)

            query = main_query + condition_query + sort_query + additional_query
            cursor.execute(query)
            result = []
            for row in cursor:
                result.append({
                    'time': row[0],
                    'value': row[1]
                })

            main_query = 'SELECT COUNT(*) FROM {}'.format(collection_name)
            query = main_query + condition_query
            cursor.execute(query)
            count = cursor.fetchone()[0]

            return {'result': result, 'count': count}
        except Exception as ex:
            Logger().error_message('Monitoring getting data error: {}'.format(str(ex)))


if __name__ == '__main__':
    structure = MonitoringDataService().get_data_structure('AMTS')
    print(structure)
    data = MonitoringDataService().get_data('AMTS', 'atmospheric_sensor', '2018-11-25 18:31:03', datetime.datetime.now())
    print(data)


