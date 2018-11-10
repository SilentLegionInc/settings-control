from singleton import Singleton
from logger import Logger
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
    def core_build_config(self):
        return self._server_config.get('machines', {}).get(self.server_config.get('type'))

    @property
    def libraries(self):
        return self._server_config.get('libraries')

    def get_core_config(self, reload_from_disk=False):
        if reload_from_disk:
            res = self.load_core_config()
            if not (res['code'] == 0):
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
            Logger().error_message('Loading server config error: {}'.format(str(ex)))
            return {'code': 1, 'error': str(ex)}
        Logger().info_message('Server config successfully loaded')
        return {'code': 0}

    # save config file for python server
    def save_server_config(self):
        Logger().info_message('Saving server config')
        try:
            config_file = open(self._server_config_path, 'w')
            config_file.write(json.dumps(self.server_config))
            config_file.close()
        except Exception as ex:
            Logger().error_message('Loading server config error: {}'.format(str(ex)))
            return {'code': 1, 'error': str(ex)}
        Logger().info_message('Server config successfully saved')
        return {'code': 0}

    # load config file for c++ core
    def load_core_config(self):
        Logger().info_message('Loading core config for {} from {}'.format(self.server_config['type'], self.server_config['core_config_path']))
        try:
            config_file = open(self.server_config['core_config_path'], 'r')
            self._core_config = json.loads(config_file.read())
            config_file.close()
        except Exception as ex:
            Logger().error_message('Loading core config error: {}'.format(str(ex)))
            return {'code': 1, 'error': str(ex)}
        return self._core_config

    # save config to file for c++ core
    def save_core_config(self, config):
        Logger().info_message('Saving core config for {} to {}'.format(self.server_config['type'], self.server_config['core_config_path']))
        try:
            self._core_config = config
            config_file = open(self.server_config['core_config_path'], 'w')
            config_file.write(json.dumps(self._core_config))
            config_file.close()
        except Exception as ex:
            Logger().error_message('Saving core config error: {}'.format(str(ex)))
            return {'code': 1, 'error': str(ex)}
        Logger().info_message('Core config successfully saved')
        return {'code': 0}


