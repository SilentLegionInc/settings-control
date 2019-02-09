from abc import ABCMeta, abstractmethod
import subprocess
from time import sleep
from packaging import version
from support.singleton import Singleton
from support.server_exception import ServerException
from flask_api import status


# send a command to the shell and return the result
def cmd(command):
    return subprocess.Popen(
        command, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    ).stdout.read().decode()


# abstracts class of Wifi configurator
class WifiService(metaclass=Singleton):
    _driver_name = None
    _driver = None

    # init
    def __init__(self, interface=None):
        # detect and init appropriate driver
        self._driver_name = self._detect_driver()
        if self._driver_name == 'nmcli':
            self._driver = NmcliWireless(interface=interface)
        elif self._driver_name == 'nmcli0990':
            self._driver = Nmcli0990Wireless(interface=interface)

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

        # try nmcli (Ubuntu w/o network-manager)
        response = cmd('which wpa_supplicant')
        if len(response) > 0 and 'not found' not in response:
            return 'wpa_supplicant'

        raise Exception('Unable to find compatible wireless driver.')

    # connect to a network
    def connect(self, ssid, password):
        print('trying to connect {}'.format(ssid))
        return self._driver.connect(ssid, password)

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
        return self._driver.list_of_connections(rescan)


# abstract class for all wifi drivers
class WifiDriver(metaclass=ABCMeta):

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


# Linux nmcli Driver < 0.9.9.0 (legacy support)
# TODO Actualize me later... if you want
class NmcliWireless(WifiDriver):
    _interface = None

    # init
    def __init__(self, interface=None):
        self.interface(interface)

    # clean up connections where partial is part of the connection name
    # this is needed to prevent the following error after extended use:
    # 'maximum number of pending replies per connection has been reached'
    def _clean(self, partial):
        # list matching connections
        response = cmd('nmcli --fields UUID,NAME con list | grep {}'.format(
            partial))

        # delete all of the matching connections
        for line in response.splitlines():
            if len(line) > 0:
                uuid = line.split()[0]
                cmd('nmcli con delete uuid {}'.format(uuid))

    # ignore warnings in nmcli output
    # sometimes there are warnings but we connected just fine
    def _errorInResponse(self, response):
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
        # clean up previous connection
        self._clean(self.current())
        print('Work in driver')
        # here
        # attempt to connect
        response = cmd('nmcli device wifi connect {} password {} iface {}'.format(
            ssid, password, self._interface))
        print(response)
        # parse response
        return not self._errorInResponse(response)

    # returned the ssid of the current network
    def current(self):
        # list active connections for all interfaces
        response = cmd('nmcli con status | grep {}'.format(
            self.interface()))

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
            if 'wireless' in line:
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
            cmd('nmcli nm wifi on')
        elif power is False:
            cmd('nmcli nm wifi off')
        else:
            response = cmd('nmcli nm wifi')
            return 'enabled' in response


# Linux nmcli Driver >= 0.9.9.0 (Actual driver)
# TODO make cleanup
class Nmcli0990Wireless(WifiDriver):
    _interface = None

    # init
    def __init__(self, interface=None):
        self.interface(interface)

    # clean up connections where partial is part of the connection name
    # this is needed to prevent the following error after extended use:
    # 'maximum number of pending replies per connection has been reached'
    def _clean(self, partial):
        # list matching connections
        response = cmd('nmcli --fields UUID,NAME con show | grep {}'.format(
            partial))

        # delete all of the matching connections
        for line in response.splitlines():
            if len(line) > 0:
                uuid = line.split()[0]
                cmd('nmcli con delete uuid {}'.format(uuid))

    # ignore warnings in nmcli output
    # sometimes there are warnings but we connected just fine
    def _errorInResponse(self, response):
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
        print('Linux driver working')
        # trying ti connect
        response = cmd('nmcli dev wifi connect {} password {} iface {}'.format(
            ssid, password, self._interface))
        print(response)
        # parse response
        # TODO if error need to up old connection
        if self._errorInResponse(response):
            raise ServerException(response, status.HTTP_400_BAD_REQUEST)
        else:
            return True

    # returned the ssid of the current network
    def current(self):
        # list active connections for all interfaces
        response = cmd('nmcli con | grep {}'.format(
            self.interface()))

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


# Linux wpa_supplicant Driver
# TODO Actualize me later... if you want
# class WpasupplicantWireless(WifiDriver):


def get_mocked_list():
    r = 'IN-USE  SSID               MODE   CHAN  RATE        SIGNAL  BARS  SECURITY\n' + \
        '*       Silence_2G         Infra  1     270 Mbit/s  83      ▂▄▆█  WPA1 WPA2\n' + \
        '        akm                Infra  1     130 Mbit/s  55      ▂▄__  WPA1 WPA2\n' + \
        '        Keenetic-3871      Infra  2     270 Mbit/s  55      ▂▄__  WPA2'

    return Nmcli0990Wireless._map_connections_list(r)


if __name__ == '__main__':
    print(get_mocked_list())
    # wifi = WifiService()
    # print(wifi.list_of_connections())


