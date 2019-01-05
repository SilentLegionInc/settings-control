import { LogsResponse } from '../models/LogsResponse';
import { LogModel } from '../models/LogModel';
import { ChartDataResponse } from '../models/ChartDataResponse';
import { ChartDataModel } from '../models/ChartDataModel';

export class MapperService {
    static mapLogsResponse(responseBody) {
        const res = new LogsResponse();
        res.count = responseBody.count;
        res.result = responseBody.result.map(elem => new LogModel(new Date(elem.time), elem.type, elem.title, elem.message));
        return res;
    }
    
    static mapChartDataResponse (responseBody) {
        const res = new ChartDataResponse();
        res.count = responseBody.count;
        res.result = responseBody.result.map(elem => new ChartDataModel(elem.latitude, elem.longitude, new Date(elem.time), elem.value));
        return res;
    }
}
