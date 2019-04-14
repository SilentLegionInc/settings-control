from flask_api import status
from toolbelt.support.server_exception import ServerException
from toolbelt.support.singleton import Singleton
from toolbelt.support.logger import Logger
import json
import os


class SettingsService(metaclass=Singleton):
    def __init__(self, server_config_path=os.getcwd() + '/config.conf'):
        self._server_config_path = server_config_path
        self._server_config = {}  # server it is me
        self._core_config = {}  # core is c++ core

        self.load_server_config()

    @property
    def private_server_config(self):
        return self._server_config.get('private_server_config', {})

    @property
    def server_config(self):
        return self._server_config.get('server_config', {})

    # get element from machines block with current server type
    @property
    def current_machine_config(self):
        return self._server_config.get('machines', {}).get(self.server_config.get('type'))

    @property
    def machines_configs(self):
        return self._server_config.get('machines', {})

    @property
    def libraries(self):
        return self._server_config.get('libraries', {})

    def get_monitoring_robots_list(self):
        return list(self._server_config.get('monitoring_config', {}).keys())

    def get_monitoring_logs_data_config(self, robot_name):
        return self._server_config.get('monitoring_config', {}).get(robot_name, {}).get("logs_data")

    def get_monitoring_sensors_data_config(self, robot_name):
        return self._server_config.get('monitoring_config', {}).get(robot_name, {}).get("sensors_data")

    def get_monitoring_full_config(self, robot_name):
        return self._server_config.get('monitoring_config', {}).get(robot_name, None)

    def get_core_config(self, reload_from_disk=False):
        if reload_from_disk:
            if not self.load_core_config():
                return {}
        return self._core_config

    # load config file for python server
    def load_server_config(self):
        Logger().info_message('Loading server config')
        try:
            config_file = open(self._server_config_path, 'r')
            self._server_config = json.loads(config_file.read())
            config_file.close()
        except Exception as ex:
            error_text = 'Ошибка загрузки конфигурации сервера: {}'.format(str(ex))
            Logger().error_message(error_text)
            raise ServerException(error_text, status.HTTP_500_INTERNAL_SERVER_ERROR)
        Logger().info_message('Server config successfully loaded')
        return True

    # save config file for python server
    def save_server_config(self):
        Logger().info_message('Saving server config')
        try:
            config_file = open(self._server_config_path, 'w')
            config_file.write(json.dumps(self._server_config))
            config_file.close()
        except Exception as ex:
            error_text = 'Ошибка загрузки конфигурации сервера: {}'.format(str(ex))
            Logger().error_message(error_text)
            raise ServerException(error_text, status.HTTP_500_INTERNAL_SERVER_ERROR)
        Logger().info_message('Server config successfully saved')
        return True

    # load config file for c++ core
    def load_core_config(self):
        try:
            path_to_current_core_config = os.path.expanduser(
                os.path.join(self.server_config.get('sources_path'),
                             self.current_machine_config.get('core', {}).get('repo_name'),
                             self.current_machine_config.get('core', {}).get('config_path'))
            )
            Logger().info_message(
                'Loading core config for {} from {}'.format(self.server_config['type'], path_to_current_core_config))
            if not os.path.exists(path_to_current_core_config):
                raise ServerException('Файл конфигурации ядра не найден в: {}'.format(path_to_current_core_config))
            config_file = open(path_to_current_core_config, 'r')
            self._core_config = json.loads(config_file.read())
            config_file.close()
        except Exception as ex:
            error_text = 'Ошибка загрузки конфигурации ядра: {}'.format(str(ex))
            Logger().error_message(error_text)
            raise ServerException(error_text, status.HTTP_500_INTERNAL_SERVER_ERROR)
        return True

    # save config to file for c++ core
    def save_core_config(self, config):
        try:
            path_to_current_core_config = os.path.expanduser(
                os.path.join(self.server_config.get('sources_path'),
                             self.current_machine_config.get('core', {}).get('repo_name'),
                             self.current_machine_config.get('core', {}).get('config_path'))
            )
            Logger().info_message('Saving core config for {} to {}'.format(self.server_config['type'],
                                                                           path_to_current_core_config))
            if not os.path.exists(path_to_current_core_config):
                raise Exception('Файл конфигурации ядра не найден в: {}'.format(path_to_current_core_config))
            self._core_config = config
            config_file = open(path_to_current_core_config, 'w')
            config_file.write(json.dumps(self._core_config))
            config_file.close()
        except Exception as ex:
            error_text = 'Ошибка сохранения конфигурации ядра: {}'.format(str(ex))
            Logger().error_message(error_text)
            raise ServerException(error_text, status.HTTP_500_INTERNAL_SERVER_ERROR)
        Logger().info_message('Core config successfully saved')
        return True


