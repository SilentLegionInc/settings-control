<template>
    <div>
        <form>
            <div class="col-xs-12 col-sm-12 col-md-12 col-lg-10 filter-flexbox-container padding-left-sm padding-right-sm">
                <span class="filter-flexbox-item margin-left-xs margin-right-xs">
                    <span>Нач. время: </span>
                    <datetime type="datetime" zone="utc" value-zone="utc" input-class="form-control"></datetime>
                </span>

                <span class="filter-flexbox-item margin-left-xs margin-right-xs">
                    <span>Кон. время: </span>
                    <datetime type="datetime" zone="utc" value-zone="utc" input-class="form-control"></datetime>
                </span>

                <span class="filter-flexbox-item margin-left-xs margin-right-xs">
                    <div>&nbsp;</div>
                    <button type="button" class="btn btn-primary margin-right-xs" @click="loadData(1)">Применить</button>
                    <button type="button" class="btn btn-secondary margin-left-xs" @click="clearFilters()">Очистить</button>
                </span>
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
            console.log(`Cleared filters`);
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
            filter.startTime = filter.startTime ? new Date(filter.startTime) : null;
            filter.endTime = filter.endTime ? new Date(filter.endTime) : null;

            const response = await this.$store.state.requestService.getStatisticsTableData(
                this.robotName, this.databaseName, limit, offset, extended, filter, this.sort
            );
            this.dbElementsCount = response.count;
            this.dataElements = response.result;
            if (extended) {
                this.dataStructure = response.dataStructure;
            }
        },

        selectElement(index) {
            console.log(`Selected ${index} element`);
        }
    },
    mounted() {
        this.databaseName = this.$route.query.dbName;

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
</style>
