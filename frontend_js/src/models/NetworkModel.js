export class NetworkModel {
    constructor(ssid, security, signal, rate, bars, channel, inUse, mode, detail = false) {
        this.name = ssid;
        this.security = security;
        this.signal = signal;
        this.rate = rate;
        this.bars = bars.replace(new RegExp('_', 'g'), '');
        this.channel = channel;
        this.active = inUse === '+';
        this.mode = mode;
        this.detail = detail;
    }
}
