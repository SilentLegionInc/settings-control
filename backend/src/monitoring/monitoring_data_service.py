from enum import Enum
from support.singleton import Singleton
from support.logger import Logger
from monitoring.monitoring_config_service import MonitoringConfigService
import copy
import sqlite3
import datetime
from flask_api import status
from support.server_exception import ServerException
from dateutil import parser


class ValueTypes(Enum):
    NUMBER = 'number'


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
                self.connections[robot_name]['logs']['file_path'] = logs_db_file_path
                self.connections[robot_name]['logs']['collection_name'] = logs_collection_name

                sensors_db_file_path = MonitoringConfigService().get_sensors_data_config(robot_name)['file_path']
                sensors_collection_name = MonitoringConfigService().get_sensors_data_config(robot_name)['collection_name']
                self.connections[robot_name]['sensors']['file_path'] = sensors_db_file_path
                self.connections[robot_name]['sensors']['collection_name'] = sensors_collection_name
        except Exception as ex:
            raise ServerException('Can\'t get information from config', status.HTTP_500_INTERNAL_SERVER_ERROR, ex)

    @staticmethod
    def get_data_structure(robot_name):
        try:
            fields_descr = MonitoringConfigService().get_sensors_data_config(robot_name)["fields_to_retrieve"]
        except Exception as ex:
            raise ServerException('Can\'t get information from config', status.HTTP_500_INTERNAL_SERVER_ERROR, ex)
        result = []
        for key, value in fields_descr.items():
            result.append({
                "system_name": key,
                "name": value["name"],
                "type": value["type"]
            })
        return result

    # Запеканий нет, потому что их нет в sqlite3, а то, что есть, - фигня
    def get_chart_data(self, robot_name, field_name, filter_params=None, additional_params=None):
        if filter_params:
            filter_params = copy.deepcopy(filter_params)
            pass
        else:
            filter_params = {}

        if additional_params:
            additional_params = copy.deepcopy(additional_params)
        else:
            additional_params = {}

        try:
            connection = sqlite3.connect(self.connections[robot_name]['sensors']['file_path'])
            cursor = connection.cursor()
        except Exception as ex:
            raise ServerException(
                'Can\'t connect to database with name {}'.format(self.connections[robot_name]['sensors']['file_path']),
                status.HTTP_500_INTERNAL_SERVER_ERROR, ex
            )

        collection_name = self.connections[robot_name]['sensors']['collection_name']

        try:
            sensors_config = MonitoringConfigService().get_sensors_data_config(robot_name)
            needed_column_name = sensors_config['fields_to_retrieve'][field_name]["column_name"]
            time_column_name = sensors_config['time_column']
            latitude_column_name = sensors_config['latitude_field']
            longitude_column_name = sensors_config['longitude_field']

            main_query = 'SELECT {},{},{},{} FROM {}'.format(
                time_column_name,
                needed_column_name,
                latitude_column_name,
                longitude_column_name,
                collection_name
            )

            # handling filter conditions
            filter_conditions = []
            if filter_params.get('start_time') is not None:
                if isinstance(filter_params['start_time'], datetime.datetime):
                    filter_params['start_time'] = filter_params['start_time'].strftime("%Y-%m-%d %H:%M:%S")
                filter_conditions.append('datetime({}) >= datetime("{}")'.format(time_column_name, filter_params['start_time']))
            if filter_params.get('end_time') is not None:
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
            if additional_params.get('limit') is not None:
                additional_conditions.append('limit {}'.format(additional_params['limit']))
            if additional_params.get('offset') is not None:
                additional_conditions.append('offset {}'.format(additional_params['offset']))

            additional_query = ''
            if additional_conditions:
                additional_query = ' '.join(additional_conditions)

            query = ' '.join([main_query, filter_query, sort_query, additional_query])

            Logger().debug_message(query, "get_charts_data :: Sensors database query: ")

            cursor.execute(query)
            result = []
            for row in cursor:
                result.append({
                    'time': parser.parse(row[0]),
                    'value': row[1],
                    'latitude': row[2],
                    'longitude': row[3]
                })

            main_query = 'SELECT COUNT(*), MIN({}), AVG({}), MAX({}) FROM {}'.format(
                needed_column_name, needed_column_name, needed_column_name, collection_name
            )
            query = ' '.join([main_query, filter_query])

            Logger().debug_message(query, "get_charts_data :: Sensors database query: ")

            cursor.execute(query)
            support_result = cursor.fetchone()

            count = support_result[0]
            minimum = support_result[1]
            average = support_result[2]
            maximum = support_result[3]

            cursor.close()
            connection.close()

            return {'result': result, 'count': count, 'minimum': minimum, 'average': average, 'maximum': maximum}
        except Exception as ex:
            cursor.close()
            connection.close()
            raise ServerException('Error while preparing and executing query', status.HTTP_500_INTERNAL_SERVER_ERROR, ex)

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

        try:
            connection = sqlite3.connect(self.connections[robot_name]['logs']['file_path'])
            cursor = connection.cursor()
        except Exception as ex:
            raise ServerException(
                'Can\'t connect to database with name {}'.format(self.connections[robot_name]['logs']['file_path']),
                status.HTTP_500_INTERNAL_SERVER_ERROR, ex
            )

        collection_name = self.connections[robot_name]['logs']['collection_name']

        id_column_name = 'id'
        time_column_name = 'dataTime'
        type_column_name = 'type'
        title_column_name = 'title'
        message_column_name = 'mess'

        try:
            main_query = 'SELECT {},{},{},{},{} FROM {}'.format(
                id_column_name, time_column_name, type_column_name,
                title_column_name, message_column_name, collection_name
            )

            # handling filter conditions
            filter_conditions = []
            if filter_params.get('start_time') is not None:
                if isinstance(filter_params['start_time'], datetime.datetime):
                    filter_params['start_time'] = filter_params['start_time'].strftime("%Y-%m-%d %H:%M:%S")
                filter_conditions.append('datetime({}) >= datetime("{}")'.format(time_column_name, filter_params['start_time']))
            if filter_params.get('end_time') is not None:
                if isinstance(filter_params['end_time'], datetime.datetime):
                    filter_params['end_time'] = filter_params['end_time'].strftime("%Y-%m-%d %H:%M:%S")
                filter_conditions.append('datetime({}) <= datetime("{}")'.format(time_column_name, filter_params['end_time']))
            if filter_params.get('type') is not None:
                filter_conditions.append('{} = {}'.format(type_column_name, filter_params['type']))

            filter_query = ''
            if filter_conditions:
                filter_query = 'WHERE ' + ' AND '.join(filter_conditions)

            # handling sort conditions
            sort_conditions = []
            if sort_params.get('type') is not None:
                sort_conditions.append('type {}'.format(sort_params['type']))
            if sort_params.get('time') is not None:
                sort_conditions.append('dataTime {}'.format(sort_params['time']))

            sort_query = ''
            if sort_conditions:
                sort_query = 'ORDER BY ' + ' '.join(sort_conditions)

            # handling additional conditions
            additional_conditions = []
            if additional_params.get('limit') is not None:
                additional_conditions.append('limit {}'.format(additional_params['limit']))
            if additional_params.get('offset') is not None:
                additional_conditions.append('offset {}'.format(additional_params['offset']))

            additional_query = ''
            if additional_conditions:
                additional_query = ' '.join(additional_conditions)

            query = ' '.join([main_query, filter_query, sort_query, additional_query])

            Logger().debug_message(query, "get_logs :: Logs database query: ")

            cursor.execute(query)
            result = []
            for row in cursor:
                result.append({
                    'id': row[0],
                    'time': parser.parse(row[1]),
                    'type': row[2],
                    'title': row[3],
                    'message': row[4]
                })

            main_query = 'SELECT COUNT(*) FROM {}'.format(collection_name)
            query = ' '.join([main_query, filter_query])

            Logger().debug_message(query, "get_logs :: Logs database query: ")

            cursor.execute(query)
            count = cursor.fetchone()[0]

            cursor.close()
            connection.close()

            return {'result': result, 'count': count}
        except Exception as ex:
            cursor.close()
            connection.close()
            raise ServerException('Error while preparing and executing query', status.HTTP_500_INTERNAL_SERVER_ERROR, ex)

    def get_maps_data(self, robot_name):
        try:
            connection = sqlite3.connect(self.connections[robot_name]['sensors']['file_path'])
            cursor = connection.cursor()
        except Exception as ex:
            raise ServerException(
                'Can\'t connect to database with name {}'.format(self.connections[robot_name]['sensors']['file_path']),
                status.HTTP_500_INTERNAL_SERVER_ERROR, ex
            )

        collection_name = self.connections[robot_name]['sensors']['collection_name']

        try:
            sensors_config = MonitoringConfigService().get_sensors_data_config(robot_name)
            latitude_column_name = sensors_config['latitude_field']
            longitude_column_name = sensors_config['longitude_field']

            query = 'SELECT {},{},COUNT(*) FROM {} group by {},{}'.format(
                latitude_column_name,
                longitude_column_name,
                collection_name,
                latitude_column_name,
                longitude_column_name
            )

            Logger().debug_message(query, "get_maps_data :: Sensors database query: ")

            cursor.execute(query)
            points_result = []
            for row in cursor:
                points_result.append({
                    'latitude': row[0],
                    'longitude': row[1],
                    'count': row[2]
                })

            query = 'SELECT  MIN({}),MIN({}),MAX({}),MAX({}) FROM {}'.format(
                latitude_column_name,
                longitude_column_name,
                latitude_column_name,
                longitude_column_name,
                collection_name
            )

            Logger().debug_message(query, "get_maps_data :: Sensors database query: ")

            cursor.execute(query)

            support_result = cursor.fetchone()
            min_latitude = support_result[0]
            min_longitude = support_result[1]
            max_latitude = support_result[2]
            max_longitude = support_result[3]

            cursor.close()
            connection.close()

            return {
                'points': points_result,
                'center_latitude': (min_latitude + max_latitude) / 2,
                'center_longitude': (min_longitude + max_longitude) / 2
            }
        except Exception as ex:
            cursor.close()
            connection.close()
            raise ServerException('Error while preparing and executing query', status.HTTP_500_INTERNAL_SERVER_ERROR, ex)

    def get_table_data(self, robot_name, filter_params=None, sort_params=None, additional_params=None):
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

        try:
            connection = sqlite3.connect(self.connections[robot_name]['sensors']['file_path'])
            cursor = connection.cursor()
        except Exception as ex:
            raise ServerException(
                'Can\'t connect to database with name {}'.format(self.connections[robot_name]['sensors']['file_path']),
                status.HTTP_500_INTERNAL_SERVER_ERROR, ex
            )

        collection_name = self.connections[robot_name]['sensors']['collection_name']

        try:
            sensors_config = MonitoringConfigService().get_sensors_data_config(robot_name)
            time_column_name = sensors_config['time_column']
            latitude_column_name = sensors_config['latitude_field']
            longitude_column_name = sensors_config['longitude_field']
            needed_fields = list(sensors_config['fields_to_retrieve'].items())
            fields_to_filter = list(
                filter(
                    lambda elem: elem[1]['type'] == ValueTypes.NUMBER.value,
                    list(sensors_config['fields_to_retrieve'].items())
                )
            )

            main_query = 'SELECT {},{},{},{} FROM {}'.format(
                time_column_name,
                latitude_column_name,
                longitude_column_name,
                ','.join(list(map(lambda elem: elem[1]['column_name'], needed_fields))),
                collection_name
            )

            # handling filter conditions
            filter_conditions = []
            if filter_params.get('start_time') is not None:
                if isinstance(filter_params['start_time'], datetime.datetime):
                    filter_params['start_time'] = filter_params['start_time'].strftime("%Y-%m-%d %H:%M:%S")
                filter_conditions.append('datetime({}) >= datetime("{}")'.format(time_column_name, filter_params['start_time']))
            if filter_params.get('end_time') is not None:
                if isinstance(filter_params['end_time'], datetime.datetime):
                    filter_params['end_time'] = filter_params['end_time'].strftime("%Y-%m-%d %H:%M:%S")
                filter_conditions.append('datetime({}) <= datetime("{}")'.format(time_column_name, filter_params['end_time']))
            for field_to_filter in fields_to_filter:
                min_name = 'min_{}'.format(field_to_filter[0])
                max_name = 'max_{}'.format(field_to_filter[0])
                if filter_params.get(min_name) is not None:
                    filter_conditions.append('{} >= {}'.format(field_to_filter[1]['column_name'], filter_params[min_name]))
                if filter_params.get(max_name) is not None:
                    filter_conditions.append('{} <= {}'.format(field_to_filter[1]['column_name'], filter_params[max_name]))

            filter_query = ''
            if filter_conditions:
                filter_query = 'WHERE ' + ' AND '.join(filter_conditions)

            # handling sort conditions
            sort_conditions = []
            if sort_params.get('time') is not None:
                sort_conditions.append('{} {}'.format(time_column_name, sort_params['time']))
            for needed_field in needed_fields:
                if sort_params.get(needed_field[0]) is not None:
                    sort_conditions.append('{} {}'.format(needed_field[1]['column_name'], sort_params[needed_field[0]]))

            sort_query = ''
            if sort_conditions:
                sort_query = 'ORDER BY ' + ' '.join(sort_conditions)

            # handling additional conditions
            additional_conditions = []
            if additional_params.get('limit') is not None:
                additional_conditions.append('limit {}'.format(additional_params['limit']))
            if additional_params.get('offset') is not None:
                additional_conditions.append('offset {}'.format(additional_params['offset']))

            additional_query = ''
            if additional_conditions:
                additional_query = ' '.join(additional_conditions)

            query = ' '.join([main_query, filter_query, sort_query, additional_query])

            Logger().debug_message(query, "get_table_data :: Sensors database query: ")

            cursor.execute(query)
            result = []
            for row in cursor:
                res_elem = {
                    'time': parser.parse(row[0]),
                    'latitude': row[1],
                    'longitude': row[2]
                }
                for index, needed_field in enumerate(needed_fields):
                    res_elem[needed_field[0]] = row[3 + index]
                result.append(res_elem)

            main_query = 'SELECT COUNT(*) FROM {}'.format(collection_name)
            query = ' '.join([main_query, filter_query])

            Logger().debug_message(query, "get_table_data :: Sensors database query: ")

            cursor.execute(query)
            count = cursor.fetchone()[0]

            cursor.close()
            connection.close()

            return {
                'result': result,
                'count': count,
                'data_structure': self.get_data_structure(robot_name),
                'extended': additional_params.get('extended')
            }
        except Exception as ex:
            cursor.close()
            connection.close()
            raise ServerException('Error while preparing and executing query', status.HTTP_500_INTERNAL_SERVER_ERROR, ex)


if __name__ == '__main__':
    structure = MonitoringDataService.get_data_structure('AMTS')
    print(structure)

    test_filter = {
        'start_time': '2018-11-25 18:31:03',
        'end_time': datetime.datetime.now()
    }
    data = MonitoringDataService().get_chart_data('AMTS', 'atmospheric_sensor', filter_params=test_filter)
    print(data)

    test_filter = {
        'start_time': '2018-08-19T11:10:17.187',
        'end_time': datetime.datetime.now()
    }
    logs = MonitoringDataService().get_logs('AMTS', filter_params=test_filter)
    print(logs)

