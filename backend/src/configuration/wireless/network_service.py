from abc import ABCMeta, abstractmethod
import subprocess
from time import sleep
from packaging import version
from support.singleton import Singleton
from support.server_exception import ServerException
from flask_api import status
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

    # init
    def __init__(self, interface=None):
        # detect and init appropriate driver
        self._driver_name = self._detect_driver()
        if self._driver_name == 'nmcli0990':
            self._driver = Nmcli0990(interface=interface)

        # attempt to auto detect the interface if none was provided
        if self.interface() is None:
            interfaces = self.interfaces()
            if len(interfaces) > 0:
                self.interface(interfaces[0])

        # raise an error if there is still no interface defined
        if self.interface() is None:
            raise Exception('Unable to auto-detect the network interface.')

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

    def connection_up(self, uuid):
        pass

    def connection_down(self, uuid):
        pass

    def create_connection(self):
        pass

    def delete_connection(self, uuid):
        pass

    def change_connection_dhcp_mode(self, uuid, dhcp):
        pass

    # def connect(self, uuid=None, ssid=None, password=None):

    # connect to a network
    # def connect(self, ssid, password):
    #     return self._driver.connect(ssid, password)

    # return the ssid of the current network
    def current(self):
        return self._driver.current()

    # return a list of wireless adapters
    def interfaces(self):
        return self._driver.interfaces()

    # return the current wireless adapter
    def interface(self, interface=None):
        return self._driver.interface(interface)

    # return the current wireless adapter
    def power(self, power=None):
        return self._driver.power(power)

    # return the driver name
    def driver(self):
        return self._driver_name

    def list_of_connections(self, rescan=True):
        # TODO scan eth, wifi (ssids) match uuid of connection with ssid if possible
        return self._driver.list_of_connections(rescan)


# abstract class for all wifi drivers
class NetworkDriver(metaclass=ABCMeta):

    @abstractmethod
    def connect(self, ssid, password):
        pass

    @abstractmethod
    def current(self):
        pass

    @abstractmethod
    def interfaces(self):
        pass

    @abstractmethod
    def interface(self, interface=None):
        pass

    @abstractmethod
    def power(self, power=None):
        pass

    @abstractmethod
    def list_of_connections(self, rescan=True):
        pass

    # @abstractmethod
    # def detail_connection_info(self):
    #     pass


class NewNmcli0990(NetworkDriver):
    _interface = None

    # init
    def __init__(self, interface=None):
        self.interface(interface)
        # TODO persist
        self.ssid_to_connection_map = {}

    # clean up connections where partial is part of the connection name
    # this is needed to prevent the following error after extended use:
    # 'maximum number of pending replies per connection has been reached'
    @staticmethod
    def _clean(partial):
        # list matching connections
        response = cmd('nmcli --fields UUID,NAME con show | grep {}'.format(partial))

        # delete all of the matching connections
        for line in response.splitlines():
            if len(line) > 0:
                uuid = line.split()[0]
                cmd('nmcli con delete uuid {}'.format(uuid))

    # ignore warnings in nmcli output
    # sometimes there are warnings but we connected just fine
    @staticmethod
    def _error_in_response(response):
        # no error if no response
        if len(response) == 0:
            return False

        # loop through each line
        for line in response.splitlines():
            # all error lines start with 'Error'
            if line.startswith('Error'):
                return True

        # if we didn't find an error then we are in the clear
        return False

    def get_wifi_list(self):
        # TODO add mapping to uuid if possible and set active now
        ans = cmd('nmcli -t -f SSID,MODE,CHAN,FREQ,RATE,SIGNAL,SECURITY,DEVICE,ACTIVE dev wifi list')
        if self._error_in_response(ans):
            raise ServerException('Не удалось получить список беспроводных соеденений. Ответ команды: {}'.format(ans))
        connections = ans.splitlines()
        mapped = []
        for connection in connections:
            splitted_array = connection.split(':')
            mapped.append({
                'name': splitted_array[0],
                'id': self.ssid_to_connection_map.get(splitted_array[0]),
                'type': 'wifi',
                'mode': splitted_array[1],
                'channel': splitted_array[2],
                'frequency': splitted_array[3],
                'speed_rate': splitted_array[4],
                'signal_level': splitted_array[5],
                'security_type': splitted_array[6],
                'device': splitted_array[7],
                'active': splitted_array[8] == 'yes',
                # TODO may be add in map by ssid 'autoconnect': splitted_array[5] == 'yes'
            })
        return mapped

    def get_eth_list(self):
        ans = cmd('nmcli -t -f NAME,UUID,TYPE,DEVICE,ACTIVE,AUTOCONNECT con show | grep ethernet')
        if self._error_in_response(ans):
            raise ServerException('Не удалось получить список проводных соеденений. Ответ команды: {}'.format(ans))
        connections = ans.splitlines()
        mapped = []
        for connection in connections:
            splitted_array = connection.split(':')
            mapped.append({
                'name': splitted_array[0],
                'id': splitted_array[1],
                'type': 'eth',
                'device': splitted_array[3],
                'active': splitted_array[4] == 'yes',
                'autoconnect': splitted_array[5] == 'yes'
            })
        return mapped

    # returned the ssid of the current network
    # TODO refactor because i want to persist used connections
    def current(self):
        # list active connections for all interfaces
        response = cmd('nmcli con | grep {}'.format(self.interface()))

        # the current network is in the first column
        for line in response.splitlines():
            if len(line) > 0:
                return line.split()[0]

        # return none if there was not an active connection
        return None

    def create_wifi_connection(self, ssid, password):
        # clean up previous connection TODO check for need of it
        # self._clean(ssid)
        # turn off current connection
        cmd('nmcli con down {}'.format(self.current()))
        # trying to connect
        # TODO check response??
        # TODO add connection_params like static ip and etc
        response = cmd('nmcli dev wifi connect {} password {} iface {}'.format(
            ssid, password, self._interface))
        # parse response
        # TODO if error need to up old connection
        # TODO add info about created uuid
        if self._error_in_response(response):
            raise ServerException(response, status.HTTP_400_BAD_REQUEST)
        else:
            res = cmd('nmcli con show | grep {}'.format(ssid))
            if res:
                # self.ssid_to_connection_map[ssid] = res['uuid']
                return True
            else:
                return False


