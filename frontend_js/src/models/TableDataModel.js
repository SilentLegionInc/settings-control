export class TableDataModel {
    constructor(data = {}) {
        this.data = {}
        for (let elem in data) {
            if (data.hasOwnProperty(elem)) {
                if (['time', 'latitude', 'longitude'].includes(elem)) {
                    this[elem] = data[elem];
                } else {
                    this.data[elem] = data[elem];
                }
            }
        }
    }
}
