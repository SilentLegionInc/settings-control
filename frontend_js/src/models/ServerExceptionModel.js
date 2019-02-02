export class ServerExceptionModel extends Error {
    constructor(message, status) {
        super();
        this.message = message;
        this.status = status
    }

    toString() {
        return `Code: ${this.status}. Description: ${this.message}`;
    }
}
