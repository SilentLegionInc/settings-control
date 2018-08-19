export class LogModel {
    constructor(id: number = 0, type: LogLevel = 0, title: string = '', message: string = '', time: Date = new Date()) {
        this.id = id;
        this.type = type;
        this.title = title;
        this.message = message;
        this.time = time;
    }

    public id: number = 0;
    public type: LogLevel = 0;
    public title: string = '';
    public message: string = '';
    public time: Date = new Date();
}

export enum LogLevel {
    Critical = 0,
    Warning,
    Debug,
    Info,
}
