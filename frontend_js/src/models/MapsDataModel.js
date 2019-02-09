export class MapsDataModel {
    constructor(points = [], centerLatitude = 0, centerLongitude = 0) {
        this.points = points;
        this.centerLatitude = centerLatitude;
        this.centerLongitude = centerLongitude;
    }
}
