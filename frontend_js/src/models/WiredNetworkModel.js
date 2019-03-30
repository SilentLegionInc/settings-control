import { NetworkRequiredParamsModel } from './NetworkRequiredParamsModel';

export class WiredNetworkModel {
    constructor(name, id, device, active, autoconnect, params) {
        this.name = name;
        this.id = id;
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