# Linux nmcli Driver >= 0.9.9.0 (Actual driver)
# TODO make cleanup, add static ip (look at set_static_ip.bash)
class Nmcli0990(NetworkDriver):
    _interface = None

    # init
    def __init__(self, interface=None):
        self.interface(interface)
        # TODO persist
        self.ssid_to_connection_map = {}

    # clean up connections where partial is part of the connection name
    # this is needed to prevent the following error after extended use:
    # 'maximum number of pending replies per connection has been reached'
    def _clean(self, partial):
        # list matching connections
        response = cmd('nmcli --fields UUID,NAME con show | grep {}'.format(partial))

        # delete all of the matching connections
        for line in response.splitlines():
            if len(line) > 0:
                uuid = line.split()[0]
                cmd('nmcli con delete uuid {}'.format(uuid))

    # ignore warnings in nmcli output
    # sometimes there are warnings but we connected just fine
    def _error_in_response(self, response):
        # no error if no response
        if len(response) == 0:
            return False

        # loop through each line
        for line in response.splitlines():
            # all error lines start with 'Error'
            if line.startswith('Error'):
                return True

        # if we didn't find an error then we are in the clear
        return False

    # connect to a network
    def connect(self, ssid, password):
        # clean up previous connection TODO check for need of it
        # self._clean(ssid)
        # turn off current connection
        cmd(command='nmcli con down {}'.format(self.current()))
        # trying ti connect
        response = cmd('nmcli dev wifi connect {} password {} iface {}'.format(
            ssid, password, self._interface))
        print(response)
        # parse response
        # TODO if error need to up old connection
        if self._error_in_response(response):
            raise ServerException(response, status.HTTP_400_BAD_REQUEST)
        else:
            return True

    # returned the ssid of the current network
    def current(self):
        # list active connections for all interfaces
        response = cmd('nmcli con | grep {}'.format(self.interface()))

        # the current network is in the first column
        for line in response.splitlines():
            if len(line) > 0:
                return line.split()[0]

        # return none if there was not an active connection
        return None

    # return a list of wireless adapters
    def interfaces(self):
        # grab list of interfaces
        response = cmd('nmcli dev')

        # parse response
        interfaces = []
        for line in response.splitlines():
            if 'wifi' in line:
                # this line has our interface name in the first column
                interfaces.append(line.split()[0])

        # return list
        return interfaces

    # return the current wireless adapter
    def interface(self, interface=None):
        if interface is not None:
            self._interface = interface
        else:
            return self._interface

    # enable/disable wireless networking
    def power(self, power=None):
        if power is True:
            cmd('nmcli r wifi on')
        elif power is False:
            cmd('nmcli r wifi off')
        else:
            response = cmd('nmcli r wifi')
            return 'enabled' in response

    @staticmethod
    def _map_connections_list(raw_str):
        def map_connection_line(connection_line):
            # split line by two spaces because between two columns we have at least two spaces,
            # after split we need to delete empty lines from array
            splitted_array = list(filter(lambda x: x != '', connection_line.split('  ')))
            if splitted_array[0] == '*':
                splitted_array[0] = '+'
            else:
                splitted_array.insert(0, '-')
            return {label.strip().lower(): splitted_array[i].strip() for i, label in enumerate(labels)}

        response_lines = raw_str.splitlines()
        # getting header and map it to labels
        labels = list(filter(lambda x: x != '', response_lines[0].split('  ')))
        # and delete header line from answer
        del response_lines[0]
        return list(map(map_connection_line, response_lines))

    def list_of_connections(self, rescan=True):
        if rescan:
            res = ''
            while 'immediately' not in res:
                res = cmd('nmcli device wifi rescan')
                sleep(0.5)
            sleep(1)

        return self._map_connections_list(cmd('nmcli device wifi list'))
