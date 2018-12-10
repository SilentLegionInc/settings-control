export class LogModel {
    constructor(id: number = 0, time: Date = new Date(), type: LogLevel = 0, title: string = '', message: string = '') {
        this.id = id;
        this.time = time;
        this.type = type;
        this.title = title;
        this.message = message;
    }

    public id: number = 0;
    public time: Date = new Date();
    public type: LogLevel = 0;
    public title: string = '';
    public message: string = '';
}

export enum LogLevel {
    Critical = 0,
    Warning,
    Debug,
    Info
}
