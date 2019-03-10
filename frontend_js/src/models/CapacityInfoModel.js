export class CapacityInfoModel {
    constructor(percent = 0, free = 0, used = 0, total = 0) {
        this.percent = percent;
        this.free = free;
        this.used = used;
        this.total = total;
    }
}
