<template>
    <div>
        <form>
            <div class="col-xs-12 col-sm-12 col-md-12 col-lg-10 filter-flexbox-container">
                <span class="filter-flexbox-item margin-left-xs margin-right-xs">
                    <span>Нач. время:</span>
                    <datetime v-model="filterStartTime" type="datetime" zone="utc" value-zone="utc" input-class="form-control"></datetime>
                </span>

                <span class="filter-flexbox-item margin-left-xs margin-right-xs">
                    <span>Кон. время:</span>
                    <datetime v-model="filterEndTime" type="datetime" zone="utc" value-zone="utc" input-class="form-control"></datetime>
                </span>

                <span class="filter-flexbox-item margin-left-xs margin-right-xs">
                    <div>&nbsp;</div>
                    <button type="button" class="btn btn-primary margin-right-xs" @click="loadData(1)">Применить</button>
                    <button type="button" class="btn btn-secondary margin-left-xs" @click="clearFilters()">Очистить</button>
                </span>
            </div>
        </form>

        <hr>

        <div style="max-width: 700px; margin-left: auto; margin-right: auto">
            <line-chart v-if="chartData" :chart-data="chartData" :options="chartOptions"></line-chart>
        </div>

        <hr>

        <table class="custom-table">
            <thead class="custom-table-header">
            <tr>
                <th>№</th>
                <th>Время</th>
                <th>Значение</th>
                <th>Широта</th>
                <th>Долгота</th>
            </tr>
            </thead>

            <tbody class="custom-table-body">
            <tr v-for="(dataElem, index) in data" :id="`${fieldName}_elem${dataElem.id}`" :key="index">
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
                    На странице:
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
    props: ['robotName', 'fieldName', 'dbName'],
    data: function() {
        return {
            chartData: null,
            chartOptions: getChartOptions(this.$moment, this.scrollToTableRow),
            tableData: [],
            elementsPerPage: 20,
            _currentPage: 1,
            dbElementsCount: 0,
            filterStartTime: null,
            filterEndTime: null,
            minimumValue: null,
            averageValue: null,
            maximumValue: null
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

        scrollToTableRow(datasetIndex, index) {
            const neededId = this.chartData.datasets[datasetIndex].data[index].id;
            if (neededId !== null && neededId !== undefined) {
                console.log(`Scroll to elem${neededId}`);
                this.$scrollTo(`#${this.fieldName}_elem${neededId}`, 500, {
                    container: 'body',
                    easing: 'ease',
                    offset: 0,
                    force: true,
                    cancelable: true,
                    onStart: false,
                    onDone: false,
                    onCancel: false,
                    x: false,
                    y: true
                });
                const htmlElement = document.getElementById(`${this.fieldName}_elem${neededId}`);
                htmlElement.classList.add('highlighted');
                setTimeout(() => { htmlElement.classList.remove('highlighted') }, 2000);
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

            const response = await this.$store.state.requestService.getStatisticsChartData(
                this.robotName, this.dbName, this.fieldName, limit, offset, filterStartTime, filterEndTime
            );
            this.dbElementsCount = response.count;
            this.minimumValue = response.minimum;
            this.averageValue = response.average;
            this.maximumValue = response.maximum;

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

                const mainDataset = JSON.parse(JSON.stringify(datasetOptions));
                mainDataset.data = newData.map(elem => {
                    return {
                        x: elem.time,
                        y: elem.value,
                        latitude: elem.latitude,
                        longitude: elem.longitude,
                        id: elem.id
                    }
                });

                const minDataset = JSON.parse(JSON.stringify(datasetOptions));
                minDataset.borderColor = '#a9a400';
                minDataset.backgroundColor = '#a9a400';
                minDataset.label = 'Минимальное значение';
                minDataset.supported = 1;
                minDataset.data = newData.map(elem => {
                    return {
                        x: elem.time,
                        y: this.minimumValue
                    }
                });

                const avgDataset = JSON.parse(JSON.stringify(datasetOptions));
                avgDataset.borderColor = '#a9003a';
                avgDataset.backgroundColor = '#a9003a';
                avgDataset.label = 'Среднее значение';
                avgDataset.supported = 2;
                avgDataset.data = newData.map(elem => {
                    return {
                        x: elem.time,
                        y: this.averageValue
                    }
                });

                const maxDataset = JSON.parse(JSON.stringify(datasetOptions));
                maxDataset.borderColor = '#00a96f';
                maxDataset.backgroundColor = '#00a96f';
                maxDataset.label = 'Максимальное значение';
                maxDataset.supported = 3;
                maxDataset.data = newData.map(elem => {
                    return {
                        x: elem.time,
                        y: this.maximumValue
                    }
                });

                this.chartData = { datasets: [mainDataset, minDataset, avgDataset, maxDataset] };
            }
        }
    },
    mounted() {
        this.currentPage = 1;
    }
}

function getChartOptions(moment, scrollToFunc) {
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
                    labelString: 'Значение данных',
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
                    const text = [];

                    switch (data.datasets[tooltipItem.datasetIndex].supported) {
                        case 1:
                            text.push(`Минимальное значение`);
                            break;
                        case 2:
                            text.push(`Среднее значение`);
                            break;
                        case 3:
                            text.push(`Максимальное значение`);
                            break;
                        default:
                            const time = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].x;
                            const latitude = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].latitude;
                            const longitude = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].longitude;

                            text.push(`Время: ${moment(time).format('DD.MM.YYYY HH:mm:ss.SSS')}`);
                            text.push(`Широта: ${latitude}`);
                            text.push(`Долгота: ${longitude}`);
                            break;
                    }

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
        },
        onClick: function (event, selectedElements) {
            if (selectedElements.length > 0) {
                const datasetIndex = selectedElements[0]._datasetIndex;
                const index = selectedElements[0]._index;
                scrollToFunc(datasetIndex, index);
            }
        }
    }
}

const datasetOptions = {
    label: 'Данные',
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

    .filter-flexbox-item {
        flex-grow: 1;
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

    .chart-container {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
    }

    @keyframes highlight {
        $startBackground: currentBackground;
        0% { background: $startBackground; }
        50% { background: rgb(190, 190, 190); }
        100% { background: $startBackground; }
    }

    tr.highlighted {
        animation-duration: 2s;
        animation-name: highlight;
        animation-iteration-count: 1;
        animation-direction: alternate;
    }
</style>
