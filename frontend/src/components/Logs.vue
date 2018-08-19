import {LogLevel} from "../models/LogModel";
import {LogLevel} from "../models/LogModel";
import {LogLevel} from "../models/LogModel";
import {LogLevel} from "../models/LogModel";
<template>
    <div>
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

<script lang="ts">
    import {Component, Vue} from 'vue-property-decorator';
    import {LogLevel, LogModel} from '../models/LogModel';

    @Component
    export default class Logs extends Vue {
        private logs: LogModel[] = [];
        private elementsPerPage: number = 20;
        private _currentPage: number;
        private dbElementsCount: number;

        mounted() {
            this.currentPage = 1;
        }

        set currentPage(newPage: number) {
            this._currentPage = newPage;
            this.mockedLoadData(this._currentPage);
        }

        private mockedLoadData(page: number) {
            this.dbElementsCount = 300;
            let data: LogModel[] = [];
            for (let i = 0; i < this.dbElementsCount; ++i) {
                const t = i + 1;
                data.push(new LogModel(t, 0, `Title ${t}`, `Very very very long message without any information ${t}`));
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
        }
    }

    Vue.filter('logLevelToString', (level: LogLevel) => {
        switch (level) {
            case LogLevel.Info:
                return 'Info';
            case LogLevel.Debug:
                return 'Debug';
            case LogLevel.Warning:
                return 'Warning';
            case LogLevel.Critical:
                return 'Critical';
            default:
                return 'Unknown';
        }
    });
</script>

<style scoped lang="scss">
    .custom-table {
        width: 100%;
    }

    .custom-table th, td {
        padding-left: 7px !important;
    }

    .custom-table-header {
        background: #7395AE;
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
        background: #DBE5F0;
    }
</style>