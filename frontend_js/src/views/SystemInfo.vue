<template>
    <div>
        <div style="max-width: 700px; margin-left: auto; margin-right: auto">
            <line-chart v-if="chartData" :chart-data="chartData" :options="chartOptions"></line-chart>
        </div>
        <div>
            <capacity-component :percent-value="72.1" :free-value="70947196928" :max-value="254721126400"></capacity-component>
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
            diskInfo: null,
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
                labels: []
            };
            for (const key of cpuInfoKeys) {
                if (response.cpuInfo.hasOwnProperty(key)) {
                    const color = this.getRandomColor();
                    this.chartData.datasets.push({
                        label: key,
                        backgroundColor: color,
                        border: color,
                        data: [response.cpuInfo[key]],
                        fill: false,
                        lineTension: 0
                    });
                    this.chartData.labels = Array(this.elementsPerChart).fill('');
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
                labels: []
            };

            let index = 0;
            for (const key of cpuInfoKeys) {
                if (response.hasOwnProperty(key)) {
                    const color = oldDatasets[index].backgroundColor;
                    this.chartData.datasets.push({
                        label: key,
                        backgroundColor: color,
                        borderColor: color,
                        data: [...oldDatasets[index++].data.slice(-(this.elementsPerChart - 1)), response[key]],
                        fill: false,
                        lineTension: 0
                    });
                }
            }
            this.chartData.labels = Array(this.elementsPerChart).fill('');
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
            scaleLabel: {
                display: true,
                labelString: 'Нагрузка',
                fontSize: 14
            },
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
</script>

<style scoped>

</style>
