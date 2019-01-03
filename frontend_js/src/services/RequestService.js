import axios from 'axios';
import { MapperService } from './MapperService';
import Logger from '../logger';

export class RequestService {
    constructor(host, port) {
        this._serverHost = host; // Config.get('backendHost')
        this._serverPort = port; // Config.get('backendPort');
        this._serverUri = `http://${this._serverHost}:${this._serverPort}`
    }
    
    _constructPath(route) {
        return `${this._serverUri}/${route}`
    }

    _setAuthHeader(token) {
        Logger.info(`Setting new token ${token}`);
        axios.defaults.headers.common['authorization'] = token;
    }

    async _authorize(password) {
        const path = this._constructPath(`api/login`);
        const result = await axios.post(path, { password });
        if (result.status === 200) {
            const body = result.data;
            return body.token;
        } else {
            // TODO Log normal
            Logger.error(result);
            return false;
        }
    }
    
    async getLogs(robotName, limit = 1, offset = 0, startTime = null, endTime = null, type = null, sortByTime = null, sortByType = null) {
        const path = this._constructPath(`api/monitoring/logs/${robotName}`);
    
        const body = {};
        if (startTime != null) {
            body['start_time'] = startTime;
        }
        if (endTime != null) {
            body['start_time'] = endTime;
        }
        if (type != null) {
            body['type'] = endTime;
        }
        if (sortByTime != null) {
            body['sort_by_time'] = sortByTime ? 1 : 0;
        }
        if (sortByType != null) {
            body['sort_by_type'] = sortByType ? 1 : 0;
        }
        if (limit != null) {
            body['limit'] = limit;
        }
        if (offset != null) {
            body['offset'] = offset;
        }
        
        Logger.debug('Request: get logs');
        Logger.debug(`Path: ${path}`);
        Logger.debug(`Body: ${JSON.stringify(body)}`);
        
        const result = await axios.post(path, body);
        return MapperService.mapLogsResponse(result.data);
    }
}
