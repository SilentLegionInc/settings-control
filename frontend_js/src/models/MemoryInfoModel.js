import { CapacityInfoModel } from './CapacityInfoModel';

export class MemoryInfoModel {
    constructor(ramInfo = new CapacityInfoModel(), swapInfo = new CapacityInfoModel()) {
        this.ramInfo = ramInfo;
        this.swapInfo = swapInfo;
    }
}
