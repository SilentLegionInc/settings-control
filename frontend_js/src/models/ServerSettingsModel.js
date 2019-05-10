export class ServerSettingsModel {
    constructor (machineType, sourcesPath, buildsPath, uploadPath, qmakePath,
        repositoriesPlatform, possibleMachinesTypes) {
        this.machineType = machineType;
        this.sourcesPath = sourcesPath;
        this.buildsPath = buildsPath;
        this.uploadPath = uploadPath;
        this.qmakePath = qmakePath;
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
            'repositories_platform': this.repositoriesPlatform
        }
    }
}
