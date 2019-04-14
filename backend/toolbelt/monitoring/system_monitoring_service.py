import psutil
import datetime
from toolbelt.support.singleton import Singleton


class SystemMonitoringService(metaclass=Singleton):
    def __init__(self, max_history_records=1000):
        self._history = []
        self._history_enabled = False
        self._max_history_records = max_history_records

    def switch_history(self, enable):
        self._history_enabled = enable

    def get_cpu_usage(self):
        usage = {
            'cpu{}'.format(index): value for index, value in enumerate(psutil.cpu_percent(percpu=True))
        }
        usage['total'] = psutil.cpu_percent(percpu=False)
        if self._history_enabled:
            usage['timestamp'] = datetime.datetime.utcnow()
            history_len = len(self._history)
            if history_len >= self._max_history_records:
                start_from = history_len - self._max_history_records
                self._history = self._history[start_from:]
            else:
                self._history.append(usage)

        return usage

    def get_cpu_history(self):
        return self._history

    def get_memory_usage(self):
        memory_info = dict(psutil.virtual_memory()._asdict())
        swap_info = dict(psutil.swap_memory()._asdict())
        # TODO need history? then add timestamp
        return {
            'ram_info': memory_info,
            'swap_info': swap_info
        }

    def get_disks_usage(self):
        disks = psutil.disk_partitions()
        mountpoints = map(lambda x: x.mountpoint, disks)
        # TODO need history? then add timestamp
        # generating for every mountpoint dict with answer from psutil.disk_usage (by default it is namedtuple)
        return {mountpoint: dict(psutil.disk_usage(mountpoint)._asdict()) for mountpoint in mountpoints}


