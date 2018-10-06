from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
import os
import re

from singleton import Singleton
from logger import Logger
from core_service import ProcessStatus


class GitService(metaclass=Singleton):
    def __init__(self, repos_path, repos):
        self.repos = repos
        self.repos_path = repos_path

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
            crypto_serialization.NoEncryption())
        public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH
        )
        return private_key, public_key
        
        
    
    def _update_libraries(self):
        regex = re.compile('/[A-Za-z0-9]+')
        for repo_url, repo_branch in self.repos:
            folder_name = regex.find(repo_url)[1::]
            folder_path = os.path.join(self.repos_path, folder_name)
            if os.path.exists(folder_path):
                #TODO cd folder, git reset --hard, git checkout branch, git pull
                pass
            else:
                #TODO git clone, git checkout branch
                pass