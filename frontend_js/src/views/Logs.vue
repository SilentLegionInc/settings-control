<template>
    <div>
        <form>
            <div class="row">
                <span class="col-md-3">
                    <span>Start time: </span>
                    <datetime v-model="filterStartTime" type="datetime" input-class="form-control"></datetime>
                </span>

                <span class="col-md-3">
                    <span>End time: </span>
                    <datetime v-model="filterEndTime" type="datetime" input-class="form-control"></datetime>
                </span>

                <span class="col-md-3">
                    <span>Type: </span>
                    <select class="form-control" v-model="filterType">
                        <option selected value> -- select an option -- </option>
                        <option value=0>Critical</option>
                        <option value=1>Warning</option>
                        <option value=2>Debug</option>
                        <option value=3>Info</option>
                    </select>
                </span>

                <span class="col-md-3">
                    <button type="button" class="btn btn-primary" @click="loadData(1)">Primary</button>
                </span>
            </div>
        </form>

        <hr>

        <table class="custom-table">
            <thead class="custom-table-header">
            <tr>
                <th>№</th>
                <th>Time</th>
                <th>Type</th>
                <th>Title</th>
                <th>Message</th>
            </tr>
            </thead>

            <tbody class="custom-table-body">
            <tr v-for="log in logs">
                <td>{{ log.id }}</td>
                <td>{{ log.time | moment("DD.MM.YYYY hh:mm:ss.SSS") }}</td>
                <td>{{ log.type | logLevelToString }}</td>
                <td>{{ log.title }}</td>
                <td>{{ log.message }}</td>
            </tr>
            </tbody>
        </table>

        <div class="col-md-12 margin-top-sm">
            <b-pagination class="pagination-nav"
                          size="md"
                          :total-rows="dbElementsCount"
                          v-model="currentPage"
                          :per-page="elementsPerPage"
                          align="center">
            </b-pagination>
        </div>
    </div>
</template>

<script>
import { LogLevel, LogModel } from '../models/LogModel';

export default {
    name: 'Logs',
    data: function() {
        return {
            logs: [],
            elementsPerPage: 20,
            _currentPage: 1,
            dbElementsCount: 0,
            filterStartTime: null,
            filterEndTime: null,
            filterType: null
        }
    },
    computed: {
        currentPage: {
            get: function() {
                return this._currentPage;
            },
            set: function(newPage) {
                this._currentPage = newPage;
                this.loadData(this._currentPage);
            }
        }
    },
    mounted: function() {
        this.currentPage = 1;
    },
    methods: {
        mockedLoadData: function(page) {
            this.dbElementsCount = 300;
            let data = [];
            for (let i = 0; i < this.dbElementsCount; ++i) {
                const t = i + 1;
                data.push(new LogModel(t, new Date(), 0, `Title ${t}`, `Very very very long message without any information ${t}`));
            }

            const offset = (page - 1) * this.elementsPerPage;
            const limit = this.elementsPerPage;
            console.log(data);
            if (offset > 0) {
                data.splice(0, (page - 1) * this.elementsPerPage);
            }
            console.log(data);
            this.logs = data.slice(0, limit);
            console.log(this.logs);
        },

        loadData: async function(page) {
            const offset = (page - 1) * this.elementsPerPage;
            const limit = this.elementsPerPage;
            const filterStartTime = this.filterStartTime ? new Date(this.filterStartTime) : null;
            const filterEndTime = this.filterEndTime ? new Date(this.filterEndTime) : null;
            const filterType = this.filterType ? parseInt(this.filterType) : null;

            const response = await this.$store.state.requestService.getLogs('AMTS', limit, offset, filterStartTime, filterEndTime, filterType);
            this.dbElementsCount = response.count;
            this.logs = response.result;
        }
    },
    filters: {
        logLevelToString: function(level) {
            switch (level) {
                case LogLevel.INFO:
                    return 'Info';
                case LogLevel.DEBUG:
                    return 'Debug';
                case LogLevel.WARNING:
                    return 'Warning';
                case LogLevel.CRITICAL:
                    return 'Critical';
                default:
                    return 'Unknown';
            }
        }
    }
}
</script>

<style scoped lang="scss">
    .custom-table {
        width: 100%;
    }

    .custom-table th, td {
        padding-left: 7px !important;
    }

    .custom-table-header {
        background: rgb(190, 190, 190);
    }

    .custom-table-header tr {
        height: 40px;
    }

    .custom-table-body {
        background: lightgray;
    }

    .custom-table-body tr {
        background: white;
        height: 40px;
    }

    .custom-table-body tr:nth-child(even) {
        background: rgb(240, 240, 240);
    }
</style>
