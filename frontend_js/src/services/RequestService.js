import axios from 'axios';
import { MapperService } from './MapperService';
import Logger from '../logger';
import { ServerExceptionModel } from '../models/ServerExceptionModel';

export class RequestService {
    constructor(url) {
        this._serverUrl = `http://${url}`;
        axios.defaults.validateStatus = function (status) {
            return status <= 500; // Reject only if the status code is greater than 500
        }
    }

    _changeHostUrl(url) {
        this._serverUrl = `http://${url}`;
    }

    _constructPath(route, anotherUrl = null) {
        if (!anotherUrl) {
            return `${this._serverUrl}/${route}`;
        } else {
            return `http://${anotherUrl}/${route}`;
        }
    }

    _deleteAuthHeader() {
        Logger.info(`Deleting auth token`);
        delete axios.defaults.headers.common['authorization'];
    }

    _setAuthHeader(token) {
        Logger.info(`Setting new token ${token}`);
        axios.defaults.headers.common['authorization'] = token;
    }

    async _authorize(password) {
        const path = this._constructPath(`api/login`);
        const result = await axios.post(path, { password });
        console.log(result.status);
        if (result.status === 200) {
            const body = result.data;
            return body.token;
        } else {
            // TODO Log normal. + Unauth
            Logger.info(result.data.errorInfo);
            throw new ServerExceptionModel(result.data.errorInfo, result.status);
            // Logger.error(result);
            // return false;
        }
    }

    async _deauthorize() {
        const path = this._constructPath(`api/logout`);
        const result = await axios.get(path);
        console.log(result.status);
        if (result.status === 200) {
            return true;
        } else {
            Logger.error(result.data.errorInfo);
            throw new ServerExceptionModel(result.data.errorInfo, result.status);
        }
    }

    async _changePassword(oldPassword, newPassword) {
        const path = this._constructPath(`api/password`);
        const res = await axios.post(path, { oldPassword, newPassword });
        if (res.status === 200) {
            const body = res.data;
            return body.token;
        } else {
            Logger.error(res.data.errorInfo);
            throw new ServerExceptionModel(res.data.errorInfo, res.status);
        }
    }

    async getHealth(url = null) {
        const path = this._constructPath('api/utils/health', url);
        try {
            const res = await axios.get(path, { timeout: 1000 });
            return res.status === 200 && res.data.code === 0;
        } catch (e) {
            return false;
        }
    }

    async getNetworks() {
        const path = this._constructPath('api/network');
        const res = await axios.get(path);
        if (res.status === 200) {
            return MapperService.mapNetworksResponse(res.data);} else {
            Logger.error(res.data.errorInfo);
            throw new ServerExceptionModel(res.data.errorInfo, res.status);
        }
    }

    async getModules() {
        const path = this._constructPath('api/modules');
        const res = await axios.get(path);
        if (res.status === 200) {
            return MapperService.mapModulesResponse(res.data);
        } else {
            Logger.error(res.data.errorInfo);
            throw new ServerExceptionModel(res.data.errorInfo, res.status);
        }
    }

    async createWifiConnection(name, password) {
        const path = this._constructPath('api/network/create_wifi_connection');
        const res = await axios.post(path, { name, password });
        if (res.status === 200) {
            return true
        } else {
            Logger.error(res.data.errorInfo);
            throw new ServerExceptionModel(res.data.errorInfo, res.status);
        }
    }

    async connectionUp(id) {
        const path = this._constructPath(`api/network/connection/up/${id}`);
        const res = await axios.get(path);
        if (res.status === 200) {
            return true
        } else {
            Logger.error(res.data.errorInfo);
            throw new ServerExceptionModel(res.data.errorInfo, res.status);
        }
    }

    async getServerConfig() {
        const path = this._constructPath('api/server_config');
        const res = await axios.get(path);
        if (res.status === 200) {
            return MapperService.mapServerSettingsResponse(res.data);
        } else {
            Logger.error(res.data.errorInfo);
            throw new ServerExceptionModel(res.data.errorInfo, res.status);
        }
    }

