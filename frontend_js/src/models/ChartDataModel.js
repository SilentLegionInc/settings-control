export class ChartDataModel {
    constructor(id = 0, latitude = 0, longitude = 0, time = new Date(), value = 0) {
        this.id = id;
        this.latitude = latitude;
        this.longitude = longitude;
        this.time = time;
        this.value = value;
    }
}
