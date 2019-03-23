export class InitChartDataResponse {
    constructor(result = [], minTime = null, maxTime = null, intervalStartTime = null,
                intervalEndTime = null, minimum = 0, average = 0, maximum = 0) {
        this.result = result;
        this.minTime = minTime;
        this.maxTime = maxTime;
        this.intervalStartTime = intervalStartTime;
        this.intervalEndTime = intervalEndTime;
        this.minimum = minimum;
        this.average = average;
        this.maximum = maximum;
    }
}
