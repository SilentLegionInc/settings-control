import { LogsResponse } from '../models/LogsResponse';
import { NetworkModel } from '../models/NetworkModel';
import { LogModel } from '../models/LogModel';
import { ChartDataResponse } from '../models/ChartDataResponse';
import { ChartDataModel } from '../models/ChartDataModel';
import { DataStructureModel } from '../models/DataStructureModel';
import { MapsDataModel } from '../models/MapsDataModel';
import { TableDataResponse } from '../models/TableDataResponse'
import { TableDataModel } from '../models/TableDataModel'

export class MapperService {
    static mapNetworksResponse(responseBody) {
        return responseBody.map(elem => new NetworkModel(elem.ssid, elem.security, elem.signal, elem.rate, elem.bars,
            elem.chan, elem['in-use'], elem.mode, false));
    }

    static mapLogsResponse(responseBody) {
        const res = new LogsResponse();
        res.count = responseBody.count;
        res.result = responseBody.result.map(elem => new LogModel(elem.id, new Date(elem.time), elem.type, elem.title, elem.message));
        return res;
    }
    
    static mapTableDataResponse(responseBody) {
        const res = new TableDataResponse();
        res.count = responseBody.count;
        res.result = responseBody.result.map(elem => new TableDataModel(elem));
        res.dataStructure = this.mapDataStructureResponse(responseBody['data_structure'])
        return res;
    }

    static mapChartDataResponse(responseBody) {
        const res = new ChartDataResponse();
        res.count = responseBody.count;
        res.minimum = responseBody.minimum;
        res.average = responseBody.average;
        res.maximum = responseBody.maximum;
        res.result = responseBody.result.map(elem => new ChartDataModel(elem.latitude, elem.longitude, new Date(elem.time), elem.value));
        return res;
    }

    static mapDataStructureResponse(responseBody) {
        return responseBody.map(elem => new DataStructureModel(elem.name, elem.system_name, elem.type));
    }
    
    static mapMapsDataResponse(responseBody) {
        return new MapsDataModel(
            responseBody['points'].map(elem => {
                return {
                    latitude: elem.latitude,
                    longitude: elem.longitude,
                    count: elem.count
                }
            }),
            responseBody['center_latitude'],
            responseBody['center_longitude']
        );
    }
}
