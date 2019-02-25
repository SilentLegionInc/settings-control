<template>
    <div>
        <h1>
            Chart statistics
        </h1>

        <vue-tabs>
            <v-tab v-for="elem in dataStructure" :key="elem.systemName" :title="elem.name">
                <chart-statistics-component
                    :robot-name="robotName"
                    :db-name="databaseName"
                    :field-name="elem.systemName"
                ></chart-statistics-component>
            </v-tab>
        </vue-tabs>
    </div>
</template>

<script>
import ChartStatisticsComponent from '../components/ChartStatisticsComponent';
import { VueTabs, VTab } from 'vue-nav-tabs';
import 'vue-nav-tabs/themes/vue-tabs.css';

export default {
    name: 'ChartStatistics',
    components: { ChartStatisticsComponent, VueTabs, VTab },
    data: function() {
        return {
            currentField: 'atmospheric_sensor',
            dataStructure: [],
            robotName: null,
            databaseName: null
        }
    },
    async mounted() {
        this.robotName = this.$store.state.robotName;
        this.databaseName = this.$route.query.dbName;
        this.dataStructure = await this.$store.state.requestService.getStatisticsDataStructure(this.robotName, this.databaseName);
    }
}
</script>

<style lang="scss" scoped>
</style>
