import { ServerExceptionModel } from './models/ServerExceptionModel';
import Logger from './logger';
import { ClientExceptionModel } from './models/ClientExceptionModel';

export async function catchErrorsWrapper(errorHandler, func) {
    try {
        await func();
    } catch (err) {
        if (err instanceof ServerExceptionModel) {
            errorHandler.error(err.message);
        } else if (err instanceof ClientExceptionModel) {
            errorHandler.error('Ошибка клиента');
            Logger.error(err.message);
        } else {
            errorHandler.error('Ошибка сервера');
            Logger.error(err);
        }
    }
}
