from src.singleton import Singleton
from src.logger import Logger
from enum import Enum
from subprocess import Popen
from subprocess import check_output
from subprocess import DEVNULL
from threading import Thread
import os
import re
import time


class ProcessStatus(Enum):
    DEFAULT = -1,
    SUCCESS = 0,
    ERROR = 1


class CoreService(metaclass=Singleton):
    def __init__(self, exec_path, qmake_path, sources_path, repos_path, repos):
        self.exec_path = exec_path
        self.qmake_path = qmake_path
        self.sources_path = sources_path
        self.main_proc = None
        self.repos = repos
        self.repos_path = repos_path

        self.compile_status = ProcessStatus.DEFAULT
        self.compile_output = None
        self.compile_thread = None

        self.update_status = ProcessStatus.DEFAULT
        self.update_output = None
        self.update_thread = None

    def run_core(self, exec_output=DEVNULL):
        if not self.main_proc or self.main_proc.poll() is not None:
            self.main_proc = Popen(self.exec_path, stdout=exec_output, stderr=exec_output)
        else:
            Logger().error_message('Core is already running. You can\'t run more than one per time.')

    def stop_core(self):
        if self.main_proc and self.main_proc.poll() is None:
            self.main_proc.kill()

    def core_is_active(self):
        return self.main_proc and self.main_proc.poll() is None

    def get_exit_code(self):
        return self.main_proc.poll() if self.main_proc else None

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

    def _compile_core(self):
        if self.compile_status is None:
            Logger().error_message('Can\'t run several compile processes at time.')
            return

        self.compile_status = None
        self.compile_output = None

        # self.compile_output = check_output([self.qmake_path, os.path.join(self.sources_path, '*.pro')]).decode('ascii')
        # self. compile_output += check_output('cd {} && make'.format(self.sources_path)).decode('ascii')
        self.compile_output = check_output(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..', 'wait_plug')).decode('ascii')

        regex = re.compile('(error)+', re.IGNORECASE)
        if regex.match(self.compile_output) is None:
            self.compile_status = ProcessStatus.SUCCESS
        else:
            self.compile_status = ProcessStatus.ERROR

    def compile_core(self):
        self.compile_thread = Thread(name='compile_core', target=self._compile_core)
        self.compile_thread.start()


if __name__ == '__main__':
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..', 'wait_plug')
    core = CoreService(path, '', '', {}, '')
    core.compile_core()
    while core.compile_status is None:
        print('wait')
        time.sleep(1)
    print(core.compile_output)

