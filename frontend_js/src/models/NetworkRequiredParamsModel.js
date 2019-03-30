export class NetworkRequiredParamsModel {
    constructor(ipv4address, ipv4method, ipv4gateway, ipv4dns) {
        this.ipv4address = ipv4address;
        this._ipv4method = ipv4method;
        this.ipv4gateway = ipv4gateway;
        this.ipv4dns = ipv4dns;
    }
    get ipv4method() {
        return this._ipv4method === 'auto'
    }
    set ipv4method(value) {
        this._ipv4method = value ? 'auto' : 'manual'
    }
    toPythonDict() {
        return {
            'ipv4.address': this.ipv4address,
            'ipv4.method': this._ipv4method,
            'ipv4.gateway': this.ipv4gateway,
            'ipv4.dns': this.ipv4dns
        }
    }
}
