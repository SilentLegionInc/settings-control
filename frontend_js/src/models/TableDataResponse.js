export class TableDataResponse {
    constructor(count = 0, result = [], dataStructure = []) {
        this.count = count;
        this.result = result;
        this.dataStructure = dataStructure;
    }
}
