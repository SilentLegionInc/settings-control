<template>
    <div class="small" align="center">
        <scatter-line-chart :chart-data="datacollection"></scatter-line-chart>
        <button class="btn btn-danger" @click="fillData()">Randomize</button>
    </div>
</template>

<script lang="ts">
import ScatterLineChart from '@/helpers/ScatterLineChart.ts';

export default {
    components: {
        ScatterLineChart,
    },
    data() {
        return {
            datacollection: {
                // labels: ['X', 'Y'],
                datasets: [
                    {
                        label: 'Data One',
                        showLine: true,
                        fill: false,
                        backgroundColor: 'aqua',
                        data: [
                            {x: new Date(2018, 7, this.getRandomInt()), y: this.getRandomInt()},
                            {x: new Date(2018, 7, this.getRandomInt()), y: this.getRandomInt()}
                        ],
                    }, {
                        label: 'Data Two',
                        showLine: true,
                        fill: false,
                        backgroundColor: 'red',
                        data: [
                            {x: new Date(2018, 7, this.getRandomInt()), y: this.getRandomInt()},
                            {x: new Date(2018, 7, this.getRandomInt()), y: this.getRandomInt()}
                        ],
                    },
                ],
            }
        };
    },
    mounted() {
        this.fillData();
    },
    methods: {
        fillData() {
            this.datacollection = {
                // labels: ['X', 'Y'],
                datasets: [
                    {
                        label: 'Data One',
                        showLine: true,
                        fill: false,
                        backgroundColor: 'aqua',
                        data: [
                            {x: new Date(2018, 7, this.getRandomInt()), y: this.getRandomInt()},
                            {x: new Date(2018, 7, this.getRandomInt()), y: this.getRandomInt()}
                        ],
                    }, {
                        label: 'Data Two',
                        showLine: true,
                        fill: false,
                        backgroundColor: 'red',
                        data: [
                            {x: new Date(2018, 7, this.getRandomInt()), y: this.getRandomInt()},
                            {x: new Date(2018, 7, this.getRandomInt()), y: this.getRandomInt()}
                            ],
                    },
                ],
            };
        },
        getRandomInt() {
            return Math.floor(Math.random() * (20 - 5 + 1)) + 5;
        },
    },
};
</script>

<style>
    .small {
        max-width: 600px;
        margin-left:  auto;
        margin-right: auto;
    }
</style>