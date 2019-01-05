<template>
    <div>
        <h1>
            Chart statistics
        </h1>

        <vue-tabs>
            <v-tab v-for="elem in dataStructure" :key="elem.systemName" :title="elem.name">
                <div class="row" style="margin:0">
                    <div class="offset-xs-0 offset-sm-0 offset-md-2 offset-lg-3"></div>

                    <div class="col-xs-12 col-sm-12 col-md-8 col-lg-6">
                        <chart-statistics-component :robot-name="currentRobot" :field-name="elem.systemName"></chart-statistics-component>
                    </div>

                    <div class="offset-xs-0 offset-sm-0 offset-md-2 offset-lg-3"></div>
                </div>
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
            currentRobot: 'AMTS', // TODO get if from $store
            currentField: 'atmospheric_sensor',
            dataStructure: []
        }
    },
    async mounted() {
        this.dataStructure = await this.$store.state.requestService.getStatisticsDataStructure(this.currentRobot);
    }
}
</script>

<style lang="scss" scoped>
</style>
