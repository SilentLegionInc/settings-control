from src.singleton import Singleton
from src.logger import Logger
from subprocess import Popen
from subprocess import DEVNULL
from subprocess import STDOUT
import os


class CoreService(metaclass=Singleton):
    def __init__(self, exec_path):
        self.exec_path = exec_path
        self.main_proc = None

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

    def update_libraries(self):
        #TODO add update handler
        pass

    def compile_core(self):
        #TODO need to add new thread witch will make project build and when it will finish, we will get result_status of this thread and output as a string
        #TODO add compile handler
        # cd to project folder
        # qmake_path = 'path/to/qmake'
        # sources_path = 'path/to/sources'
        # out = check_output([qmake_path, os.path.join(sources_path, '*.pro')])
        pass


if __name__ == '__main__':
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..', 'wait_plug')
    core = CoreService(path)
    core.run_core(None)
    core.main_proc.wait()
