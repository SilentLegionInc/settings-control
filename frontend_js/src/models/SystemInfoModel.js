import { MemoryInfoModel } from './MemoryInfoModel';

export class SystemInfoModel {
    constructor(cpuInfo = {}, diskInfo = {}, memoryInfo = new MemoryInfoModel()) {
        this.cpuInfo = cpuInfo;
        this.diskInfo = diskInfo;
        this.memoryInfo = memoryInfo;
    }
}
