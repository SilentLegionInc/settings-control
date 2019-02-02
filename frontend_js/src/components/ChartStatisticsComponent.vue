<template>
    <div>
        <form>
            <div class="row filter-flexbox-container">
                <span class="margin-left-xs margin-right-xs">
                    <span>Start time: </span>
                    <datetime v-model="filterStartTime" type="datetime" zone="utc" value-zone="utc" input-class="form-control"></datetime>
                </span>

                <span class="margin-left-xs margin-right-xs">
                    <span>End time: </span>
                    <datetime v-model="filterEndTime" type="datetime" zone="utc" value-zone="utc" input-class="form-control"></datetime>
                </span>

                <span class="margin-left-xs margin-right-xs">
                    <div>&nbsp;</div>
                    <button type="button" class="btn btn-primary margin-right-xs" @click="loadData(1)">Apply</button>
                    <button type="button" class="btn btn-secondary margin-left-xs" @click="clearFilters()">Clear</button>
                </span>
            </div>
        </form>

        <hr>

        <line-chart v-if="chartData" :chart-data="chartData" :options="chartOptions"></line-chart>

        <hr>

        <table class="custom-table">
            <thead class="custom-table-header">
            <tr>
                <th>№</th>
                <th>Time</th>
                <th>Value</th>
                <th>Latitude</th>
                <th>Longitude</th>
            </tr>
            </thead>

            <tbody class="custom-table-body">
            <tr v-for="(dataElem, index) in data" :key="index">
                <td>{{ (_currentPage - 1) * elementsPerPage + index + 1 }}</td>
                <td>{{ dataElem.time | moment("DD.MM.YYYY HH:mm:ss.SSS") }}</td>
                <td>{{ dataElem.value }}</td>
                <td>{{ dataElem.latitude }}</td>
                <td>{{ dataElem.longitude }}</td>
            </tr>
            </tbody>
        </table>

        <div class="pagination-flexbox-container padding-top-sm">
            <b-pagination class="paginator-flexbox-item padding-bottom-sm"
                          size="md"
                          :total-rows="dbElementsCount"
                          v-model="currentPage"
                          :per-page="elementsPerPage"
                          align="center">
            </b-pagination>

            <div class="per-page-flexbox-item per-page-flexbox-container padding-bottom-sm">
                <div class="margin-right-xs" style="white-space: nowrap;">
                    Per page:
                </div>

                <div>
                    <input :value="elementsPerPage" @change="changeElementsPerPage" type="number" class="form-control" style="max-width: 80px">
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import LineChart from '../views/LineChart.js';
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
            chartOptions: getChartOptions(this.$moment),
            tableData: [],
            elementsPerPage: 20,
            _currentPage: 1,
            dbElementsCount: 0,
            filterStartTime: null,
            filterEndTime: null,
            minimumValue: null,
            averageValue: null,
            maximumValue: null,
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

        clearFilters() {
            this.filterStartTime = null;
            this.filterEndTime = null;
        },

        changeElementsPerPage(event) {
            this.elementsPerPage = event.target.valueAsNumber;
            this.loadData(this.currentPage);
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

            const response = await this.$store.state.requestService.getStatisticsData(this.robotName, this.fieldName, limit, offset, filterStartTime, filterEndTime);
            this.dbElementsCount = response.count;
            this.minimumValue = response.minimum;
            this.averageValue = response.average;
            this.maximumValue = response.maximum;
            // TODO add these values to chart
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

function getChartOptions(moment) {
    return {
        scales: {
            xAxes: [{
                type: 'time',
                ticks: {
                    autoSkip: true
                },
                distribution: 'linear',
                time: {
                    unit: 'second',
                    round: 'millisecond',
                    displayFormats: {
                        second: 'DD.MM.YY HH:mm:ss'
                    }
                }
            }],
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Value',
                    fontSize: 14
                }
            }]
        },

        hover: {
            mode: 'nearest',
            intersect: true
        },

        legend: {
            display: true,
            position: 'bottom',
            fullWidth: true,
            reverse: false
        },

        tooltips: {
            callbacks: {
                label: (tooltipItem, data) => {
                    const time = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].x;
                    const latitude = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].latitude;
                    const longitude = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].longitude;

                    const text = [];
                    text.push(`Время: ${moment(time).format('DD.MM.YYYY HH:mm:ss.SSS')}`);
                    text.push(`Широта: ${latitude}`);
                    text.push(`Долгота: ${longitude}`);

                    return text;
                },

                title: (tooltipItem, data) => {
                    return `Значение: ${tooltipItem[0].yLabel}`;
                }
            }
        },

        pan: {
            // Boolean to enable panning
            enabled: true,

            // Panning directions. Remove the appropriate direction to disable
            // Eg. 'y' would only allow panning in the y direction
            mode: 'x'
        },

        // Container for zoom options
        zoom: {
            // Boolean to enable zooming
            enabled: true,

            // Zooming directions. Remove the appropriate direction to disable
            // Eg. 'y' would only allow zooming in the y direction
            mode: 'x'
        }
    }
}

const datasetOptions = {
    label: 'Data One',
    backgroundColor: '#0a00a9',
    borderColor: '#0a00a9',
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

<style lang="scss">
    .filter-flexbox-container {
        display: flex;
        flex-direction: row;
        justify-content: left;
        align-items: flex-end;
        flex-wrap: wrap;
    }

    .per-page-flexbox-container {
        display: flex;
        flex-direction: row;
        justify-content: flex-end;
        align-items: center;
    }

    .pagination-flexbox-container {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
    }

    .paginator-flexbox-item {
        margin: 0;
        justify-self: center;
        flex-grow: 3;
    }

    .per-page-flexbox-item {
        justify-self: flex-end;
        flex-grow: 1;
    }
</style>
