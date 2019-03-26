export class WirelessNetworkModel {
    constructor(name, id, mode, channel, frequency, speedRate, signalLevel, security, device, active) {
        this.name = name;
        this.id = id;
        this.mode = mode;
        this.channel = channel;
        this.frequency = frequency;
        this.security = security;
        this.signalLevel = signalLevel;
        this.speedRate = speedRate;
        this.channel = channel;
        this.device = device;
        this.active = active;
    }
}
