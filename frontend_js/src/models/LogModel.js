export class LogModel {
    constructor(id = 0, time = new Date(), type = 0, title = '', message = '') {
        this.id = id;
        this.time = time;
        this.type = type;
        this.title = title;
        this.message = message;
    }
}

export const LogLevel = {
    CRITICAL: 1,
    WARNING: 2,
    DEBUG: 3,
    INFO: 4
}
Object.freeze(LogLevel)
LogModel.LogLevel = LogLevel;
