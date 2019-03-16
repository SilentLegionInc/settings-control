import datetime
import os
import random
import sqlite3

from dateutil import parser

from monitoring.monitoring_config_service import MonitoringConfigService
from monitoring.monitoring_data_service import ValueTypes
from support.logger import Logger


def generate_close_value(base_value):
    difference = random.uniform(-1, 1)
    return base_value + difference


robot_name = 'AMTS'
table_names_prefix = ''
base_number_value = 245.6
base_string_value = 'sousage'
base_time_value = '2018-11-15T12:00:00'
records_count = 5000

monitoring_config_path = os.path.join(os.getcwd(), '../monitoring/monitoring_config.json')
sensors_config = MonitoringConfigService(monitoring_config_path).get_sensors_data_config(robot_name)
for key, table_config in sensors_config.items():
    id_column_name = table_config['id_column']
    time_column_name = table_config['time_column']
    latitude_column_name = table_config['latitude_field']
    longitude_column_name = table_config['longitude_field']
    number_fields = list(
        map(
            lambda elem: elem[1]['column_name'],
            filter(
                lambda elem: elem[1]['type'] == ValueTypes.NUMBER.value,
                list(table_config['fields_to_retrieve'].items())
            )
        )
    )
    string_fields = list(
        map(
            lambda elem: elem[1]['column_name'],
            filter(
                lambda elem: elem[1]['type'] == ValueTypes.STRING.value,
                list(table_config['fields_to_retrieve'].items())
            )
        )
    )

    time = parser.parse(base_time_value)
    table_name = table_config['collection_name']
    real_table = table_names_prefix + table_name if table_names_prefix else table_name

    try:
        with sqlite3.connect(table_config['file_path']) as connection:
            cursor = connection.cursor()

            cursor.execute('DROP TABLE IF EXISTS {}'.format(real_table))
            create_query = 'CREATE TABLE {}({},{},{},{},{})'.format(
                real_table,
                '{} NUMBER'.format(id_column_name),
                '{} TEXT'.format(time_column_name),
                '{} REAL'.format(latitude_column_name),
                '{} REAL'.format(longitude_column_name),
                ','.join(
                    list(map(lambda elem: '{} REAL'.format(elem), number_fields)) +
                    list(map(lambda elem: '{} TEXT'.format(elem), string_fields))
                )
            )
            cursor.execute(create_query)

            for index in range(0, records_count):
                number_values = [str(generate_close_value(base_number_value)) for i in range(0, len(number_fields))]
                string_values = ['\'{}\''.format(base_string_value)] * len(string_fields)
                insert_query = 'INSERT INTO {} ({},{},{},{},{}) VALUES({},{},{},{},{})'.format(
                    real_table,
                    id_column_name,
                    time_column_name,
                    latitude_column_name,
                    longitude_column_name,
                    ','.join(number_fields + string_fields),
                    index,
                    (time + datetime.timedelta(0, index)).strftime('\'%Y-%m-%d %H:%M:%S\''),
                    random.uniform(-90, 90),
                    random.uniform(-180, 180),
                    ','.join(number_values + string_values)
                )
                cursor.execute(insert_query)
    except Exception as ex:
        Logger().error_message('SQL error while working with {}'.format(table_config['file_path']))

