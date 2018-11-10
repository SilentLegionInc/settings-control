from singleton import Singleton
from logger import Logger
from enum import Enum
from subprocess import Popen
from subprocess import check_output
from subprocess import DEVNULL
from threading import Thread
from settings_service import SettingsService
import os
import re
import time


class ProcessStatus(Enum):
    DEFAULT = -1,
    SUCCESS = 0,
    ERROR = 1


class CoreService(metaclass=Singleton):
    def __init__(self):
        run_file_name = SettingsService().core_build_config['core']['executable_name']
        self.build_path = os.path.join(SettingsService().server_config['core_build_path'], run_file_name)
        if not os.path.exists(self.build_path):
            os.makedirs(self.build_path)
        self.qmake_path = SettingsService().server_config['qmake_path']
        self.sources_path = SettingsService().server_config['core_src_path']
        
        self.main_proc = None
        self.compile_status = ProcessStatus.DEFAULT
        self.compile_output = None
        self.compile_thread = None

    def run_core(self, exec_output=DEVNULL):
        if not self.main_proc or self.main_proc.poll() is not None:
            run_file_name = SettingsService().core_build_config['core']['executable_name']
            self.main_proc = Popen(os.path.join(self.build_path, run_file_name), stdout=exec_output, stderr=exec_output)
        else:
            Logger().error_message('Core is already running. You can\'t run more than one per time.')

    def stop_core(self):
        if self.main_proc and self.main_proc.poll() is None:
            # if it will not die. Use kill()
            self.main_proc.terminate()

    def core_is_active(self):
        return self.main_proc and self.main_proc.poll() is None

    def get_exit_code(self):
        return self.main_proc.poll() if self.main_proc else None

    def _compile_core(self):
        if self.compile_status is None:
            Logger().error_message('Can\'t run several compile processes at time.')
            return

        self.compile_status = None
        self.compile_output = None

        self.compile_output = check_output([self.qmake_path,
                                            os.path.join(self.sources_path, '*.pro'),
                                            '-o {}'.format(self.build_path)]).decode('ascii')
        self.compile_output += check_output('cd {} && make'.format(self.build_path)).decode('ascii')

        regex = re.compile('(error)+', re.IGNORECASE)
        if regex.match(self.compile_output) is None:
            self.compile_status = ProcessStatus.SUCCESS
        else:
            self.compile_status = ProcessStatus.ERROR

    def compile_core(self):
        if self.core_is_active():
            Logger().error_message('Can\'t compile core while it\'s running.')
            return
        self.compile_thread = Thread(name='compile_core', target=self._compile_core)
        self.compile_thread.start()


if __name__ == '__main__':
    core = CoreService()
    core.compile_core()
    while core.compile_status is None:
        print('wait')
        time.sleep(1)
    print(core.compile_output)

