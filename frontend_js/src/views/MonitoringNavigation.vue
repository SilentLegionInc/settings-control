<template>
    <div class="container-fluid">
        <h2 class="mb-3" align="center">Группы данных мониторинга</h2>
        <div class="row" style="margin: auto;" v-for="(elem, index) in databasesInfo" :key="elem.systemName">
            <div class="offset-md-1 offset-lg-2 offset-xl-3 col-12 col-sm-12 col-md-10 col-lg-8 col-xl-6">
                <b-card no-body>
                    <b-card-header header-tag="header" role="tab">
                        <b-button block href="#" v-b-toggle="elem.systemName" variant="info">{{elem.name}}</b-button>
                        <!--<button class="btn btn-info" :v-b-toggle="elem.systemName" style="width: 100%">{{elem.name}}</button>-->
                    </b-card-header>
                    <b-collapse :visible="index === 0" :id="elem.systemName" accordion="charts-accordion" role="tabpanel">
                        <b-card-body>
                            <div class="row mb-2">
                                <div class="col-12 col-sm-12 col-md-4 col-lg-4 col-xl-4">
                                    <button type="button" @click="toCharts(elem.systemName)" class="btn btn-primary btn-block mb-2">
                                        Графики
                                    </button>
                                </div>
                                <div class="col-12 col-sm-12 col-md-4 col-lg-4 col-xl-4">
                                    <button type="button" @click="toTables(elem.systemName)" class="btn btn-primary btn-block mb-2">
                                        Таблицы
                                    </button>
                                </div>
                                <div class="col-12 col-sm-12 col-md-4 col-lg-4 col-xl-4">
                                    <button type="button" @click="toMaps(elem.systemName)" class="btn btn-primary btn-block mb-2">
                                        Карты
                                    </button>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12">
                                    <div class="table-container">
                                        <table class="custom-table">
                                            <thead class="custom-table-header">
                                            <tr>
                                                <th>№</th>
                                                <th>Поле</th>
                                                <th>Тип</th>
                                            </tr>
                                            </thead>

                                            <tbody class="custom-table-body">
                                            <tr v-for="(fieldsElem, index) in elem.fields" :key="index">
                                                <td>{{index + 1}}</td>
                                                <td>{{fieldsElem.name}}</td>
                                                <td>{{fieldsElem.type | typeToHuman}}</td>
                                            </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </b-card-body>
                    </b-collapse>
                </b-card>
            </div>
        </div>
    </div>
</template>

<script>
import { catchErrorsWrapper } from '../helpers';

export default {
    name: 'MonitoringNavigation',
    data() {
        return {
            robotName: null,
            databasesInfo: []
        }
    },
    methods: {
        async loadDatabasesInfo() {
            this.loader = this.$loading.show();

            await catchErrorsWrapper(this.$toaster, async () => {
                this.robotName = this.$store.state.robotName;
                this.databasesInfo = await this.$store.state.requestService.getStatisticsDatabasesInfo(this.robotName);
            });

            this.loader.hide();
        },
        toCharts(dbName) {
            this.$router.push(`/chart_statistics?dbName=${dbName}`);
        },
        toTables(dbName) {
            this.$router.push(`/table_statistics?dbName=${dbName}`);
        },
        toMaps(dbName) {
            this.$router.push(`/maps_statistics?dbName=${dbName}`);
        }
    },
    mounted() {
        this.loadDatabasesInfo();
    },
    filters: {
        typeToHuman(value) {
            switch (value) {
                case 'number':
                    return 'Число';
                case 'string':
                    return 'Строка';
                default:
                    return 'Неизвестно';
            }
        }
    }
}
</script>

<style lang="scss" scoped>
    @import "../global_css/styles";

    @media only screen and (min-width: $min-wide-width) {
        .table-container {
            overflow-y: auto;
            max-height: 400px;
        }
    }
</style>
