import glob
import shutil

from dateutil import tz
from toolbelt.support.server_exception import ServerException
from toolbelt.support.singleton import Singleton
from toolbelt.support.logger import Logger
from flask_api import status
from enum import Enum
from subprocess import Popen
from subprocess import check_output
from subprocess import DEVNULL
from threading import Thread
from toolbelt.support.settings_service import SettingsService
from git import Repo
from multiprocessing import Process
import os
import re
import time
import datetime


class ProcessStatus(Enum):
    DEFAULT = -1,
    SUCCESS = 0,
    ERROR = 1


class CoreService(metaclass=Singleton):
    def __call__(self):
        # We need this to handle when config changed
        repo_name = SettingsService().current_machine_config['core']['repo_name']
        self.build_path = os.path.expanduser(os.path.join(SettingsService().server_config['builds_path'], repo_name))
        self.qmake_path = os.path.expanduser(SettingsService().server_config['qmake_path'])
        self.sources_path = os.path.join(
            os.path.expanduser(SettingsService().server_config['sources_path']), repo_name)
        self.repo_url = SettingsService().libraries['cores'][repo_name]

    def __init__(self):
        repo_name = SettingsService().current_machine_config['core']['repo_name']
        self.build_path = os.path.expanduser(os.path.join(SettingsService().server_config['builds_path'], repo_name))
        self.qmake_path = os.path.expanduser(SettingsService().server_config['qmake_path'])
        self.sources_path = os.path.join(
            os.path.expanduser(SettingsService().server_config['sources_path']), repo_name)
        self.repo_url = SettingsService().libraries['cores'][repo_name]

        self.main_proc = None
        self.compile_status = ProcessStatus.DEFAULT
        self.compile_output = None
        self.compile_thread = None

    def pull_info(self):
        is_cloned = os.path.isdir(self.sources_path) and os.listdir(self.sources_path)
        if is_cloned:
            all_files = glob.iglob('{}/*'.format(self.sources_path), recursive=True)
            pull_time = max([os.path.getmtime(file_path) for file_path in all_files])
            mtime = datetime.datetime.fromtimestamp(pull_time).replace(tzinfo=tz.tzlocal())
            return True, mtime
        return False, None

    def built_info(self):
        is_built = os.path.isdir(self.build_path) and os.listdir(self.build_path)
        if is_built:
            all_files = glob.iglob('{}/*'.format(self.build_path), recursive=True)
            built_time = max([os.path.getmtime(file_path) for file_path in all_files])
            mtime = datetime.datetime.fromtimestamp(built_time).replace(tzinfo=tz.tzlocal())
            return True, mtime
        return False, None

    def run_core(self, exec_output=DEVNULL):
        if not self.core_is_active():
            run_file_name = SettingsService().current_machine_config['core']['executable_name']
            run_file_path = os.path.expanduser(os.path.join(self.build_path, run_file_name))
            self.main_proc = Popen(run_file_path, stdout=exec_output, stderr=exec_output)
            return True
        else:
            Logger().error_message('Core is already running. You can\'t run more than one per time.')
            raise ServerException('Нельзя запустить ядро, когда оно уже запущено', status.HTTP_400_BAD_REQUEST)

    def stop_core(self):
        if self.core_is_active():
            # if it will not die. Use kill()
            self.main_proc.terminate()
        return True

    def core_is_active(self):
        return bool(self.main_proc and self.main_proc.poll() is None)

    def get_exit_code(self):
        return self.main_proc.poll() if self.main_proc else None

    def _compile_core(self):
        if self.compile_status is None:
            Logger().error_message('Can\'t run several compile processes at time.')
            return

        self.compile_status = None
        self.compile_output = None
        try:
            shutil.rmtree(self.build_path, ignore_errors=True)
            os.makedirs(self.build_path)
            self.compile_output = check_output('{} {} -o {}'.format(self.qmake_path,
                                                                    os.path.join(self.sources_path, '*.pro'),
                                                                    self.build_path), shell=True).decode('ascii')
            self.compile_output += check_output('cd {} && make'.format(self.build_path), shell=True).decode('ascii')
            config_file_name = SettingsService().current_machine_config['core']['config_path']
            config_file_path = os.path.join(self.sources_path, config_file_name)
            target_config_path = os.path.join(self.build_path, config_file_name)
            self.compile_output += check_output('cp -f {} {}'.format(config_file_path, target_config_path), shell=True).decode(
                'ascii')
        except Exception as e:
            self.compile_status = ProcessStatus.ERROR
            Logger().error_message('Exception while core building: {}'.format(e))
            return self.compile_status, self.compile_output

        regex = re.compile('(error)+', re.IGNORECASE)
        if regex.match(self.compile_output) is None:
            self.compile_status = ProcessStatus.SUCCESS
        else:
            self.compile_status = ProcessStatus.ERROR

    def compile_core_sync(self):
        # if self.core_is_active():
        #     Logger().error_message('Can\'t compile core while it\'s running.')
        #     raise ServerException('Невозможно собрать ядро когда оно запущено', status.HTTP_406_NOT_ACCEPTABLE)

        self._compile_core()
        return self.compile_status, self.compile_output

    def compile_core(self):
        # if self.core_is_active():
        #     Logger().error_message('Can\'t compile core while it\'s running.')
        #     raise ServerException('Невозможно собрать ядро когда оно запущено', status.HTTP_406_NOT_ACCEPTABLE)

        self.compile_thread = Thread(name='compile_core', target=self._compile_core)
        self.compile_thread.start()

    def update_core_sync(self):
        url = self.repo_url
        path = self.sources_path

        need_clone = False
        if not os.path.isdir(path):
            need_clone = True

        if need_clone:
            Repo.clone_from(url, path)
        else:
            repo = Repo(path)
            repo.git.reset('--hard')
            repo.git.pull()

    def update_core_async(self):
        p = Process(target=self.update_core_sync)
        p.start()
        return p


if __name__ == '__main__':
    core = CoreService()
    core.compile_core()
    while core.compile_status is None:
        print('wait')
        time.sleep(1)
    print(core.compile_output)

