<template>
    <div>
        <form>
            <div class="col-12 col-sm-12 col-md-12 col-lg-10 col-lg-8 filter-flexbox-container pl-2 pr-2">
                <span class="filter-flexbox-item ml-1 mr-1">
                    <span>Нач. время: </span>
                    <datetime v-model="filterStartTime" type="datetime" zone="utc" value-zone="utc" input-class="form-control"></datetime>
                </span>

                <span class="filter-flexbox-item ml-1 mr-1">
                    <span>Кон. время: </span>
                    <datetime v-model="filterEndTime" type="datetime" zone="utc" value-zone="utc" input-class="form-control"></datetime>
                </span>

                <span class="filter-flexbox-item ml-1 mr-1">
                    <span>Тип: </span>
                    <select class="form-control" v-model="filterType">
                        <option value=0>Critical</option>
                        <option value=1>Warning</option>
                        <option value=2>Debug</option>
                        <option value=3>Info</option>
                    </select>
                </span>

                <span class="filter-flexbox-item ml-1 mr-1">
                    <div>&nbsp;</div>
                    <button type="button" class="btn btn-primary mr-1" @click="loadData(1)">Применить</button>
                    <button type="button" class="btn btn-secondary ml-1" @click="clearFilters()">Очистить</button>
                </span>
            </div>
        </form>

        <hr>

        <table class="custom-table">
            <thead class="custom-table-header">
                <tr>
                    <th>№</th>
                    <th>Время</th>
                    <th>Тип</th>
                    <th>Заголовок</th>
                    <th>Сообщение</th>
                </tr>
            </thead>

            <tbody class="custom-table-body">
                <tr v-for="(log, index) in logs" :key="index" @click="selectLog(index)" class="selectable-table-row">
                    <td>{{ (_currentPage - 1) * elementsPerPage + index + 1 }}</td>
                    <td>{{ log.time | moment("DD.MM.YYYY HH:mm:ss.SSS") }}</td>
                    <td>{{ log.type | logLevelToString }}</td>
                    <td>{{ log.title }}</td>
                    <td>{{ log.message | chopLongMessage}}</td>
                </tr>
            </tbody>
        </table>

        <div class="pagination-flexbox-container pt-2">
            <b-pagination class="paginator-flexbox-item pb-2"
                          size="md"
                          :total-rows="dbElementsCount"
                          v-model="currentPage"
                          :per-page="elementsPerPage"
                          align="center">
            </b-pagination>

            <div class="per-page-flexbox-item per-page-flexbox-container pb-2">
                <div class="mr-1" style="white-space: nowrap;">
                    На странице:
                </div>

                <div>
                    <input :value="elementsPerPage" @change="changeElementsPerPage" type="number" class="form-control" style="max-width: 80px">
                </div>
            </div>
        </div>

        <logs-modal ref="logsModal"></logs-modal>
    </div>
</template>

<script>
import { LogModel } from '../models/LogModel';
import LogsModal from '../components/LogsModal';

export default {
    name: 'Logs',
    components: {
        'logs-modal': LogsModal
    },
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
    methods: {
        mockedLoadData: function(page) {
            this.dbElementsCount = 300;
            let data = [];
            for (let i = 0; i < this.dbElementsCount; ++i) {
                const t = i + 1;
                data.push(new LogModel(i, t, new Date(), 0, `Title ${t}`, `Very very very long message without any information ${t}`));
            }

            const offset = (page - 1) * this.elementsPerPage;
            const limit = this.elementsPerPage;
            if (offset > 0) {
                data.splice(0, (page - 1) * this.elementsPerPage);
            }
            this.logs = data.slice(0, limit);
        },

        clearFilters() {
            this.filterStartTime = null;
            this.filterEndTime = null;
            this.filterType = null;
        },

        changeElementsPerPage(event) {
            this.elementsPerPage = event.target.valueAsNumber;
            this.loadData(this.currentPage);
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
        },

        selectLog(index) {
            this.$refs.logsModal.showModal(this.logs[index]);
        }
    },
    mounted() {
        this.currentPage = 1;
    },
    filters: {
        chopLongMessage: function(str) {
            if (str.length > 50) {
                return str.slice(0, 50) + '...';
            } else {
                return str;
            }
        }
    }
}
</script>

<style scoped lang="scss">
    .filter-flexbox-container {
        display: flex;
        flex-direction: row;
        justify-content: left;
        align-items: flex-end;
        flex-wrap: wrap;
    }

    .filter-flexbox-item {
        flex-grow: 1;
    }

    .per-page-flexbox-container {
        display: flex;
        flex-direction: row;
        justify-content: flex-end;
        align-items: center;
    }

    .pagination-flexbox-container {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
    }

    .paginator-flexbox-item {
        margin: 0;
        justify-self: center;
        flex-grow: 3;
    }

    .per-page-flexbox-item {
        justify-self: flex-end;
        flex-grow: 1;
    }
</style>
