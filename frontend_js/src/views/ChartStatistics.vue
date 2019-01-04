<template>
    <div>
        <h1>
            Home page
        </h1>
        <div class="small">
            <line-chart :chart-data="chartData" :options="options"></line-chart>
            <button @click="fillData()">Randomize</button>
        </div>
    </div>
</template>

<script>
import LineChart from './LineChart.js'

export default {
    name: 'ChartStatistics',
    components: {
        LineChart
    },
    props: ['robotName'],
    data: function() {
        return {
            chartData: null,
            options: {
            }
        }
    },
    mounted: function () {
        this.fillData()
    },
    methods: {
        fillData () {
            this.chartData = {
                datasets: [
                    {
                        label: 'Data One',
                        backgroundColor: '#0a00a9',
                        borderColor: '#0a00a9',
                        data: [{ x: 3, y: 15 }, { x: 5, y: 17 }, { x: 9, y: 30 }, { x: 13, y: 36 }],
                        fill: false,
                        lineTension: 0
                    }
                ]
            }
        },
        getRandomInt () {
            return Math.floor(Math.random() * 80)
        }
    }
}
</script>

<style>
    .small {
        max-width: 600px;
        margin:  150px auto;
    }
</style>
