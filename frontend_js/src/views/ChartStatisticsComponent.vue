<template>
    <div>
        <line-chart v-if="chartData" :chart-data="chartData" :options="chartOptions"></line-chart>
    </div>
</template>

<script>
import LineChart from './LineChart.js';
import Logger from '../logger';

export default {
    name: 'ChartStatisticsComponent',
    components: {
        LineChart
    },
    props: ['robotName', 'fieldName'],
    data: function() {
        return {
            chartData: [],
            chartOptions: chartOptions,
            tableData: [],
            elementsPerPage: 20,
            _currentPage: 1,
            dbElementsCount: 0,
            filterStartTime: null,
            filterEndTime: null
        }
    },
    methods: {
        mockedLoadData() {
            const data = [];
            for (let i = 10; i < 60; i++) {
                data.push({ x: new Date(`2008-09-10T15:53:${i}`), y: Math.floor(Math.random() * 500) })
            }

            this.chartData = {
                datasets: [
                    {
                        label: 'Data One',
                        backgroundColor: '#0a00a9',
                        borderColor: '#0a00a9',
                        data: data,
                        fill: false,
                        lineTension: 0,
                        borderCapStyle: 'round',
                        borderJoinStyle: 'round'
                    }
                ]
            }
        },
        async loadData(page) {
            if (this.robotName == null || this.fieldName == null) {
                const wrongField = this.robotName == null ? 'robot name' : 'field name';
                Logger.warn(`Chart statistics: can't load data, ${wrongField} is empty`);
                return;
            }

            const offset = (page - 1) * this.elementsPerPage;
            const limit = this.elementsPerPage;
            const filterStartTime = this.filterStartTime ? new Date(this.filterStartTime) : null;
            const filterEndTime = this.filterEndTime ? new Date(this.filterEndTime) : null;

            const response = await this.$store.state.requestService.getChartData(this.robotName, this.fieldName, limit, offset, filterStartTime, filterEndTime);
            this.dbElementsCount = response.count;
            this.data = response.result;
        }
    },
    computed: {
        currentPage: {
            get() {
                return this._currentPage;
            },
            set(newPage) {
                this._currentPage = newPage;
                this.loadData(this._currentPage);
            }
        },
        data: {
            get() {
                return this.tableData;
            },
            set(newData) {
                this.tableData = newData;

                const dataset = JSON.parse(JSON.stringify(datasetOptions));
                dataset.data = newData.map(elem => {
                    return {
                        x: elem.time,
                        y: elem.value,
                        latitude: elem.latitude,
                        longitude: elem.longitude
                    }
                });
                this.chartData = { datasets: [dataset] };
            }
        }
    },
    mounted() {
        this.currentPage = 1;
    }
}

const chartOptions = {
    scales: {
        xAxes: [{
            type: 'time',
            ticks: {
                autoSkip: true
            },
            distribution: 'linear',
            time: {
                unit: 'second'
            }
        }]
    }
};

const datasetOptions = {
    label: 'Data One',
    backgroundColor: '#0a00a9',
    borderColor: '#0a00a9',
    fill: false,
    lineTension: 0,
    borderCapStyle: 'round',
    borderJoinStyle: 'round'
};
</script>

<style>
</style>
