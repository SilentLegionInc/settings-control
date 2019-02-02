import axios from 'axios';
import { MapperService } from './MapperService';
import Logger from '../logger';
import store from '../store';
import { ServerExceptionModel } from '../models/ServerExceptionModel';

export class RequestService {
    constructor(host, port) {
        this._serverHost = host; // Config.get('backendHost')
        this._serverPort = port; // Config.get('backendPort');
        this._serverUri = `http://${this._serverHost}:${this._serverPort}`;
        axios.defaults.validateStatus = function (status) {
            return status <= 500; // Reject only if the status code is greater than 500
        }
        Logger.info('i\'m born');
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

    async changePassword(oldPassword, newPassword) {
        const path = this._constructPath(`api/password`);
        const res = await axios.post(path, { oldPassword, newPassword });
        if (res.status === 200) {
            const body = res.data;
            store.commit('setAuthToken', body.token)
        } else {
            Logger.error(res.data.errorInfo);
            throw new ServerExceptionModel(res.data.errorInfo, res.status);
        }
    }

    async getNetworks() {
        const path = this._constructPath('api/wifi');
        const res = await axios.get(path);
        if (res.status === 200) {
            return MapperService.mapNetworksResponse(res.data);
        } else {
            Logger.error(res.data.errorInfo);
            throw new ServerExceptionModel(res.data.errorInfo, res.status);
        }
    }

    async changeNetwork(name, password) {
        const path = this._constructPath('api/wifi/connect');
        const res = await axios.post(path, { name, password });
        if (res.status === 200) {
            return true
        } else {
            Logger.error(res.data.errorInfo);
            throw new ServerExceptionModel(res.data.errorInfo, res.status);
        }
    }

    async getCoreConfig() {
        const path = this._constructPath('api/config');
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
        if (startTime != null) {
            body['start_time'] = startTime;
            if (typeof body['start_time'] !== 'string') {
                body['start_time'] = body['start_time'].toISOString();
            }
        }
        if (endTime != null) {
            body['end_time'] = endTime.toISOString();
            if (typeof body['end_time'] !== 'string') {
                body['end_time'] = body['end_time'].toISOString();
            }
        }
        if (type != null) {
            body['type'] = type;
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

        Logger.debug('POST request: get logs');
        Logger.debug(`Path: ${path}`);
        Logger.debug(`Body: ${JSON.stringify(body)}`);

        const result = await axios.post(path, body);
        return MapperService.mapLogsResponse(result.data);
    }

    async getStatisticsData(robotName, fieldName, limit = 1, offset = 0, startTime = null, endTime = null) {
        const path = this._constructPath(`api/monitoring/data/${robotName}`);

        const body = {};
        body['field_name'] = fieldName;
        if (startTime != null) {
            body['start_time'] = startTime;
            if (typeof body['start_time'] !== 'string') {
                body['start_time'] = body['start_time'].toISOString();
            }
        }
        if (endTime != null) {
            body['end_time'] = endTime.toISOString();
            if (typeof body['end_time'] !== 'string') {
                body['end_time'] = body['end_time'].toISOString();
            }
        }
        if (limit != null) {
            body['limit'] = limit;
        }
        if (offset != null) {
            body['offset'] = offset;
        }

        Logger.debug('POST request: get statistics data');
        Logger.debug(`Path: ${path}`);
        Logger.debug(`Body: ${JSON.stringify(body)}`);

        const result = await axios.post(path, body);
        return MapperService.mapChartDataResponse(result.data);
    }

    async getStatisticsDataStructure(robotName) {
        const path = this._constructPath(`api/monitoring/structure/${robotName}`);

        Logger.debug('GET request: get statistics data structure');
        Logger.debug(`Path: ${path}`);

        const result = await axios.get(path);
        return MapperService.mapDataStructureResponse(result.data);
    }
}
