<template>
    <div class="container-fluid">
        <div class="row" style="margin: auto">
            <div class="col-12 col-sm-12 col-md-6 col-lg-6 col-xl-6 mb-2">
                <h4 align="center">Нагрузка процессора</h4>
                <div style="max-width: 600px; margin-left: auto; margin-right: auto">
                    <line-chart v-if="chartData" :chart-data="chartData" :options="chartOptions"></line-chart>
                </div>
            </div>
            <div class="col-12 col-sm-12 col-md-6 col-lg-6 col-xl-6">
                <h4 align="center">Точки монтирования</h4>
                <div class="row">
                    <div class="col-12 col-sm-12 col-md-12 col-lg-6 col-xl-6 pb-3">
                        <b-card v-if="memoryInfo">
                            <div class="row">
                                <div class="col-2 col-sm-2 col-md-3 col-lg-3 col-xl-3">
                                    <img src="@/assets/ram.svg" width="100%" height="100%" alt="ram image">
                                </div>
                                <div class="col-10 col-sm-10 col-md-9 col-lg-9 col-xl-9 flexbox">
                                    <div>
                                        <h5 class="custom-card-header">RAM</h5>
                                    </div>
                                    <div>
                                        <capacity-component
                                            :percent-value="memoryInfo.ramInfo.percent"
                                            :free-value="memoryInfo.ramInfo.free"
                                            :max-value="memoryInfo.ramInfo.total"
                                        ></capacity-component>
                                    </div>
                                </div>
                            </div>
                        </b-card>
                    </div>
                    <div class="col-12 col-sm-12 col-md-12 col-lg-6 col-xl-6 pb-3">
                        <b-card v-if="memoryInfo">
                            <div class="row">
                                <div class="col-2 col-sm-2 col-md-3 col-lg-3 col-xl-3">
                                    <img src="@/assets/swap.svg" width="100%" height="100%" alt="swap image">
                                </div>
                                <div class="col-10 col-sm-10 col-md-9 col-lg-9 col-xl-9 flexbox">
                                    <div>
                                        <h5 class="custom-card-header">Swap</h5>
                                    </div>
                                    <div>
                                        <capacity-component
                                            :percent-value="memoryInfo.swapInfo.percent"
                                            :free-value="memoryInfo.swapInfo.free"
                                            :max-value="memoryInfo.swapInfo.total"
                                        ></capacity-component>
                                    </div>
                                </div>
                            </div>
                        </b-card>
                    </div>
                    <div v-for="(disk, index) of diskInfo" v-bind:key="index" class="col-12 col-sm-12 col-md-12 col-lg-6 col-xl-6 pb-3 pt-3">
                        <b-card>
                            <div class="row">
                                <div class="col-2 col-sm-2 col-md-3 col-lg-3 col-xl-3">
                                    <img src="@/assets/disk.svg" width="100%" height="100%" alt="disk image">
                                </div>
                                <div class="col-10 col-sm-10 col-md-9 col-lg-9 col-xl-9 flexbox">
                                    <div>
                                        <h5 class="custom-card-header">{{disk.name}}</h5>
                                    </div>
                                    <div>
                                        <capacity-component
                                            :percent-value="disk.info.percent"
                                            :free-value="disk.info.free"
                                            :max-value="disk.info.total"
                                        ></capacity-component>
                                    </div>
                                </div>
                            </div>
                        </b-card>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import CapacityComponent from '../components/CapacityComponent';
import LineChart from './LineChart';
import Logger from '../logger';

export default {
    name: 'SystemInfo',
    components: { CapacityComponent, LineChart },
    data: function() {
        return {
            diskInfo: [],
            memoryInfo: null,
            chartData: null,
            chartOptions: options,
            elementsPerChart: 30
        }
    },
    methods: {
        async loadFullInfo() {
            const response = await this.$store.state.requestService.getSystemInfo();
            this.diskInfo = response.diskInfo;
            this.memoryInfo = response.memoryInfo;

            const cpuInfoKeys = Object.keys(response.cpuInfo);
            cpuInfoKeys.sort();
            this.chartData = {
                datasets: [],
                labels: Array(this.elementsPerChart).fill('')
            };
            for (const key of cpuInfoKeys) {
                if (response.cpuInfo.hasOwnProperty(key)) {
                    const color = this.getRandomColor();
                    const dataset = JSON.parse(JSON.stringify(datasetOptions));
                    dataset.label = key;
                    dataset.backgroundColor = color;
                    dataset.borderColor = color;
                    dataset.data = [...Array(this.elementsPerChart - 1).fill(null), response.cpuInfo[key]];

                    this.chartData.datasets.push(dataset);
                }
            }
        },
        async loadCpuInfo() {
            const response = await this.$store.state.requestService.getSystemInfo(false);
            const cpuInfoKeys = Object.keys(response);
            if (this.chartData.datasets.length !== cpuInfoKeys.length) {
                Logger.error('CPU\'s count didn\'t match');
                return;
            }
            cpuInfoKeys.sort();

            const oldDatasets = this.chartData.datasets.slice();

            this.chartData = {
                datasets: [],
                labels: this.chartData.labels
            };

            let index = 0;
            for (const key of cpuInfoKeys) {
                if (response.hasOwnProperty(key)) {
                    const color = oldDatasets[index].backgroundColor;
                    const dataset = JSON.parse(JSON.stringify(datasetOptions));
                    dataset.label = key;
                    dataset.backgroundColor = color;
                    dataset.borderColor = color;
                    dataset.data = [...oldDatasets[index++].data.slice(-(this.elementsPerChart - 1)), response[key]];

                    this.chartData.datasets.push(dataset);
                }
            }
        },
        getRandomColor() {
            return '#' + (0x1000000 + (Math.random()) * 0xffffff).toString(16).substr(1, 6);
        }
    },
    mounted: async function() {
        await this.loadFullInfo();
        setInterval(this.loadCpuInfo, 1000);
    }
}

const options = {
    animation: false,
    scales: {
        yAxes: [{
            ticks: {
                max: 100,
                min: 0,
                stepSize: 10
            }
        }]
    },

    hover: {
        mode: 'nearest',
        intersect: true
    },

    legend: {
        position: 'bottom',
        fullWidth: true,
        reverse: false
    }
};

const datasetOptions = {
    borderWidth: 3,
    fill: false,
    lineTension: 0,
    borderCapStyle: 'round',
    borderJoinStyle: 'round',
    pointRadius: 3,
    pointHoverRadius: 4,
    pointHitRadius: 10,
    pointBorderWidth: 2
};
</script>

<style scoped lang="scss">
    .flexbox {
        display: flex;
        justify-content: center;
        align-items: stretch;
        flex-flow: column;
    }

    .custom-card-header {
        margin-bottom: 0 !important;
    }
</style>
