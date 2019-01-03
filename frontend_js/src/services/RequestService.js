import Config from '../config';
import axios from 'axios';
import {MapperService} from './MapperService'

class RequestService {
    constructor() {
        this._serverHost = Config.get("host")
        this._serverPort = Config.get("port")
        this._serverUri = `http://${this._serverHost}:${this._serverPort}`
    }
    
    _constructPath(route) {
        return `${this._serverUri}/${route}`
    }
    
    async getLogs(robotName, startTime = null, endTime = null, type = null, sortByTime = null, sortByType = null, limit = null, offset = null) {
        let path = this._constructPath(`api/monitoring/logs/${robotName}`);
        
        let body = {};
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
            body['offset'] = limit;
        }
        
        let result = await axios.post(path, body);
        return MapperService.mapLogsResponse(result.data);
    }
}
