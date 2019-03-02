<template>
    <div v-if="databaseName && robotName">
        <form>
            <div class="col-xs-12 col-sm-11 col-md-9 col-lg-7">
                <div class="row margin-bottom-sm">
                    <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                        <span>Нач. время: </span>
                        <datetime v-model="filter.startTime" type="datetime" zone="utc" value-zone="utc" input-class="form-control"></datetime>
                    </div>
                    <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                        <span>Кон. время: </span>
                        <datetime v-model="filter.endTime" type="datetime" zone="utc" value-zone="utc" input-class="form-control"></datetime>
                    </div>
                </div>

                <div class="scrollable-filters">
                    <transition name="filter">
                        <div v-if="showAdditionalFilters" style="overflow: hidden;">
                            <div class="row margin-bottom-sm" v-for="(element, index) in numDataStructure" :key="index">
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                                    <span>Мин. {{element.name.toLowerCase()}}: </span>
                                    <input type="number" class="form-control" v-model="filter[`min_${element.systemName}`]">
                                </div>
                                <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                                    <span>Макс. {{element.name.toLowerCase()}}: </span>
                                    <input type="number" class="form-control" v-model="filter[`max_${element.systemName}`]">
                                </div>
                            </div>
                        </div>
                    </transition>
                </div>

                <div class="row">
                    <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                        <button type="button" class="btn btn-primary margin-right-sm" @click="loadData(1)">Применить</button>
                        <button type="button" class="btn btn-secondary margin-right-sm" @click="clearFilters()">Очистить</button>
                        <button type="button" class="btn btn-secondary margin-right-sm" @click="showAdditionalFilters = !showAdditionalFilters">Доп. фильтры</button>
                    </div>
                </div>
            </div>
        </form>

        <hr>

        <table class="custom-table">
            <thead class="custom-table-header">
            <tr>
                <th>№</th>
                <th>Время</th>
                <th>Широта</th>
                <th>Долгота</th>
                <th v-for="(element, index) in dataStructure" :key="index">{{element.name}}</th>
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

        <div class="pagination-flexbox-container padding-top-sm">
            <b-pagination class="paginator-flexbox-item padding-bottom-sm"
                          size="md"
                          :total-rows="dbElementsCount"
                          v-model="currentPage"
                          :per-page="elementsPerPage"
                          align="center">
            </b-pagination>

            <div class="per-page-flexbox-item per-page-flexbox-container padding-bottom-sm">
                <div class="margin-right-xs" style="white-space: nowrap;">
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
            showAdditionalFilters: false,
            robotName: null,
            databaseName: null
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

        changeElementsPerPage(event) {
            this.elementsPerPage = event.target.valueAsNumber;
            this.loadData(this.currentPage);
        },

        loadData: async function(page) {
            const offset = (page - 1) * this.elementsPerPage;
            const limit = this.elementsPerPage;
            const extended = this.dataStructure.length <= 0;
            const filter = JSON.parse(JSON.stringify(this.filter));
            for (let key in filter) {
                if (filter.hasOwnProperty(key)) {
                    if (key === 'startTime' || key === 'endTime') {
                        filter[key] = filter[key] ? new Date(filter[key]) : null;
                    } else if (key.startsWith('min_') || key.startsWith('max_')) {
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

    .filter-enter, .filter-leave-to {
        max-height: 0;
    }

    .filter-enter-to, .filter-leave {
        max-height: 300px;
    }

    .filter-leave-active, .filter-enter-active {
        transition: max-height 0.5s;
    }

    .scrollable-filters {
        height: auto;
        max-height: 300px;
        overflow-y: auto;
    }
</style>