    async runCore() {
        const path = this._constructPath('api/core/run');
        const res = await axios.post(path);
        if (res.status === 200) {
            return res.data.core_status;
        } else {
            Logger.error(res.data.errorInfo);
            throw new ServerExceptionModel(res.data.errorInfo, res.status);
        }
    }
    async stopCore() {
        const path = this._constructPath('api/core/stop');
        const res = await axios.post(path);
        if (res.status === 200) {
            return !res.data.core_status;
        } else {
            Logger.error(res.data.errorInfo);
            throw new ServerExceptionModel(res.data.errorInfo, res.status);
        }
    }

    async getCoreIsActive() {
        const path = this._constructPath('api/core/status');
        const res = await axios.get(path);
        if (res.status === 200) {
            return res.data.core_status;
        } else {
            Logger.error(res.data.errorInfo);
            throw new ServerExceptionModel(res.data.errorInfo, res.status);
        }
    }

    async setServerConfig(newConfig) {
        const path = this._constructPath('api/server_config');
        const res = await axios.post(path, newConfig);
        if (res.status === 200) {
            // TODO change answer format in backend
            return true;
        } else {
            Logger.error(res.data.errorInfo);
            throw new ServerExceptionModel(res.data.errorInfo, res.status);
        }
    }

    async getCoreConfig() {
        const path = this._constructPath('api/core_config');
        const res = await axios.get(path);
        if (res.status === 200) {
            return res.data;
        } else {
            Logger.error(res.data.errorInfo);
            throw new ServerExceptionModel(res.data.errorInfo, res.status);
        }
    }

    async setCoreConfig(newConfig) {
        const path = this._constructPath('api/config');
        const res = await axios.post(path, newConfig);
        if (res.status === 200) {
            // TODO change answer format in backend
            return true;
        } else {
            Logger.error(res.data.errorInfo);
            throw new ServerExceptionModel(res.data.errorInfo, res.status);
        }
    }

    async getLogs(robotName, limit = 1, offset = 0, startTime = null, endTime = null, type = null, sortByTime = null, sortByType = null) {
        const path = this._constructPath(`api/monitoring/logs/${robotName}`);

        const body = {};
        body['filter'] = {};
        body['sort'] = {};
        if (startTime != null) {
            body['filter']['start_time'] = startTime;
            if (typeof body['filter']['start_time'] !== 'string') {
                body['filter']['start_time'] = body['filter']['start_time'].toISOString();
            }
        }
        if (endTime != null) {
            body['filter']['end_time'] = endTime.toISOString();
            if (typeof body['filter']['end_time'] !== 'string') {
                body['filter']['end_time'] = body['filter']['end_time'].toISOString();
            }
        }
        if (type != null) {
            body['filter']['type'] = type;
        }
        if (sortByTime != null) {
            body['sort']['time'] = sortByTime ? 1 : 0;
        }
        if (sortByType != null) {
            body['sort']['type'] = sortByType ? 1 : 0;
        }
        if (limit != null) {
            body['limit'] = limit;
        }
        if (offset != null) {
            body['offset'] = offset;
        }

        Logger.debug('POST request: get logs');
        Logger.debug(`Path: ${path}`);
        Logger.debug(`Body: ${JSON.stringify(body)}`);

        const result = await axios.post(path, body);
        if (result.status === 200) {
            return MapperService.mapLogsResponse(result.data);
        } else {
            Logger.error(result.data.errorInfo);
            throw new ServerExceptionModel(result.data.errorInfo, result.status);
        }
    }

    async getStatisticsDataStructure(robotName, dbName) {
        const path = this._constructPath(`api/monitoring/structure/${robotName}/${dbName}`);

        Logger.debug('GET request: get statistics data structure');
        Logger.debug(`Path: ${path}`);

        const result = await axios.get(path);
        if (result.status === 200) {
            return MapperService.mapDataStructureResponse(result.data);
        } else {
            Logger.error(result.data.errorInfo);
            throw new ServerExceptionModel(result.data.errorInfo, result.status);
        }
    }

