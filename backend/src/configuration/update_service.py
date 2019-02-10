from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from support.singleton import Singleton
from configuration.core_service import ProcessStatus
from multiprocessing import Process
from configuration.settings_service import SettingsService
from git import Repo
from subprocess import check_output
import os
import re
import shutil


class UpdateService(metaclass=Singleton):
    def __init__(self):
        self.repos = {}
        self.sources_path = os.path.expanduser(SettingsService().server_config['sources_path'])
        self.build_path = os.path.expanduser(SettingsService().server_config['builds_path'])
        self.qmake_path = os.path.expanduser(SettingsService().server_config['qmake_path'])
        self.ssh_key_name = SettingsService().server_config['ssh_key_name']
        self.repositories_platform = SettingsService().server_config['repositories_platform']

        self.update_status = ProcessStatus.DEFAULT
        self.update_output = None
        self.update_thread = None

        self.ssh_path = os.path.expanduser('~/.ssh')
        if not os.path.isdir(self.ssh_path):
            os.mkdir(self.ssh_path)

    def generate_ssh_key(self):
        key = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=2048
        )
        private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.PKCS8,
            crypto_serialization.NoEncryption()
        ).decode('utf-8')
        public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH
        ).decode('utf-8')
        return private_key, public_key

    def _create_ssh_key(self, return_dict=None, key='create_ssh_key_result'):
        private_key, public_key = self.generate_ssh_key()
        key_path = os.path.join(self.ssh_path, self.ssh_key_name)

        with open(key_path, 'w') as file:
            file.write(private_key)

        with open(key_path + '.pub', 'w') as file:
            file.write(public_key)

        hosts_file_name = os.path.join(self.ssh_path, 'known_hosts')
        if os.path.isfile(hosts_file_name):
            os.remove(hosts_file_name)
        os.system('ssh-keyscan ' + self.repositories_platform + ' >> ' + hosts_file_name)

        if return_dict:
            return_dict[key] = public_key

        return public_key

    def create_ssh_key_sync(self):
        return self._create_ssh_key()

    # return_dict - словарь, в который по ключу key складывается результат асинхронной операции.
    # return_dict должен представлять собой инстанс multiprocessing.Manager().dict() иначе данные не будут расшарены между процессами
    def create_ssh_key_async(self, return_dict, key='create_ssh_key_result'):
        return_dict[key] = None
        p = Process(target=self._create_ssh_key, args=(return_dict, key))
        p.start()
        return p

    def _update_lib(self, lib_name):
        lib_url = SettingsService().libraries['dependencies'][lib_name]
        lib_path = os.path.join(self.sources_path, lib_name)

        need_clone = False
        if not os.path.isdir(lib_path):
            need_clone = True

        if need_clone:
            Repo.clone_from(lib_url, lib_path)
        else:
            repo = Repo(lib_path)
            repo.git.reset('--hard')
            repo.git.pull()

    def update_lib_sync(self, lib_name):
        return self._update_lib(lib_name)

    def update_lib_async(self, lib_name):
        p = Process(target=self._update_lib, args=(lib_name,))
        p.start()
        return p

    def _upgrade_lib(self, lib_name, return_dict=None, key='upgrade_lib_result'):
        lib_path = os.path.join(self.sources_path, lib_name)
        build_path = os.path.join(self.build_path, lib_name)

        shutil.rmtree(build_path, ignore_errors=True)
        os.makedirs(build_path)

        qmake_command = '{} {} -o {}'.format(self.qmake_path, os.path.join(lib_path, '*.pro'), build_path)
        make_command = 'cd {} && make install'.format(build_path)

        compile_output = check_output(qmake_command, shell=True).decode('ascii')
        compile_output += check_output(make_command, shell=True).decode('ascii')
        compile_status = ProcessStatus.SUCCESS

        regex = re.compile('(error)+', re.IGNORECASE)
        if regex.match(compile_output) is not None:
            compile_status = ProcessStatus.ERROR

        if return_dict:
            return_dict[key] = compile_status, compile_output

        return compile_status, compile_output

    def upgrade_lib_sync(self, lib_name):
        return self._upgrade_lib(lib_name)

    # return_dict - словарь, в который по ключу key складывается результат асинхронной операции.
    # return_dict должен представлять собой инстанс multiprocessing.Manager().dict() иначе данные не будут расшарены между процессами
    def upgrade_lib_async(self, lib_name, return_dict, key='upgrade_lib_result'):
        return_dict[key] = None
        p = Process(target=self._upgrade_lib, args=(lib_name, return_dict, key))
        p.start()
        return p

    def _update_and_upgrade_lib(self, lib_name, return_dict=None, key='update_and_upgrade_lib_result'):

        self.update_lib_sync(lib_name)
        result = self.upgrade_lib_sync(lib_name)

        if return_dict:
            if not return_dict[key]:
                return_dict[key] = {}
            return_dict[key][lib_name] = result

        return result

    def update_and_upgrade_lib_sync(self, lib_name):
        return self._update_and_upgrade_lib(lib_name)

    # return_dict - словарь, в который по ключу key складывается результат асинхронной операции.
    # return_dict должен представлять собой инстанс multiprocessing.Manager().dict() иначе данные не будут расшарены между процессами
    def update_and_upgrade_lib_async(self, lib_name, return_dict, key='update_and_upgrade_lib_result'):
        return_dict[key] = None
        p = Process(target=self._update_and_upgrade_lib, args=(lib_name, return_dict, key))
        p.start()
        return p


if __name__ == '__main__':
    service = UpdateService()
    service.update_lib_sync('fomodel')
    out = service.upgrade_lib_sync('fomodel')
    print('Status: {}\nOutput: {}'.format(out[0], out[1]))

    # from multiprocessing import Manager
    # manager = Manager()
    # d = manager.dict()
    # process = service.create_ssh_key_async(d, 'qwerty')
    # process.join()
    # print(d)
