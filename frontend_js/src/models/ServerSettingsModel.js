export class ServerSettingsModel {
    constructor (machineType, sourcesPath, buildsPath, uploadPath, qmakePath,
        sshName, repositoriesPlatform, possibleMachinesTypes) {
        this.machineType = machineType;
        this.sourcesPath = sourcesPath;
        this.buildsPath = buildsPath;
        this.uploadPath = uploadPath;
        this.qmakePath = qmakePath;
        this.sshName = sshName;
        this.repositoriesPlatform = repositoriesPlatform;
        this.possibleMachinesTypes = possibleMachinesTypes;
    }

    toPythonDict() {
        return {
            'type': this.machineType,
            'sources_path': this.sourcesPath,
            'builds_path': this.buildsPath,
            'qmake_path': this.qmakePath,
            'upload_path': this.uploadPath,
            'ssh_key_name': this.sshName,
            'repositories_platform': this.repositoriesPlatform
        }
    }
}