    async getStatisticsDatabasesInfo(robotName) {
        const path = this._constructPath(`api/monitoring/databases_info/${robotName}`);

        Logger.debug('GET request: get statistics databases info');
        Logger.debug(`Path: ${path}`);

        const result = await axios.get(path);
        if (result.status === 200) {
            return MapperService.mapDatabasesInfoResponse(result.data);
        } else {
            Logger.error(result.data.errorInfo);
            throw new ServerExceptionModel(result.data.errorInfo, result.status);
        }
    }

    async getStatisticsInitChartData(robotName, dbName, fieldName, intervalSize) {
        const path = this._constructPath(`api/monitoring/chart_data/${robotName}/${dbName}/${fieldName}?interval_size=${intervalSize}`);

        Logger.debug('GET request: get statistics init chart data');
        Logger.debug(`Path: ${path}`);

        const result = await axios.get(path);
        if (result.status === 200) {
            return MapperService.mapInitChartDataResponse(result.data);
        } else {
            Logger.error(result.data.errorInfo);
            throw new ServerExceptionModel(result.data.errorInfo, result.status);
        }
    }

    async getStatisticsFilterChartData(robotName, dbName, fieldName, minTime, maxTime, intervalSize) {
        const path = this._constructPath(`api/monitoring/chart_data/${robotName}/${dbName}/${fieldName}`);

        if (typeof minTime !== 'string') {
            minTime = minTime.toISOString();
        }
        if (typeof maxTime !== 'string') {
            maxTime = maxTime.toISOString();
        }

        const body = {};
        body['min_time'] = minTime;
        body['max_time'] = maxTime;
        body['interval_size'] = intervalSize;

        Logger.debug('POST request: get statistics filter chart data');
        Logger.debug(`Path: ${path}`);
        Logger.debug(`Body: ${JSON.stringify(body)}`);

        const result = await axios.post(path, body);
        if (result.status === 200) {
            return MapperService.mapFilterChartDataResponse(result.data);
        } else {
            Logger.error(result.data.errorInfo);
            throw new ServerExceptionModel(result.data.errorInfo, result.status);
        }
    }

    async getStatisticsPageChartData(robotName, dbName, fieldName, intervalStartTime, intervalEndTime) {
        const path = this._constructPath(`api/monitoring/chart_data/${robotName}/${dbName}/${fieldName}?page=true`);

        if (typeof intervalStartTime !== 'string') {
            intervalStartTime = intervalStartTime.toISOString();
        }
        if (typeof intervalEndTime !== 'string') {
            intervalEndTime = intervalEndTime.toISOString();
        }

        const body = {};
        body['interval_start_time'] = intervalStartTime;
        body['interval_end_time'] = intervalEndTime;

        Logger.debug('POST request: get statistics page chart data');
        Logger.debug(`Path: ${path}`);
        Logger.debug(`Body: ${JSON.stringify(body)}`);

        const result = await axios.post(path, body);
        if (result.status === 200) {
            return MapperService.mapPageChartDataResponse(result.data);
        } else {
            Logger.error(result.data.errorInfo);
            throw new ServerExceptionModel(result.data.errorInfo, result.status);
        }
    }

