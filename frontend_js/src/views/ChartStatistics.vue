<template>
    <div v-if="databaseName && robotName">
        <b-tabs lazy="true">
            <b-tab v-for="elem in dataStructure" :key="elem.systemName" :title="elem.name">
                <chart-statistics-component
                    :robot-name="robotName"
                    :db-name="databaseName"
                    :field-name="elem.systemName"
                ></chart-statistics-component>
            </b-tab>
        </b-tabs>
    </div>
</template>

<script>
import ChartStatisticsComponent from '../components/ChartStatisticsComponent';
import Logger from '../logger';

export default {
    name: 'ChartStatistics',
    components: { ChartStatisticsComponent },
    data: function() {
        return {
            currentField: 'atmospheric_sensor',
            dataStructure: [],
            robotName: null,
            databaseName: null
        }
    },
    async mounted() {
        const loader = this.$loading.show();

        this.robotName = this.$store.state.robotName;
        this.databaseName = this.$route.query.dbName;
        if (this.databaseName == null) {
            Logger.warn(`Chart statistics: can't load data, database name is empty`);
            return;
        }

        this.dataStructure = await this.$store.state.requestService.getStatisticsDataStructure(this.robotName, this.databaseName);
        this.dataStructure = this.dataStructure.filter(elem => elem.type === 'number');

        loader.hide();
    }
}
</script>

<style lang="scss" scoped>
    .custom-tab:active {
        box-shadow: 0 0 0 0 !important;
        background: #000000 !important;
    }
</style>
