<template>
    <div>
        <form>
            <div class="container-fluid">
                <div class="row">
                    <div class="col-12 col-sm-12 col-md-12 col-lg-10 col-xl-8 filter-flexbox-container">
                        <span class="filter-flexbox-item ml-1 mr-1">
                            <span>Нач. время:</span>
                            <datetime v-model="filterStartTime" type="datetime" zone="UTC" value-zone="UTC" input-class="form-control"></datetime>
                        </span>

                        <span class="filter-flexbox-item ml-1 mr-1">
                            <span>Кон. время:</span>
                            <datetime v-model="filterEndTime" type="datetime" zone="UTC" value-zone="UTC" input-class="form-control"></datetime>
                        </span>

                        <span class="filter-flexbox-item ml-1 mr-1">
                            <div>&nbsp;</div>
                            <button type="button" class="btn btn-primary mr-1" @click="loadFilterData()">Применить</button>
                            <button type="button" class="btn btn-secondary ml-1" @click="clearFilters()">Очистить</button>
                        </span>
                    </div>
                </div>

                <div class="row pt-2">
                    <div class="col-12 col-sm-12 col-md-6 col-lg-4 col-xl-3">
                        <button type="button" class="btn btn-primary mr-1" @click="loadLeftPageData()" :disabled="!leftPageActive">&#10094;</button>
                        <button type="button" class="btn btn-primary ml-1 mr-1" @click="loadRightPageData()" :disabled="!rightPageActive">&#10095;</button>
                        <button type="button" class="btn btn-secondary ml-1" @click="showModal()">Изменить интервал</button>
                    </div>
                </div>
            </div>
        </form>

        <hr>

        <div class="container-fluid">
            <div class="row">
                <div class="col-12 col-sm-12 col-md-12 col-lg-6 col-xl-6">
                    <line-chart :id="`${fieldName}_chart`" v-if="chartData" :chart-data="chartData" :options="chartOptions"></line-chart>
                </div>
                <div class="col-12 col-sm-12 col-md-12 col-lg-6 col-xl-6">
                    <div :id="`${fieldName}-table-container`" class="table-container">
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
                                <td>{{ index + 1 }}</td>
                                <td>{{ dataElem.time | moment("DD.MM.YYYY HH:mm:ss.SSS") }}</td>
                                <td>{{ dataElem.value | toFixedPrecision }}</td>
                                <td>{{ dataElem.latitude | toFixedPrecision }}</td>
                                <td>{{ dataElem.longitude | toFixedPrecision }}</td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <b-modal :ref="`${fieldName}_modal`"
                 :id="`${fieldName}_modal`"
                 size="md"
                 title="Изменение интервала"
                 centered
                 @ok="onModalOk()"
        >
            <div class="container-fluid">
                <div class="row mb-2">
                    <div class="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12">
                        <b>Внимание!</b> Большой интервал может замедлить работу приложения. Рекомендуемый размер - 3 минуты.
                    </div>
                </div>
                <div class="row">
                    <div class="col-8 col-sm-7 col-md-7 col-lg-6 col-xl-5">
                        <b>Интервал в минутах:</b>
                    </div>
                    <div class="col-4 col-sm-5 col-md-5 col-lg-6 col-xl-7" align="left">
                        <input v-model="tempIntervalSize" type="number" class="form-control">
                    </div>
                </div>
            </div>
        </b-modal>
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
    props: {
        robotName: {
            type: String,
            required: true
        },
        dbName: {
            type: String,
            required: true
        },
        fieldName: {
            type: String,
            required: true
        }
    },
    data: function() {
        return {
            chartData: null,
            chartOptions: getChartOptions(this.$moment, this.scrollToTableRow),
            tableData: [],
            minTime: null,
            maxTime: null,
            filterStartTime: null,
            filterEndTime: null,
            intervalStartTime: null,
            intervalEndTime: null,
            tempIntervalSize: '3',
            intervalSize: 3,
            minimumValue: null,
            averageValue: null,
            maximumValue: null
        }
    },
    methods: {
        scrollToTableRow(datasetIndex, index) {
            const neededId = this.chartData.datasets[datasetIndex].data[index].id;
            if (neededId !== null && neededId !== undefined) {
                this.$scrollTo(`#${this.fieldName}_elem${neededId}`, 500, {
                    container: `#${this.fieldName}-table-container`,
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
        showModal() {
            this.$refs[`${this.fieldName}_modal`].show();
        },
        onModalOk() {
            this.intervalSize = Number.parseInt(this.tempIntervalSize);
            this.loadFilterData();
        },
        async loadInitData() {
            if (!this.robotName || !this.dbName || !this.fieldName) {
                Logger.error(`Chart statistics: can't load data, one of required params is empty`);
                return;
            }

            const loader = this.$loading.show();

            const response = await this.$store.state.requestService.getStatisticsInitChartData(
                this.robotName, this.dbName, this.fieldName, this.intervalSize
            );

            console.log(response.minTime);
            console.log(response.maxTime);
            this.minTime = response.minTime;
            this.maxTime = response.maxTime;
            this.filterStartTime = response.minTime.toISOString();
            this.filterEndTime = response.maxTime.toISOString();
            this.intervalStartTime = response.intervalStartTime;
            this.intervalEndTime = response.intervalEndTime;
            this.minimumValue = response.minimum;
            this.averageValue = response.average;
            this.maximumValue = response.maximum;
            this.data = response.result;

            loader.hide();
        },
        async loadFilterData() {
            if (!this.robotName || !this.dbName || !this.fieldName) {
                Logger.error(`Chart statistics: can't load data, one of required params is empty`);
                return;
            }

            const loader = this.$loading.show();

            const filterStartTime = new Date(this.filterStartTime);
            const filterEndTime = new Date(this.filterEndTime);

            const response = await this.$store.state.requestService.getStatisticsFilterChartData(
                this.robotName, this.dbName, this.fieldName, filterStartTime, filterEndTime, this.intervalSize
            );

            this.minTime = filterStartTime;
            this.maxTime = filterEndTime;
            this.intervalStartTime = response.intervalStartTime;
            this.intervalEndTime = response.intervalEndTime;
            this.minimumValue = response.minimum;
            this.averageValue = response.average;
            this.maximumValue = response.maximum;
            this.data = response.result;

            loader.hide();
        },
        async loadLeftPageData() {
            if (!this.robotName || !this.dbName || !this.fieldName) {
                Logger.error(`Chart statistics: can't load data, one of required params is empty`);
                return;
            }

            const loader = this.$loading.show();

            this.intervalEndTime = this.intervalStartTime;
            this.intervalStartTime = this.$moment(this.intervalStartTime).subtract(this.intervalSize, 'm').toDate();
            this.intervalStartTime = this.intervalStartTime > this.minTime ? this.intervalStartTime : this.minTime;

            this.data = await this.$store.state.requestService.getStatisticsPageChartData(
                this.robotName, this.dbName, this.fieldName, this.intervalStartTime, this.intervalEndTime
            );

            loader.hide();
        },
        async loadRightPageData() {
            if (!this.robotName || !this.dbName || !this.fieldName) {
                Logger.error(`Chart statistics: can't load data, one of required params is empty`);
                return;
            }

            const loader = this.$loading.show();

            this.intervalStartTime = this.intervalEndTime;
            this.intervalEndTime = this.$moment(this.intervalEndTime).add(this.intervalSize, 'm').toDate();
            this.intervalEndTime = this.intervalEndTime < this.maxTime ? this.intervalEndTime : this.maxTime;

            this.data = await this.$store.state.requestService.getStatisticsPageChartData(
                this.robotName, this.dbName, this.fieldName, this.intervalStartTime, this.intervalEndTime
            );

            loader.hide();
        }
    },
    computed: {
        leftPageActive: function() {
            return this.intervalStartTime > this.minTime;
        },
        rightPageActive: function() {
            return this.intervalEndTime < this.maxTime;
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
                minDataset.spanGaps = true;
                minDataset.label = 'Минимальное значение';
                minDataset.supported = 1;
                minDataset.data = newData.map((elem, index) => {
                    return {
                        x: elem.time,
                        y: (index === 0 || index === newData.length - 1) ? this.minimumValue : null
                    }
                });

                const avgDataset = JSON.parse(JSON.stringify(datasetOptions));
                avgDataset.borderColor = '#a9003a';
                avgDataset.backgroundColor = '#a9003a';
                avgDataset.spanGaps = true;
                avgDataset.label = 'Среднее значение';
                avgDataset.supported = 2;
                avgDataset.data = newData.map((elem, index) => {
                    return {
                        x: elem.time,
                        y: (index === 0 || index === newData.length - 1) ? this.averageValue : null
                    }
                });

                const maxDataset = JSON.parse(JSON.stringify(datasetOptions));
                maxDataset.borderColor = '#00a96f';
                maxDataset.backgroundColor = '#00a96f';
                maxDataset.spanGaps = true;
                maxDataset.label = 'Максимальное значение';
                maxDataset.supported = 3;
                maxDataset.data = newData.map((elem, index) => {
                    return {
                        x: elem.time,
                        y: (index === 0 || index === newData.length - 1) ? this.maximumValue : null
                    }
                });

                this.chartData = { datasets: [mainDataset, minDataset, avgDataset, maxDataset] };
            }
        }
    },
    mounted() {
        this.loadInitData();
    }
}

function getChartOptions(moment, scrollToFunc) {
    return {
        maintainAspectRatio: false,
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
                        second: 'HH:mm:ss'
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

    @media  only screen and (min-resolution: 165dpi) and (max-resolution: 168dpi),
            only screen and (min-resolution: 155dpi) and (max-resolution: 160dpi),
            only screen and (min-resolution: 134dpi) and (max-resolution: 144dpi),
            only screen and (min-resolution: 120dpi) and (max-resolution: 130dpi),
            only screen and (max-resolution: 116dpi) {
        .table-container {
            overflow-y: auto;
            overflow-x: hidden;
            max-height: 400px;
        }
    }
</style>
