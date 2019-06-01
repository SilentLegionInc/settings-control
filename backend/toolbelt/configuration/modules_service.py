import os
import shutil
import zipfile
from collections import OrderedDict

from toolbelt.configuration.core_service import CoreService, ProcessStatus
from toolbelt.support.settings_service import SettingsService
from toolbelt.configuration.update_service import UpdateService
from flask_api import status
from toolbelt.support.helper import cmd
from toolbelt.support.server_exception import ServerException
from toolbelt.support.singleton import Singleton


class ModulesService(metaclass=Singleton):
    def __call__(self):
        self._core_service.refresh_from_config()
        self._dependencies_service.refresh_from_config()
        self._download_path = os.path.expanduser(SettingsService().server_config['upload_path'])

    def __init__(self):
        self._settings_service = SettingsService()
        self._core_service = CoreService()
        self._dependencies_service = UpdateService()
        self._download_path = os.path.expanduser(SettingsService().server_config['upload_path'])

    def get_modules_list(self):
        machine_config = self._settings_service.current_machine_config
        if not machine_config:
            raise ServerException(
                'Не удалось найти конфигурацию для комплекса: {}'.format(self._settings_service.server_config['type']),
                status.HTTP_500_INTERNAL_SERVER_ERROR)

        mapped_dependencies = []
        dependencies = dict(OrderedDict(sorted(machine_config['dependencies'].items(), key=lambda x: x[1])))
        for dependency in dependencies:
            dependency_url = self._settings_service.libraries['dependencies'].get(dependency)
            dependency_info = {
                'name': dependency,
                'url': dependency_url,
                'index': dependencies[dependency]
            }
            build_info = self._dependencies_service.built_info(dependency)
            dependency_info['is_built'] = build_info[0]
            dependency_info['build_modify_time'] = build_info[1]

            clone_info = self._dependencies_service.pull_info(dependency)
            dependency_info['is_cloned'] = clone_info[0]
            dependency_info['src_modify_time'] = clone_info[1]
            mapped_dependencies.append(dependency_info)

        core_info = {
            'name': machine_config['core']['repo_name'],
            'execute': machine_config['core']['executable_name'],
            'config_path': machine_config['core']['config_path'],
            'url': self._settings_service.libraries['cores'].get(machine_config['core']['repo_name']),
            'is_active': self._core_service.core_is_active()
        }

        core_build_info = self._core_service.built_info()
        core_info['is_built'] = core_build_info[0]
        core_info['build_modify_time'] = core_build_info[1]

        core_clone_info = self._core_service.pull_info()
        core_info['is_cloned'] = core_clone_info[0]
        core_info['src_modify_time'] = core_clone_info[1]

        return {'core': core_info, 'dependencies': mapped_dependencies}
    
    def pull_machine(self):
        machine_config = self._settings_service.current_machine_config
        if not machine_config:
            raise ServerException(
                'Не удалось найти конфигурацию для комплекса: {}'.format(self._settings_service.server_config['type']),
                status.HTTP_500_INTERNAL_SERVER_ERROR)

        dependencies = dict(OrderedDict(sorted(machine_config['dependencies'].items(), key=lambda x: x[1])))
        for dependency in dependencies:
            dependency_url = self._settings_service.libraries['dependencies'].get(dependency)
            if not dependency_url:
                raise ServerException('Ошибка обновления. Неизвестная зависимость: {}'.format(dependency),
                                      status.HTTP_500_INTERNAL_SERVER_ERROR)

            self._dependencies_service.update_lib_sync(dependency)

        # TODO check that core is not running if it is -> kill them? or not needed?
        self._core_service.update_core_sync()
        return True
    
    def build_machine(self):
        machine_config = self._settings_service.current_machine_config
        if not machine_config:
            raise ServerException(
                'Не удалось найти конфигурацию для комплекса: {}'.format(self._settings_service.server_config['type']),
                status.HTTP_500_INTERNAL_SERVER_ERROR)

        dependencies = dict(OrderedDict(sorted(machine_config['dependencies'].items(), key=lambda x: x[1])))
        for dependency in dependencies:
            dependency_url = self._settings_service.libraries['dependencies'].get(dependency)
            if not dependency_url:
                raise ServerException('Ошибка сборки. Неизвестная зависимость: {}'.format(dependency),
                                      status.HTTP_500_INTERNAL_SERVER_ERROR)
            (is_cloned, _) = self._dependencies_service.pull_info(dependency)
            if not is_cloned:
                self._dependencies_service.update_lib_sync(dependency)
            (compile_status, compile_output, errors) = self._dependencies_service.upgrade_lib_sync(dependency)
            if compile_status is not ProcessStatus.SUCCESS:
                raise ServerException('Ошибка сборки. Информация: {}'.format(';\n'.join(errors)), status.HTTP_500_INTERNAL_SERVER_ERROR)

        (is_cloned, _) = self._core_service.pull_info()
        if not is_cloned:
            self._core_service.update_core_sync()
        # TODO check that core is not running if it is -> kill them?
        (compile_status, compile_output, errors) = self._core_service.compile_core_sync()
        if compile_status is ProcessStatus.SUCCESS:
            return True
        else:
            raise ServerException('Ошибка сборки. Информация: {}'.format(';\n'.join(errors)), status.HTTP_500_INTERNAL_SERVER_ERROR)

    def build_module(self, module_name):
        # (compile_status, compile_output, errors) = (ProcessStatus.DEFAULT, None, [])
        if module_name in self._settings_service.libraries['dependencies']:
            (is_cloned, _) = self._dependencies_service.pull_info(module_name)
            if not is_cloned:
                self._dependencies_service.update_lib_sync(module_name)
            (compile_status, compile_output, errors) = self._dependencies_service.upgrade_lib_sync(module_name)
        elif module_name in self._settings_service.libraries['cores']:
            (is_cloned, _) = self._core_service.pull_info()
            if not is_cloned:
                self._core_service.update_core_sync()
            (compile_status, compile_output, errors) = self._core_service.compile_core_sync()
        else:
            raise ServerException('Неизвестный модуль {}'.format(module_name), status.HTTP_400_BAD_REQUEST)

        if compile_status is ProcessStatus.SUCCESS:
            return True
        else:
            raise ServerException('Ошибка сборки. Информация: {}'.format(';\n'.join(errors)), status.HTTP_500_INTERNAL_SERVER_ERROR)

    def pull_module(self, module_name):
        if module_name in self._settings_service.libraries['dependencies']:
            self._dependencies_service.update_lib_sync(module_name)
        elif module_name in self._settings_service.libraries['cores']:
            self._core_service.update_core_sync()
        return True

    def manual_module_update(self, file_path, module_name):
        zip_archive = zipfile.ZipFile(file_path, 'r')
        zip_archive.extractall(self._download_path)
        zip_archive.close()

        target_path = os.path.join(
            os.path.expanduser(SettingsService().server_config['sources_path']),
            module_name
        )
        source_lib_path = os.path.join(self._download_path, module_name)
        if not os.path.isdir(target_path):
            shutil.rmtree(target_path, ignore_errors=True)
            os.makedirs(target_path)
        cmd('cp -Rf {}/* {}'.format(source_lib_path, target_path))
        # (compile_status, compile_output, errors) = (ProcessStatus.DEFAULT, None, [])
        if module_name in self._settings_service.libraries['dependencies']:
            (compile_status, compile_output, errors) = self._dependencies_service.upgrade_lib_sync(module_name)
        elif module_name in self._settings_service.libraries['cores']:
            (compile_status, compile_output, errors) = self._core_service.compile_core_sync()
        else:
            raise ServerException('Неизвестный модуль {}'.format(module_name), status.HTTP_400_BAD_REQUEST)

        if compile_status is ProcessStatus.SUCCESS:
            return True
        else:
            raise ServerException('Ошибка сборки. Информация: {}'.format(';\n'.join(errors)), status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_ssh_key(self, file_path):
        zip_archive = zipfile.ZipFile(file_path, 'r')
        zip_archive.extractall(self._download_path)
        zip_archive.close()
        file_path = file_path.replace('.zip', '')
        ssh_path = os.path.expanduser('~/.ssh')
        if os.path.exists(ssh_path):
            cmd('sudo rm -rf {}'.format(ssh_path))
        os.makedirs(ssh_path)
        cmd('sudo mv -f {}/*.pub {}/id_rsa.pub'.format(file_path, ssh_path))
        cmd('sudo mv -f {}/* {}/id_rsa'.format(file_path, ssh_path))
        hosts_file_name = os.path.join(ssh_path, 'known_hosts')
        cmd('ssh-keyscan {} >> {}'.format(self._settings_service.server_config['repositories_platform'], hosts_file_name))
        return True

    def run_core(self, cmd_params=''):
        self._core_service.run_core(cmd_params=cmd_params)
        if self._core_service.core_is_active():
            return True
        else:
            raise ServerException('Не удалось запутсить ядро', status.HTTP_500_INTERNAL_SERVER_ERROR)

    def stop_core(self):
        self._core_service.stop_core()
        if not self._core_service.core_is_active():
            return True
        else:
            raise ServerException('Не удалось запутсить ядро', status.HTTP_500_INTERNAL_SERVER_ERROR)

    def core_is_active(self):
        return self._core_service.core_is_active()
