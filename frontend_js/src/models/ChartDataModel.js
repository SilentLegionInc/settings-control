export class ChartDataModel {
    constructor(latitude = 0, longitude = 0, time = new Date(), value = 0) {
        this.latitude = latitude;
        this.longitude = longitude;
        this.time = time;
        this.value = value;
    }
}
