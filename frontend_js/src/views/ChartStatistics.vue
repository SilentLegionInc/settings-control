<template>
    <div>
        <h1>
            Chart statistics
        </h1>

        <chart-statistics-component :robot-name="currentRobot" :field-name="currentField"></chart-statistics-component>
    </div>
</template>

<script>
import ChartStatisticsComponent from '../components/ChartStatisticsComponent'

export default {
    name: 'ChartStatistics',
    components: {
        ChartStatisticsComponent
    },
    data: function() {
        return {
            currentRobot: 'AMTS',
            currentField: 'atmospheric_sensor'
        }
    }
}
</script>

<style scoped>

</style>
