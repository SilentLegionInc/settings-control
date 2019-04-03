<template>
    <div v-if="databaseName && robotName">
        <b-tabs v-if="$isWideScreen()" :lazy="true">
            <b-tab v-for="elem in dataStructure" :key="elem.systemName" :title="elem.name">
                <chart-statistics-component
                    :robot-name="robotName"
                    :db-name="databaseName"
                    :field-name="elem.systemName"
                ></chart-statistics-component>
            </b-tab>
        </b-tabs>

        <div v-else class="container-fluid pl-0 pr-0">
            <div class="row" style="margin: auto;" v-for="elem in dataStructure" :key="elem.systemName">
                <div class="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12 p-0">
                    <b-card no-body class="mb-1">
                        <b-card-header header-tag="header" class="p-1" role="tab">
                            <button class="btn btn-info" style="width: 100%" @click="selectMobileTab(elem.systemName)">{{elem.name}}</button>
                        </b-card-header>
                        <b-collapse :id="elem.systemName" :visible="isMobileTabVisible(elem.systemName)" accordion="charts-accordion" role="tabpanel">
                            <b-card-body class="p-0">
                                <chart-statistics-component
                                    v-if="isMobileTabVisible(elem.systemName)"
                                    :robot-name="robotName"
                                    :db-name="databaseName"
                                    :field-name="elem.systemName"
                                ></chart-statistics-component>
                            </b-card-body>
                        </b-collapse>
                    </b-card>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import ChartStatisticsComponent from '../components/ChartStatisticsComponent';
import Logger from '../logger';
import { catchErrorsWrapper } from '../helpers';

export default {
    name: 'ChartStatistics',
    components: { ChartStatisticsComponent },
    data() {
        return {
            dataStructure: [],
            robotName: null,
            databaseName: null,
            activeTab: null
        }
    },
    methods: {
        selectMobileTab(tabName) {
            if (this.activeTab === tabName) {
                this.activeTab = null;
            } else {
                this.activeTab = tabName;
            }
        },
        isMobileTabVisible(tabName) {
            return this.activeTab === tabName;
        },
        async loadAvailableFields() {
            this.loader = this.$loading.show();

            await catchErrorsWrapper(this.$toaster, async () => {
                this.robotName = this.$store.state.robotName;
                this.databaseName = this.$route.query.dbName;
                if (this.databaseName == null) {
                    Logger.warn(`Chart statistics: can't load data, database name is empty`);
                    return;
                }

                this.dataStructure = await this.$store.state.requestService.getStatisticsDataStructure(this.robotName, this.databaseName);
                this.dataStructure = this.dataStructure.filter(elem => elem.type === 'number');
            });

            this.loader.hide();
        }
    },
    mounted() {
        this.loadAvailableFields();
    }
}
</script>

<style lang="scss" scoped>
    .tab-pane {
        outline: none !important;
    }
</style>
