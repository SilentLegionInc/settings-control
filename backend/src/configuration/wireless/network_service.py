from abc import ABCMeta, abstractmethod
import subprocess
from time import sleep
from packaging import version
from support.singleton import Singleton
from support.server_exception import ServerException
from configuration.settings_service import SettingsService
from flask_api import status
import atexit
import json
import os
import re
# set static ip:  nmcli con modify wireless_clone ipv4.addresses 192.168.1.100/24 ipv4.method manual
# ipv4.gateway 192.168.1.1 ipv4.dns 8.8.4.4 && nmcli con down wireless_clone && nmcli con up wireless_clone


# send a command to the shell and return the result
def cmd(command):
    return subprocess.Popen(
        command, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    ).stdout.read().decode()


# abstracts class of Wifi configurator
class NetworkService(metaclass=Singleton):
    _driver_name = None
    _driver = None

    def __call__(self):
        self.refresh_interfaces()

    # init
    def __init__(self, interface_wifi=None, interface_eth=None,
                 detail_connection_params=SettingsService().private_server_config['detail_connection_params']):
        # detect and init appropriate driver
        self._driver_name = self._detect_driver()
        if self._driver_name == 'nmcli0990':
            self._driver = Nmcli0990(interface_wifi=interface_wifi, interface_eth=interface_eth,
                                     detail_connection_params=detail_connection_params)

        self.refresh_interfaces()

        # raise an error if there is still no interface defined
        if self.interface_wifi() is None and self.interface_eth() is None:
            raise Exception('Не удалось найти ни одного сетевого интерфейса')

    @staticmethod
    def _detect_driver():
        # try nmcli (Ubuntu 14.04, 16.04, 18.04)
        response = cmd('which nmcli')
        if len(response) > 0 and 'not found' not in response:
            response = cmd('nmcli --version')
            parts = response.split()
            ver = parts[-1]
            if version.parse(ver) > version.parse('0.9.9.0'):
                return 'nmcli0990'
            else:
                return 'nmcli'

        raise Exception('Unable to find compatible nmcli driver.')

    def refresh_interfaces(self):
        # attempt to auto detect the wifi interface if none was provided
        if self.interface_wifi() is None:
            interfaces = self.interfaces_wifi()
            if interfaces:
                self.interface_wifi(interfaces[0])

        # attempt to auto detect the ethernet interface if none was provided
        if self.interface_eth() is None:
            interfaces = self.interfaces_eth()
            if interfaces:
                self.interface_eth(interfaces[0])

    def connection_up(self, uuid):
        return self._driver.connection_up(uuid)

    def connection_down(self, uuid):
        return self._driver.connection_down(uuid)

    def create_wifi_connection(self, ssid, password):
        return self._driver.create_wifi_connection(ssid, password)

    def delete_connection(self, uuid):
        return self._driver.delete_connection(uuid)

    def modify_connection_params(self, uuid, params_dict):
        return self._driver.modify_connection_params(uuid, params_dict)

    # uuid of current wi-fi connection
    def current_wifi(self):
        return self._driver.current_wifi()

    # uuid of current eth connection
    def current_eth(self):
        return self._driver.current_eth()

    def interfaces_wifi(self):
        return self._driver.interfaces_wifi()

    def interfaces_eth(self):
        return self._driver.interfaces_eth()

    # return the current wireless adapter
    def interface_wifi(self, interface=None):
        return self._driver.interface_wifi(interface)

    def interface_eth(self, interface=None):
        return self._driver.interface_eth(interface)

    # return the current wireless adapter
    def power_wifi(self, power=None):
        return self._driver.power_wifi(power)

    # return the driver name
    def driver(self):
        return self._driver_name

    def list_of_connections(self, rescan_wifi=True):
        return self._driver.list_of_connections(rescan_wifi)


# abstract class for all wifi drivers
class NetworkDriver(metaclass=ABCMeta):

    @abstractmethod
    def current_wifi(self):
        pass

    @abstractmethod
    def current_eth(self):
        pass

    @abstractmethod
    def interfaces_wifi(self):
        pass

    @abstractmethod
    def modify_connection_params(self, connection_uuid, params_dict):
        pass

    @abstractmethod
    def create_wifi_connection(self, ssid, password):
        pass

    @abstractmethod
    def connection_up(self, connection_uuid):
        pass

    @abstractmethod
    def connection_down(self, connection_uuid):
        pass

    @abstractmethod
    def delete_connection(self, connection_uuid):
        pass

    @abstractmethod
    def interfaces_eth(self):
        pass

    @abstractmethod
    def interface_wifi(self, interface=None):
        pass

    @abstractmethod
    def interface_eth(self, interface=None):
        pass

    @abstractmethod
    def power_wifi(self, power=None):
        pass

    @abstractmethod
    def list_of_connections(self, rescan_wifi=True):
        pass


