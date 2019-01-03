import Logger from 'js-logger';
import Config from './config'

const levels = {
    TRACE: Logger.TRACE,
    DEBUG: Logger.DEBUG,
    INFO: Logger.INFO,
    TIME: Logger.TIME,
    WARN: Logger.WARN,
    ERROR: Logger.ERROR,
    OFF: Logger.OFF
}

const logLevel = Config.get('loggingLevel');
Logger.useDefaults();
const logger = Logger.get('GlobalLogger');
logger.setLevel(levels[logLevel]);

export default logger;
