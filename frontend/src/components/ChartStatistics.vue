<template>
    <h1>
        Chart statistics
        <line-chart :datasets="datasetss" :options="optionss"></line-chart>
    </h1>
</template>

<script lang="ts">
    import { Component, Vue, Prop } from 'vue-property-decorator';
    import {Line} from 'vue-chartjs';
    import LineChart from '../services/LineChart';
    @Component({
        components: {'line-chart': LineChart}
    })
    export default class ChartStatistics extends Line {
        @Prop() private datasetss = {
            labels: ['labelOne', 'labelTwo'],
            datasets: [
                {
                    label: 'Data One',
                    backgroundColor: '#f87979',
                    data: [0, 1]
                }, {
                    label: 'Data One',
                    backgroundColor: '#f87979',
                    data: [1, 2]
                }
            ]
        };

        @Prop() private optionss = {responsive: false, maintainAspectRatio: false}
    }
</script>

<style scoped lang="scss">
</style>