import { LogsResponse } from '../models/LogsResponse'
import { LogModel } from '../models/LogModel'

export class MapperService {
    static mapLogsResponse(responseBody) {
        const res = new LogsResponse();
        res.count = responseBody.count;
        res.result = responseBody.result.map(elem => new LogModel(new Date(elem.time), elem.type, elem.title, elem.message));
        return res;
    }
}