# Linux nmcli Driver >= 0.9.9.0 (Actual driver)
class Nmcli0990(NetworkDriver):
    _interface_wifi = None
    _interface_eth = None

    # init
    def __init__(self, interface_wifi=None, interface_eth=None,
                 detail_connection_params=None):
        self.interface_wifi(interface_wifi)
        self.interface_eth(interface_eth)
        self.ssid_to_uuid = {}
        self._load_connection_map()
        self._detail_connection_params = detail_connection_params
        # register destructor method
        # TODO doesn't work
        atexit.register(self._save_connection_map)

    def _save_connection_map(self):
        print('saving connections map')
        with open('settings_tool_backend_connection_map', 'w') as f:
            f.write(json.dumps(self.ssid_to_uuid))
        return True

    def _load_connection_map(self):
        if os.path.isfile('settings_tool_backend_connection_map'):
            with open('settings_tool_backend_connection_map', 'r') as f:
                json_data = f.read()
                if json_data:
                    self.ssid_to_uuid = json.loads(json_data)
                    return
        self.ssid_to_uuid = {}

    # clean up connections where partial is part of the connection name
    # this is needed to prevent the following error after extended use:
    # 'maximum number of pending replies per connection has been reached'
    def _delete_connection_by_name(self, name):
        # list matching connections
        # TODO check what will be if we delete last wired connection?
        command = 'nmcli -t -f UUID,NAME con show | grep wireless | grep -w {}'.format(name)
        if self.ssid_to_uuid.get(name):
            del self.ssid_to_uuid[name]
        response = cmd(command)
        # delete all of the matching connections
        for line in response.splitlines():
            if line:
                connection_uuid = line.split(':')[0]
                cmd('nmcli con delete {}'.format(connection_uuid))

    # ignore warnings in nmcli output
    # sometimes there are warnings but we connected just fine
    @staticmethod
    def _error_in_response(response):
        # no error if no response
        if not response:
            return False

        # loop through each line
        for line in response.splitlines():
            # all error lines start with 'Error'
            if line.startswith('Error'):
                return True

        # if we didn't find an error then we are in the clear
        return False

    def _get_detailed_record_info(self, search_str, connection_type=''):
        result = {}
        response = cmd('nmcli -t -f NAME,UUID,AUTOCONNECT,TYPE con show | grep {} | grep -w {}'
                       .format(connection_type, search_str))
        if self._error_in_response(response):
            print('Error in get detailed info {}'.format(response))
            return result

        if response:
            splitted = response.split(':')
            result['id'] = splitted[1]
            result['autoconnect'] = splitted[2] == 'yes'
            if self._detail_connection_params:
                fields = ','.join(self._detail_connection_params)
                detail_response = cmd('nmcli -t -f {} con show {}'.format(fields, result['id']))
                if self._error_in_response(detail_response):
                    print('Cant find detail fields {} of connection {}. Response: {}'.format(fields, result['id'], detail_response))
                    return result
                params_fields = detail_response.splitlines()
                result['params'] = {}
                for field_str in params_fields:
                    splitted_field = field_str.split(':')
                    field_key = splitted_field[0]
                    field_value = splitted_field[1]
                    result['params'][field_key] = field_value

        else:
            print('Cant find connection by {}'.format(search_str))
            return result
        return result

    def _get_wifi_list(self):
        response = cmd('nmcli -t -f SSID,MODE,CHAN,FREQ,RATE,SIGNAL,SECURITY,DEVICE,ACTIVE dev wifi list')
        if self._error_in_response(response):
            raise ServerException('Не удалось получить список беспроводных соеденений. Ответ команды: {}'
                                  .format(response), status.HTTP_500_INTERNAL_SERVER_ERROR)
        connections = response.splitlines()
        mapped = []
        need_to_save_map = False
        for connection in connections:
            splitted_array = connection.split(':')
            record = {
                'name': splitted_array[0],
                'id': self.ssid_to_uuid.get(splitted_array[0]),
                'type': 'wifi',
                'mode': splitted_array[1],
                'channel': splitted_array[2],
                'frequency': splitted_array[3],
                'speed_rate': splitted_array[4],
                'signal_level': splitted_array[5],
                'security_type': splitted_array[6],
                'device': splitted_array[7],
                'active': splitted_array[8] == 'yes',
            }

            search_str = record['id'] if record['id'] else record['name']
            detail_record_info = self._get_detailed_record_info(search_str, 'wireless')
            if detail_record_info.get('id'):
                record['id'] = detail_record_info['id']
                self.ssid_to_uuid[record['name']] = record['id']
                need_to_save_map = True
            record['autoconnect'] = detail_record_info.get('autoconnect', None)
            record['params'] = detail_record_info.get('params', {})

            mapped.append(record)

        if need_to_save_map:
            self._save_connection_map()
        # sorted_list = list(sorted(mapped, key=lambda k: k['signal_level'], reverse=True))
        return mapped

    def _get_eth_list(self):
        response = cmd('nmcli -t -f NAME,UUID,TYPE,DEVICE,ACTIVE,AUTOCONNECT con show | grep ethernet')
        if self._error_in_response(response):
            raise ServerException('Не удалось получить список проводных соеденений. Ответ команды: {}'.format(response))
        connections = response.splitlines()
        mapped = []
        for connection in connections:
            splitted_array = connection.split(':')
            record = {
                'name': splitted_array[0],
                'id': splitted_array[1],
                'type': 'eth',
                'device': splitted_array[3],
                'active': splitted_array[4] == 'yes',
                'autoconnect': splitted_array[5] == 'yes'
            }

            search_str = record['id'] if record['id'] else record['name']
            detail_record_info = self._get_detailed_record_info(search_str, 'ethernet')
            record['autoconnect'] = detail_record_info.get('autoconnect', None)
            record['params'] = detail_record_info.get('params', {})

            mapped.append(record)
        return mapped

    def connection_up(self, connection_uuid):
        response = cmd('nmcli con up {}'.format(connection_uuid))
        if self._error_in_response(response):
            if 'unknown connection' in response:
                raise ServerException('Неизвестный идентификатор соединения {}'.format(connection_uuid), status.HTTP_400_BAD_REQUEST)
            elif 'device could not be readied' in response:
                raise ServerException('Не удалось активировать соединение. Девайс недоступен', status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                # TODO add logger
                raise ServerException('Серверная ошибка', status.HTTP_500_INTERNAL_SERVER_ERROR)
        return True

    def connection_down(self, connection_uuid):
        response = cmd('nmcli con down {}'.format(connection_uuid))
        if self._error_in_response(response):
            if 'unknown connection' in response:
                raise ServerException('Неизвестный идентификатор соединения {}'.format(connection_uuid),
                                      status.HTTP_400_BAD_REQUEST)
            elif 'device could not be readied' in response:
                raise ServerException('Не удалось активировать соединение. Девайс недоступен',
                                      status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                # TODO add logger
                raise ServerException('Серверная ошибка', status.HTTP_500_INTERNAL_SERVER_ERROR)
        return True

    def delete_connection(self, connection_uuid):
        response = cmd('nmcli con delete {}'.format(connection_uuid))
        if self._error_in_response(response):
            if 'unknown connection' in response:
                raise ServerException('Неизвестный идентификатор соединения {}'.format(connection_uuid),
                                      status.HTTP_400_BAD_REQUEST)
            else:
                # TODO add logger
                raise ServerException('Серверная ошибка', status.HTTP_500_INTERNAL_SERVER_ERROR)

        name_regex = r".*'(?P<name>.*)'.*"
        ssid = re.findall(name_regex, response)[0]
        if self.ssid_to_uuid.get(ssid):
            del self.ssid_to_uuid[ssid]
            self._save_connection_map()
        return True

    def current_wifi(self):
        # list active connections for all interfaces
        response = cmd('nmcli -t -f UUID,TYPE con show --active | grep wireless')

        # the current network is in the first column
        for line in response.splitlines():
            if line:
                return line.split(':')[0]

        # return none if there was not an active connection
        return None

    def current_eth(self):
        # list active connections for all interfaces
        response = cmd('nmcli -t -f UUID,TYPE con show --active | grep ethernet')

        # the current network is in the first column
        for line in response.splitlines():
            if line:
                return line.split(':')[0]

        # return none if there was not an active connection
        return None

    def modify_connection_params(self, connection_uuid, params_dict):
        # if we don't provide params to modify then return sucess status
        if not params_dict:
            return True
        params_string = ''
        for key in params_dict:
            params_string += '{} {} '.format(key, params_dict[key])
        command = 'nmcli con modify {} {} && nmcli && nmcli con up {}'.format(connection_uuid, params_string, connection_uuid)
        response = cmd(command)
        if self._error_in_response(response):
            # TODO check error type, add logger
            raise ServerException(response, status.HTTP_400_BAD_REQUEST)
        else:
            return True

    def create_wifi_connection(self, ssid, password):
        if self.ssid_to_uuid.get(ssid):
            # if connection already exists just up it
            return self.connection_up(self.ssid_to_uuid[ssid])
        # trying to connect
        response = cmd('nmcli dev wifi connect {} password {} iface {}'.format(
            ssid, password, self._interface_wifi))
        # parse response
        # TODO if error need to up old connection or autoconnect?
        if self._error_in_response(response):
            # TODO check error type invalid password or smth another
            print(response)
            raise ServerException(response, status.HTTP_400_BAD_REQUEST)
        else:
            # trying to fetch uuid from response from nmcli
            connection_uuid = response.split(' ')[-1].replace("'", '').replace('.', '').replace('\n', '')
            self.ssid_to_uuid[ssid] = connection_uuid
            self._save_connection_map()
            return True

    def list_of_connections(self, rescan_wifi=True):
        if rescan_wifi and self.interface_wifi() is not None:
            res = ''
            while 'immediately' not in res:
                res = cmd('nmcli dev wifi rescan')
                sleep(0.5)
            sleep(1)

        answer = {
            'wired': self._get_eth_list(),
            'wireless': self._get_wifi_list()
        }
        return answer

    def interfaces_wifi(self):
        # grab list of interfaces
        response = cmd('nmcli -t dev | grep wifi')

        # parse response
        interfaces = []
        for line in response.splitlines():
            # this line has our interface name in the first column
            interfaces.append(line.split(':')[0])

        # return list
        return interfaces

    def interfaces_eth(self):
        # grab list of interfaces
        response = cmd('nmcli -t dev | grep ethernet')

        # parse response
        interfaces = []
        for line in response.splitlines():
            # this line has our interface name in the first column
            interfaces.append(line.split(':')[0])

        # return list
        return interfaces

    # TODO refactor to get\set
    # return the current wireless adapter
    def interface_wifi(self, interface=None):
        if interface is not None:
            self._interface_wifi = interface
        else:
            return self._interface_wifi

    def interface_eth(self, interface=None):
        if interface is not None:
            self._interface_eth = interface
        else:
            return self._interface_eth

    # TODO refactor to get\set
    def power_wifi(self, power=None):
        if power is True:
            cmd('nmcli r wifi on')
        elif power is False:
            cmd('nmcli r wifi off')
        else:
            if self.interface_wifi() is not None:
                response = cmd('nmcli r wifi')
                return 'enabled' in response
            else:
                return False


if __name__ == '__main__':
    test_connection_uuid = 'e6d4847b-ce3f-466b-9cd5-bd3f31d94891'
    params = {
        'ipv4.addresses': '192.168.1.100/24',
        'ipv4.method': 'manual',
        'ipv4.gateway': '192.168.1.1',
        'ipv4.dns': '8.8.4.4'
    }
    print(NetworkService().list_of_connections())
    # print('Changed connection static params result: {}'.format(NetworkService().modify_connection_params(test_connection_uuid, params)))
    # params = {
    #     'ipv4.method': 'auto'
    # }
    # print('Changed connection dynamic params result: {}'.format(NetworkService().modify_connection_params(test_connection_uuid, params)))
    # print('Changed connection empty params result: {}'.format(NetworkService().modify_connection_params(test_connection_uuid, {})))
    # NetworkService().delete_connection('370a8d53-a80c-42e1-b82c-63ded0db8581')
    # NetworkService().create_wifi_connection('Silencium', 'KeepSilence')
    # NetworkService().create_wifi_connection('Silencium', 'KeepSilence')
