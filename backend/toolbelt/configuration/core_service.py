import glob
import shutil

from dateutil import tz
from toolbelt.support.server_exception import ServerException
from toolbelt.support.singleton import Singleton
from toolbelt.support.logger import Logger
from flask_api import status
from enum import Enum
from subprocess import Popen, STDOUT, CalledProcessError
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
    def refresh_from_config(self):
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
        self.errors = []

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

    def run_core(self, cmd_params='', exec_output=DEVNULL):
        if not self.core_is_active():
            run_file_name = SettingsService().current_machine_config['core']['executable_name']
            run_file_path = os.path.expanduser(os.path.join(self.build_path, run_file_name))
            try:
                self.main_proc = Popen([run_file_path, *cmd_params.split(' ')], stdout=exec_output, stderr=exec_output)
            except FileNotFoundError as file_error:
                raise ServerException('Не удалось найти файл для запуска, возможно его имя некорректно', status.HTTP_500_INTERNAL_SERVER_ERROR, file_error)
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
            raise ServerException('Нельзя запустить несколько процессов сборки одновременно')

        self.compile_status = None
        self.compile_output = ''
        self.errors = []
        try:
            shutil.rmtree(self.build_path, ignore_errors=True)
            os.makedirs(self.build_path)
            qmake_command = '{} {} -o {}'.format(self.qmake_path,
                                                 os.path.join(self.sources_path, '*.pro'),
                                                 self.build_path)
            make_command = 'cd {} && make'.format(self.build_path)
            compile_output = check_output(qmake_command, shell=True, stderr=STDOUT).decode('utf-8')
            compile_output += check_output(make_command, shell=True, stderr=STDOUT).decode('utf-8')

            config_file_name = SettingsService().current_machine_config['core']['config_path']
            config_file_path = os.path.join(self.sources_path, config_file_name)
            target_config_path = os.path.join(self.build_path, config_file_name)
            copy_config_command = 'cp -f {} {}'.format(config_file_path, target_config_path)
            self.compile_output += check_output(copy_config_command, shell=True, stderr=STDOUT).decode('utf-8')
        except CalledProcessError as command_error:
            self.compile_status = ProcessStatus.ERROR
            error_info = command_error.output.decode('utf-8')
            Logger().error_message('Command {} return non-zero code: {}'.format(command_error.cmd, error_info))
            self.compile_output += error_info
            self.errors.append(error_info)
        except Exception as e:
            self.compile_status = ProcessStatus.ERROR
            Logger().error_message('Exception while core building: {}'.format(e))

        self.compile_status = ProcessStatus.SUCCESS
        real_errors_regex = r"^(?P<real_error>.*error.*(?<!\(ignored\)))$"
        self.errors.extend(re.findall(real_errors_regex, self.compile_output, re.IGNORECASE | re.MULTILINE))
        if self.errors:
            Logger().debug_message('Ошибки сборки вот такие: {}'.format(self.errors))
            self.compile_status = ProcessStatus.ERROR

        return self.compile_status, self.compile_output, self.errors

    def compile_core_sync(self):
        # if self.core_is_active():
        #     Logger().error_message('Can\'t compile core while it\'s running.')
        #     raise ServerException('Невозможно собрать ядро когда оно запущено', status.HTTP_406_NOT_ACCEPTABLE)

        return self._compile_core()

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

        try:
            if need_clone:
                Repo.clone_from(url, path)
            else:
                repo = Repo(path)
                repo.git.reset('--hard')
                repo.git.pull()
        except Exception as e:
            raise ServerException('Ошибка работы с гит. Информация: {}'.format(str(e)), status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_core_async(self):
        p = Process(target=self.update_core_sync)
        p.start()
        return p

