from toolbelt.support.singleton import Singleton
from toolbelt.support.logger import Logger
import os
import json


class MonitoringConfigService(metaclass=Singleton):

    def __init__(self, monitoring_config_path=os.path.join(os.getcwd(), './monitoring/monitoring_config.json')):
        self._config_path = monitoring_config_path
        self._config = {}

        self.load_config()

    def load_config(self):
        Logger().info_message('Loading monitoring config')
        try:
            config_file = open(self._config_path, 'r')
            self._config = json.loads(config_file.read())
            config_file.close()
        except Exception as ex:
            Logger().error_message('Loading monitoring config error: {}'.format(str(ex)))

    def get_robots_list(self):
        return list(self._config.keys())

    def get_logs_data_config(self, robot_name):
        return self._config.get(robot_name, {}).get("logs_data")

    def get_sensors_data_config(self, robot_name):
        return self._config.get(robot_name, {}).get("sensors_data")

    def get_full_config(self, robot_name):
        return self._config.get(robot_name, None)