    async getStatisticsTableData(robotName, dbName, limit = 1, offset = 0, extended = false, filter = {}, sort = {}) {
        const path = this._constructPath(`api/monitoring/table_data/${robotName}/${dbName}`);

        const body = {};
        body['filter'] = {};
        body['sort'] = {};
        body['extended'] = extended;

        if (limit != null) {
            body['limit'] = limit;
        }
        if (offset != null) {
            body['offset'] = offset;
        }

        for (let filterElem in filter) {
            if (filter.hasOwnProperty(filterElem)) {
                const newName = filterElem.replace(/([A-Z])/g, '_$1').toLowerCase();
                body['filter'][newName] = filter[filterElem];
                if (['startTime', 'endTime'].includes(filterElem) && body['filter'][newName] && typeof body['filter'][newName] !== 'string') {
                    body['filter'][newName] = body['filter'][newName].toISOString();
                }
            }
        }

        for (let sortElem in sort) {
            if (sort.hasOwnProperty(sortElem)) {
                const newName = sortElem.replace(/([A-Z])/g, '_$1').toLowerCase();
                body['sort'][newName] = sort[sortElem]
            }
        }

        Logger.debug('POST request: get logs');
        Logger.debug(`Path: ${path}`);
        Logger.debug(`Body: ${JSON.stringify(body)}`);

        const result = await axios.post(path, body);
        if (result.status === 200) {
            return MapperService.mapTableDataResponse(result.data);
        } else {
            Logger.error(result.data.errorInfo);
            throw new ServerExceptionModel(result.data.errorInfo, result.status);
        }
    }

    async getSystemInfo(extended = true) {
        const path = this._constructPath(`api/monitoring/system_info?extended=${extended}`);

        Logger.debug('GET request: get system info');
        Logger.debug(`Path: ${path}`);

        const result = await axios.get(path);
        if (result.status === 200) {
            return MapperService.mapSystemInfoResponse(result.data);
        } else {
            Logger.error(result.data.errorInfo);
            throw new ServerExceptionModel(result.data.errorInfo, result.status);
        }
    }

    async getStatisticsMapsData(robotName, dbName, onlyFields, filter = {}) {
        const path = this._constructPath(`api/monitoring/maps_data/${robotName}/${dbName}`);

        let result = null;
        if (onlyFields) {
            Logger.debug('GET request: get statistics maps data');
            Logger.debug(`Path: ${path}`);

            result = await axios.get(path);
        } else {
            Logger.debug('POST request: get statistics maps data');
            Logger.debug(`Path: ${path}`);

            const body = {};

            if (filter.startTime != null) {
                body['start_time'] = filter.startTime;
                if (typeof body['start_time'] !== 'string') {
                    body['start_time'] = body['start_time'].toISOString();
                }
            }
            if (filter.endTime != null) {
                body['end_time'] = filter.endTime;
                if (typeof body['end_time'] !== 'string') {
                    body['end_time'] = body['end_time'].toISOString();
                }
            }

            result = await axios.post(path, body);
        }
        if (result.status === 200) {
            return MapperService.mapMapsDataResponse(result.data);
        } else {
            Logger.error(result.data.errorInfo);
            throw new ServerExceptionModel(result.data.errorInfo, result.status);
        }
    }

    async uploadModuleArchive(formData, moduleName) {
        const path = this._constructPath(`api/update_module/${moduleName}`);

        Logger.debug('POST request: upload file');
        Logger.debug(`Path: ${path}`);

        const result = await axios.post(path, formData, { headers: { 'Content-Type': 'multipart/form-data' } });
        if (result.status === 200) {
            return true;
        } else {
            Logger.error(`Can't upload file`);
            throw new ServerExceptionModel(result.data.errorInfo, result.status);
        }
    }

    async cloneModule(moduleName) {
        const path = this._constructPath(`api/clone_module/${moduleName}`);
        const result = await axios.get(path);
        if (result.status === 200) {
            return true;
        } else {
            throw new ServerExceptionModel(result.data.errorInfo, result.status);
        }
    }

    async buildModule(moduleName) {
        const path = this._constructPath(`api/build_module/${moduleName}`);
        const result = await axios.get(path);
        if (result.status === 200) {
            return true;
        } else {
            throw new ServerExceptionModel(result.data.errorInfo, result.status);
        }
    }

    async uploadSSHArchive(formData) {
        const path = this._constructPath(`api/update_ssh`);
        const result = await axios.post(path, formData, { headers: { 'Content-Type': 'multipart/form-data' } });
        if (result.status === 200) {
            // TODO change answer format in backend
            return true;
        } else {
            Logger.error(result.data.errorInfo);
            throw new ServerExceptionModel(result.data.errorInfo, result.status);
        }
    }
}
