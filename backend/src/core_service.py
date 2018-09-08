from src.singleton import Singleton
from src.logger import Logger
from subprocess import Popen
import time


class CoreService(metaclass=Singleton):
    def __init__(self, exec_path='/home/befezdow/wait_plug'):
        self.exec_path = exec_path
        self.proc = None

    def run_core(self):
        if not self.proc or self.proc.poll() is not None:
            self.proc = Popen(self.exec_path)
        else:
            Logger().error_message('Core is already running. You can\'t run more than one per time.')

    def stop_core(self):
        if self.proc and self.proc.poll() is None:
            self.proc.kill()

    def core_is_active(self):
        return self.proc and self.proc.poll() is None

    def get_exit_code(self):
        return self.proc.poll() if self.proc else None
