export class LogModel {
    constructor(time = new Date(), type = 0, title = '', message = '') {
        this.time = time;
        this.type = type;
        this.title = title;
        this.message = message;
    }
}

export const LogLevel = {
    CRITICAL: 0,
    WARNING: 1,
    DEBUG: 2,
    INFO: 3
}
Object.freeze(LogLevel)
LogModel.LogLevel = LogLevel;
