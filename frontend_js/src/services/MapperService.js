import { LogsResponse } from '../models/LogsResponse';
import { ServerSettingsModel } from '../models/ServerSettingsModel';
import { NetworkModel } from '../models/NetworkModel';
import { LogModel } from '../models/LogModel';
import { ChartDataResponse } from '../models/ChartDataResponse';
import { ChartDataModel } from '../models/ChartDataModel';
import { MapsDataModel } from '../models/MapsDataModel';
import { TableDataResponse } from '../models/TableDataResponse'
import { TableDataModel } from '../models/TableDataModel'
import { ShortDataStructureModel } from '../models/ShortDataStructureModel'
import { DataStructureElementModel } from '../models/DataStructureElementModel';
import { ModuleModel } from '../models/ModuleModel'
import { CapacityInfoModel } from '../models/CapacityInfoModel';
import { MemoryInfoModel } from '../models/MemoryInfoModel';
import { SystemInfoModel } from '../models/SystemInfoModel';

export class MapperService {
    static mapNetworksResponse(responseBody) {
        return responseBody.map(elem => new NetworkModel(elem.ssid, elem.security, elem.signal, elem.rate, elem.bars,
            elem.chan, elem['in-use'], elem.mode, false));
    }

    static mapModulesResponse(responseBody) {
        const coreInfo = responseBody.core;
        const dependencies = responseBody.dependencies;
        return {
            core: new ModuleModel(coreInfo.name, coreInfo.url, coreInfo.build_modify_time, coreInfo.src_modify_time,
                coreInfo.is_built, coreInfo.is_cloned, null, coreInfo.config_path, coreInfo.execute, coreInfo.is_active),
            dependencies: dependencies.map(x => new ModuleModel(x.name, x.url, x.build_modify_time, x.src_modify_time,
                x.is_built, x.is_cloned, x.index, null, null))
        }
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
        if (responseBody['data_structure']) {
            res.dataStructure = this.mapDataStructureResponse(responseBody['data_structure'])
        }
        return res;
    }

    static mapServerSettingsResponse(responseBody) {
        return new ServerSettingsModel(responseBody['type'], responseBody['sources_path'],
            responseBody['builds_path'], responseBody['upload_path'], responseBody['qmake_path'],
            responseBody['ssh_key_name'], responseBody['repositories_platform'],
            responseBody['possible_machines_types']);
    }

    static mapChartDataResponse(responseBody) {
        const res = new ChartDataResponse();
        res.count = responseBody.count;
        res.minimum = responseBody.minimum;
        res.average = responseBody.average;
        res.maximum = responseBody.maximum;
        res.result = responseBody.result.map(elem => new ChartDataModel(elem.id, elem.latitude, elem.longitude, new Date(elem.time), elem.value));
        return res;
    }

    static mapDataStructureResponse(responseBody) {
        return responseBody.map(elem => new DataStructureElementModel(elem.name, elem.system_name, elem.type));
    }

    static mapDatabasesInfoResponse(responseBody) {
        const result = [];
        for (let key in responseBody) {
            if (responseBody.hasOwnProperty(key)) {
                result.push(new ShortDataStructureModel(responseBody[key], key));
            }
        }
        return result
    }

    static mapMapsDataResponse(responseBody) {
        if (Array.isArray(responseBody)) {
            return responseBody.map(elem => {
                return {
                    name: elem['name'],
                    systemName: elem['system_name']
                }
            });
        } else {
            return new MapsDataModel(
                responseBody['points'].map(elem => {
                    const result = {
                        latitude: elem.latitude,
                        longitude: elem.longitude,
                        count: elem.count,
                        average: {}
                    };
                    for (let key in elem.average) {
                        if (elem.average.hasOwnProperty(key)) {
                            result.average[key] = {
                                name: elem.average[key].name,
                                value: elem.average[key].value
                            };
                        }
                    }
                    return result;
                }),
                responseBody['center_latitude'],
                responseBody['center_longitude']
            );
        }
    }

    static mapSystemInfoResponse(responseBody) {
        function mapCpuInfo(cpuInfoResponse) {
            let result = {};
            for (let cpuName in cpuInfoResponse) {
                if (cpuInfoResponse.hasOwnProperty(cpuName)) {
                    result[cpuName] = cpuInfoResponse[cpuName];
                }
            }
            return result;
        }

        function mapDiskInfo(diskInfoResponse) {
            let result = [];
            for (let diskName in diskInfoResponse) {
                if (diskInfoResponse.hasOwnProperty(diskName)) {
                    result.push({
                        name: diskName,
                        info: new CapacityInfoModel(
                            diskInfoResponse[diskName].percent,
                            diskInfoResponse[diskName].free,
                            diskInfoResponse[diskName].used,
                            diskInfoResponse[diskName].total
                        )
                    });
                }
            }
            return result;
        }

        function mapMemoryInfo(memoryInfoResponse) {
            let ramInfo = new CapacityInfoModel(
                memoryInfoResponse['ram_info'].percent,
                memoryInfoResponse['ram_info'].free,
                memoryInfoResponse['ram_info'].used,
                memoryInfoResponse['ram_info'].total
            );
            let swapInfo = new CapacityInfoModel(
                memoryInfoResponse['swap_info'].percent,
                memoryInfoResponse['swap_info'].free,
                memoryInfoResponse['swap_info'].used,
                memoryInfoResponse['swap_info'].total
            );
            return new MemoryInfoModel(ramInfo, swapInfo);
        }

        if (responseBody['memory']) {
            return new SystemInfoModel(
                mapCpuInfo(responseBody['cpu']),
                mapDiskInfo(responseBody['disk']),
                mapMemoryInfo(responseBody['memory'])
            );
        } else {
            return mapCpuInfo(responseBody);
        }
    }
}
