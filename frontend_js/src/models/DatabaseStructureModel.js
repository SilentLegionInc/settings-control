export class DatabaseStructureModel {
    constructor(systemName = '', name = '', fields = []) {
        this.systemName = systemName;
        this.name = name;
        this.fields = fields;
    }
}
