<template>
    <div>
        <h1>
            Home page
        </h1>
        <div class="small">
            <line-chart :chart-data="datacollection" :options="options"></line-chart>
            <button @click="fillData()">Randomize</button>
        </div>
    </div>
</template>

<script>
import LineChart from './LineChart.js'

export default {
    components: {
        LineChart
    },
    data: function() {
        return {
            datacollection: null,
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        }
    },
    mounted: function () {
        this.fillData()
    },
    methods: {
        fillData () {
            this.datacollection = {
                labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                datasets: [
                    {
                        label: 'Data One',
                        backgroundColor: '#0a00a9',
                        borderColor: '#0a00a9',
                        data: Array.from({ length: 40 }, () => this.getRandomInt()),
                        fill: false,
                        lineTension: 0
                    },
                    {
                        label: 'Data Two',
                        backgroundColor: '#00f808',
                        borderColor: '#00f808',
                        data: Array.from({ length: 40 }, () => this.getRandomInt()),
                        fill: false,
                        lineTension: 0
                    },
                    {
                        label: 'Data Three',
                        backgroundColor: '#f80100',
                        borderColor: '#f80100',
                        data: Array.from({ length: 40 }, () => this.getRandomInt()),
                        fill: false,
                        lineTension: 0
                    }
                ]
            }
        },
        getRandomInt () {
            return Math.floor(Math.random() * 5)
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
