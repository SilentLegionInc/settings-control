<template>
    <div v-if="databaseName && robotName">
        <div class="col-12 col-sm-12 col-md-9 col-lg-7 col-xl-6">
            <div class="row" style="margin:auto">
                <div class="col-12 col-sm-6 col-md-6 col-lg-6 col-xl-6 pl-1 pr-1">
                    <span>Нач. время: </span>
                    <datetime v-model="filter.startTime" type="datetime" zone="utc" value-zone="utc" input-class="form-control"></datetime>
                </div>
                <div class="col-12 col-sm-6 col-md-6 col-lg-6 col-xl-6 pl-1 pr-1">
                    <span>Кон. время: </span>
                    <datetime v-model="filter.endTime" type="datetime" zone="utc" value-zone="utc" input-class="form-control"></datetime>
                </div>
            </div>

            <div class="scrollable-filters mb-3">
                <b-collapse id="filters-collapse">
                    <div class="row" style="margin:auto" v-for="(element, index) in numDataStructure" :key="index">
                        <div class="col-12 col-sm-6 col-md-6 col-lg-6 col-xl-6 pl-1 pr-1">
                            <span>Мин. {{element.name.toLowerCase()}}: </span>
                            <input type="number" class="form-control" v-model="filter[`min__${element.systemName}`]">
                        </div>
                        <div class="col-12 col-sm-6 col-md-6 col-lg-6 col-xl-6 pl-1 pr-1">
                            <span>Макс. {{element.name.toLowerCase()}}: </span>
                            <input type="number" class="form-control" v-model="filter[`max__${element.systemName}`]">
                        </div>
                    </div>
                </b-collapse>
            </div>

            <div class="row" style="margin:auto">
                <div class="col-12 col-sm-12 col-md-4 col-lg-3 col-xl-3 pb-1 pl-1 pr-1">
                    <button type="button" class="btn btn-primary btn-block" @click="loadData(1)">Применить</button>
                </div>
                <div class="col-12 col-sm-12 col-md-4 col-lg-3 col-xl-3 pb-1 pl-1 pr-1">
                    <button type="button" class="btn btn-secondary btn-block" @click="clearFilters()">Очистить</button>
                </div>
                <div class="col-12 col-sm-12 col-md-4 col-lg-3 col-xl-3 pl-1 pr-1">
                    <button type="button" class="btn btn-secondary btn-block" v-b-toggle.filters-collapse>Доп. фильтры</button>
                </div>
            </div>
        </div>

        <hr>

        <div style="overflow-x: auto;">
            <table class="custom-table">
                <thead class="custom-table-header">
                <tr>
                    <th>№</th>
                    <th @click="changeSort('time')" class="clickable-header-elem">
                        <span v-if="sort.time">
                            <i v-if="sort.time === 1" key="1" class="fa fa-chevron-down" aria-hidden="true"></i>
                            <i v-else key="2" class="fa fa-chevron-up" aria-hidden="true"></i>
                        </span>
                        Время
                    </th>
                    <th>
                        Широта
                    </th>
                    <th>
                        Долгота
                    </th>
                    <th v-for="(element, index) in dataStructure" :key="index" @click="changeSort(element.systemName)" class="clickable-header-elem">
                        <span v-if="sort[element.systemName]">
                            <i v-if="sort[element.systemName] === 1" key="1" class="fa fa-chevron-down" aria-hidden="true"></i>
                            <i v-else key="2" class="fa fa-chevron-up" aria-hidden="true"></i>
                        </span>
                        {{element.name}}
                    </th>
                </tr>
                </thead>

                <tbody class="custom-table-body">
                <tr v-for="(dataElement, dataElementIndex) in dataElements" :key="dataElementIndex" @click="selectElement(dataElementIndex)" class="selectable-table-row">
                    <td>{{ (_currentPage - 1) * elementsPerPage + dataElementIndex + 1 }}</td>
                    <td>{{ dataElement.time | moment("DD.MM.YYYY HH:mm:ss.SSS") }}</td>
                    <td>{{ dataElement.latitude }}</td>
                    <td>{{ dataElement.longitude }}</td>
                    <td v-for="(structElement, structElementIndex) in dataStructure" :key="structElementIndex">{{ dataElement.data[structElement.systemName] }}</td>
                </tr>
                </tbody>
            </table>
        </div>

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
    </div>
</template>

<script>
import Logger from '../logger';
export default {
    name: 'TableStatistics',
    data: function() {
        return {
            dataElements: [],
            elementsPerPage: 20,
            _currentPage: 1,
            dbElementsCount: 0,
            dataStructure: [],
            filter: {},
            sort: {},
            robotName: null,
            databaseName: null,
            numDataStructure: null
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
        clearFilters() {
            for (let key in this.filter) {
                if (this.filter.hasOwnProperty(key)) {
                    this.filter[key] = null;
                }
            }
        },

        changeSort(systemFieldName) {
            const oldValue = this.sort[systemFieldName];
            this.sort = {};
            this.sort[systemFieldName] = oldValue ? -oldValue : 1;
            this.loadData(this.currentPage);
        },

        changeElementsPerPage(event) {
            this.elementsPerPage = event.target.valueAsNumber;
            this.loadData(this.currentPage);
        },

        loadData: async function(page) {
            const loader = this.$loading.show();

            const offset = (page - 1) * this.elementsPerPage;
            const limit = this.elementsPerPage;
            const extended = this.dataStructure.length <= 0;
            const filter = JSON.parse(JSON.stringify(this.filter));
            for (let key in filter) {
                if (filter.hasOwnProperty(key)) {
                    if (key === 'startTime' || key === 'endTime') {
                        filter[key] = filter[key] ? new Date(filter[key]) : null;
                    } else if (key.startsWith('min__') || key.startsWith('max__')) {
                        filter[key] = filter[key] ? parseFloat(filter[key]) : null;
                    }
                }
            }

            const response = await this.$store.state.requestService.getStatisticsTableData(
                this.robotName, this.databaseName, limit, offset, extended, filter, this.sort
            );
            this.dbElementsCount = response.count;
            this.dataElements = response.result;
            if (extended) {
                this.dataStructure = response.dataStructure;
                this.numDataStructure = this.dataStructure.filter(elem => elem.type === 'number');
            }

            loader.hide();
        },

        selectElement(index) {
            console.log(`Selected ${index} element`);
        }
    },
    mounted() {
        this.databaseName = this.$route.query.dbName;
        if (this.databaseName == null) {
            Logger.warn(`Chart statistics: can't load data, database name is empty`);
            return;
        }

        if (this.$route.query.latitude && this.$route.query.longitude) {
            this.filter.latitude = this.$route.query.latitude;
            this.filter.longitude = this.$route.query.longitude;
        }

        this.robotName = this.$store.state.robotName;
        this.currentPage = 1;
    }
}
</script>

<style scoped lang="scss">
    @import "../global_css/styles";

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

    @media only screen and (min-width: $max-narrow-width) {
        .scrollable-filters {
            height: auto;
            max-height: 300px;
            overflow-y: auto;
            overflow-x: hidden;
        }
    }

    th.clickable-header-elem {
        cursor: pointer;
    }

    th.clickable-header-elem:hover {
        color: #DAB6C8;
    }
</style>
