from singleton import Singleton
from logger import Logger
from monitoring.monitoring_config_service import MonitoringConfigService
import copy
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

    # Запеканий нет, потому что их нет в sqlite3, а то, что есть, - фигня
    def get_data(self, robot_name, field_name, filter_params=None, additional_params=None):
        if filter_params:
            filter_params = copy.deepcopy(filter_params)
            pass
        else:
            filter_params = {}

        if additional_params:
            additional_params = copy.deepcopy(additional_params)
        else:
            additional_params = {}

        cursor = self.connections[robot_name]['sensors']['connection'].cursor()
        collection_name = self.connections[robot_name]['sensors']['collection_name']

        try:
            sensors_config = MonitoringConfigService().get_sensors_data_config(robot_name)
            needed_column_name = sensors_config['fields_to_retrieve'][field_name]["column_name"]
            time_column_name = sensors_config['time_column']
            latitude_column_name = sensors_config['latitude_field']
            longitude_column_name = sensors_config['longitude_field']

            main_query = 'SELECT {},{},{},{} FROM {}'.format(time_column_name, needed_column_name, latitude_column_name, longitude_column_name, collection_name)

            # handling filter conditions
            filter_conditions = []
            if filter_params.get('start_time'):
                if isinstance(filter_params['start_time'], datetime.datetime):
                    filter_params['start_time'] = filter_params['start_time'].strftime("%Y-%m-%d %H:%M:%S")
                filter_conditions.append('datetime({}) >= datetime("{}")'.format(time_column_name, filter_params['start_time']))
            if filter_params.get('end_time'):
                if isinstance(filter_params['end_time'], datetime.datetime):
                    filter_params['end_time'] = filter_params['end_time'].strftime("%Y-%m-%d %H:%M:%S")
                filter_conditions.append('datetime({}) <= datetime("{}")'.format(time_column_name, filter_params['end_time']))

            filter_query = ''
            if filter_conditions:
                filter_query = 'WHERE ' + ' AND '.join(filter_conditions)

            # handling sort conditions
            sort_query = 'ORDER BY datetime({}) DESC'.format(time_column_name)

            # handling additional conditions
            additional_conditions = []
            if additional_params.get('limit'):
                additional_conditions.append('limit {}'.format(additional_params['limit']))
            if additional_params.get('offset'):
                additional_conditions.append('offset {}'.format(additional_params['offset']))

            additional_query = ''
            if additional_conditions:
                additional_query = ' '.join(additional_conditions)

            query = ' '.join([main_query, filter_query, sort_query, additional_query])
            cursor.execute(query)
            result = []
            for row in cursor:
                result.append({
                    'time': row[0],
                    'value': row[1],
                    'latitude': row[2],
                    'longitude': row[3]
                })

            main_query = 'SELECT COUNT(*) FROM {}'.format(collection_name)
            query = ' '.join([main_query, filter_query])
            cursor.execute(query)
            count = cursor.fetchone()[0]

            return {'result': result, 'count': count}
        except Exception as ex:
            Logger().error_message('Monitoring getting data error: {}'.format(str(ex)))

    # Запеканий нет, потому что их нет в sqlite3, а то, что есть, - фигня
    def get_logs(self, robot_name, filter_params=None, sort_params=None, additional_params=None):
        if filter_params:
            filter_params = copy.deepcopy(filter_params)
            pass
        else:
            filter_params = {}

        if sort_params:
            sort_params = copy.deepcopy(sort_params)
        else:
            sort_params = {}

        if additional_params:
            additional_params = copy.deepcopy(additional_params)
        else:
            additional_params = {}

        cursor = self.connections[robot_name]['logs']['connection'].cursor()
        collection_name = self.connections[robot_name]['logs']['collection_name']

        time_column_name = 'dataTime'
        type_column_name = 'type'
        title_column_name = 'title'
        message_column_name = 'mess'

        try:
            main_query = 'SELECT {},{},{},{} FROM {}'.format(time_column_name, type_column_name, title_column_name, message_column_name, collection_name)

            # handling filter conditions
            filter_conditions = []
            if filter_params.get('start_time'):
                if isinstance(filter_params['start_time'], datetime.datetime):
                    filter_params['start_time'] = filter_params['start_time'].strftime("%Y-%m-%d %H:%M:%S")
                filter_conditions.append('datetime({}) >= datetime("{}")'.format(time_column_name, filter_params['start_time']))
            if filter_params.get('end_time'):
                if isinstance(filter_params['end_time'], datetime.datetime):
                    filter_params['end_time'] = filter_params['end_time'].strftime("%Y-%m-%d %H:%M:%S")
                filter_conditions.append('datetime({}) <= datetime("{}")'.format(time_column_name, filter_params['end_time']))
            if filter_params.get('type'):
                filter_conditions.append('{} <= {}'.format(type_column_name, filter_params['type']))

            filter_query = ''
            if filter_conditions:
                filter_query = 'WHERE ' + ' AND '.join(filter_conditions)

            # handling sort conditions
            sort_conditions = []
            if sort_params.get('type'):
                order = 'ASC' if sort_params['type'] == 1 else 'DESC'
                sort_conditions.append('type {}'.format(order))
            if sort_params.get('time'):
                order = 'ASC' if sort_params['time'] == 1 else 'DESC'
                sort_conditions.append('time {}'.format(order))

            sort_query = ''
            if sort_conditions:
                sort_query = 'ORDER BY ' + ' '.join(sort_conditions)

            # handling additional conditions
            additional_conditions = []
            if additional_params.get('limit'):
                additional_conditions.append('limit {}'.format(additional_params['limit']))
            if additional_params.get('offset'):
                additional_conditions.append('offset {}'.format(additional_params['offset']))

            additional_query = ''
            if additional_conditions:
                additional_query = ' '.join(additional_conditions)

            query = ' '.join([main_query, filter_query, sort_query, additional_query])
            cursor.execute(query)
            result = []
            for row in cursor:
                result.append({
                    'time': row[0],
                    'type': row[1],
                    'title': row[2],
                    'message': row[3]
                })

            main_query = 'SELECT COUNT(*) FROM {}'.format(collection_name)
            query = ' '.join([main_query, filter_query])
            cursor.execute(query)
            count = cursor.fetchone()[0]

            return {'result': result, 'count': count}
        except Exception as ex:
            Logger().error_message('Monitoring getting logs error: {}'.format(str(ex)))


if __name__ == '__main__':
    structure = MonitoringDataService().get_data_structure('AMTS')
    print(structure)

    filter_params = {
        'start_time': '2018-11-25 18:31:03',
        'end_time': datetime.datetime.now()
    }
    data = MonitoringDataService().get_data('AMTS', 'atmospheric_sensor', filter_params=filter_params)
    print(data)

    filter_params = {
        'start_time': '2018-08-19T11:10:17.187',
        'end_time': datetime.datetime.now()
    }
    logs = MonitoringDataService().get_logs('AMTS', filter_params=filter_params)
    print(logs)

