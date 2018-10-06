from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from singleton import Singleton
from core_service import ProcessStatus
from multiprocessing import Process
from settings_service import SettingsService
from git import Repo
from subprocess import check_output
import os
import re


class UpdateService(metaclass=Singleton):
    def __init__(self):
        self.repos = {}  # TODO add repos declaration to config
        self.sources_path = SettingsService().server_config['core_src_path']
        self.qmake_path = SettingsService().server_config['qmake_path']
        self.ssh_key_path = SettingsService().server_config['ssh_key_path']

        self.update_status = ProcessStatus.DEFAULT
        self.update_output = None
        self.update_thread = None
        
    def generate_ssh(self):
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
        
    def update_lib_sync(self, lib_repo_url, lib_path):
        need_clone = False
        if not os.path.isdir(lib_path):
            need_clone = True

        if need_clone:
            Repo.clone_from(lib_repo_url, lib_path)
        else:
            repo = Repo(lib_path)
            repo.git.reset('--hard')
            repo.git.pull()
    
    def upgrade_lib_sync(self, lib_path):
        compile_output = check_output([self.qmake_path, os.path.join(lib_path, '*.pro')]).decode('ascii')
        compile_output += check_output('cd {} && make install'.format(lib_path)).decode('ascii')
        compile_status = ProcessStatus.SUCCESS
        
        regex = re.compile('(error)+', re.IGNORECASE)
        if regex.match(compile_output) is not None:
            compile_status = ProcessStatus.ERROR
        
        return compile_status, compile_output
    
    def update_and_upgrade_lib_sync(self, lib_repo_url, return_dict=None):  # return_dict: manager = multiprocessing.Manager(); return_dict = manager.dict(); need set None if sync using
        regex = re.compile('/[A-Za-z0-9]+')
        folder_name = regex.findall(lib_repo_url)[0][1::]
        folder_path = os.path.join(self.sources_path, folder_name)
        
        self.update_lib_sync(lib_repo_url, folder_path)
        result = self.upgrade_lib_sync(folder_path)
        if return_dict:
            return_dict[lib_repo_url] = result
    
    def update_and_upgrade_lib_async(self, lib_repo_url, return_dict):
        p = Process(target=self.update_and_upgrade_lib_sync, args=(lib_repo_url, return_dict))
        p.start()
        return p
