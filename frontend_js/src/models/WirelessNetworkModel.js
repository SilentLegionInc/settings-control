import { NetworkRequiredParamsModel } from './NetworkRequiredParamsModel';

export class WirelessNetworkModel {
    constructor(name, id, mode, channel, frequency, speedRate, signalLevel, security, device, active, autoconnect, params) {
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
        this.autoconnect = autoconnect;
        this.requiredParams = new NetworkRequiredParamsModel(params['ipv4.addresses'],
            params['ipv4.method'], params['ipv4.gateway'], params['ipv4.dns']);

        if (params.hasOwnProperty('ipv4.addresses')) {
            delete params['ipv4.addresses'];
        }
        if (params.hasOwnProperty('ipv4.method')) {
            delete params['ipv4.method'];
        }
        if (params.hasOwnProperty('ipv4.gateway')) {
            delete params['ipv4.gateway'];
        }
        if (params.hasOwnProperty('ipv4.dns')) {
            delete params['ipv4.dns'];
        }

        this.additionalParams = params;
    }
}
