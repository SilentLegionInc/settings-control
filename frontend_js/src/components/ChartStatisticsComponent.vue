<template>
    <div>
        <div class="container-fluid">
            <div class="row">
                <div class="col-12 col-sm-12 col-md-12 col-lg-10 col-xl-8">
                    <div class="row">
                        <div class="col-12 col-sm-6 col-md-4 col-lg-4 col-xl-4 pl-1 pr-1">
                            <span class="ml-1">Нач. время:</span>
                            <datetime v-model="filterStartTime" type="datetime" zone="UTC" value-zone="UTC" input-class="form-control"></datetime>
                        </div>

                        <div class="col-12 col-sm-6 col-md-4 col-lg-4 col-xl-4 pl-1 pr-1">
                            <span class="ml-1">Кон. время:</span>
                            <datetime v-model="filterEndTime" type="datetime" zone="UTC" value-zone="UTC" input-class="form-control" :class="{'mb-3': !$isWideScreen()}"></datetime>
                        </div>

                        <div class="col-12 col-sm-12 col-md-2 col-lg-2 col-xl-2 pl-1 pr-1">
                            <span v-if="$isWideScreen()">&nbsp;</span>
                            <button type="button" class="btn btn-success btn-block" :class="{'mb-1': !$isWideScreen()}" @click="loadFilterData()">Применить</button>
                        </div>
                        <div class="col-12 col-sm-12 col-md-2 col-lg-2 col-xl-2 pl-1 pr-1">
                            <span v-if="$isWideScreen()">&nbsp;</span>
                            <button type="button" class="btn btn-secondary btn-block" :class="{'mb-1': !$isWideScreen()}" @click="clearFilters()">Очистить</button>
                        </div>

                        <div v-if="!$isWideScreen()" class="col-12 col-sm-12 col-md-5 col-lg-4 col-xl-3 pl-1 pr-1">
                            <div class="row">
                                <div class="col-6 col-sm-6 col-md-6 col-lg-6 col-xl-6 pr-1">
                                    <button type="button" class="btn btn-primary btn-block mb-1" @click="loadLeftPageData()" :disabled="!leftPageActive">&#10094;</button>
                                </div>
                                <div class="col-6 col-sm-6 col-md-6 col-lg-6 col-xl-6 pl-1">
                                    <button type="button" class="btn btn-primary btn-block" @click="loadRightPageData()" :disabled="!rightPageActive">&#10095;</button>
                                </div>
                            </div>
                        </div>

                        <div v-if="!$isWideScreen()" class="col-12 col-sm-12 col-md-5 col-lg-4 col-xl-3 pl-1 pr-1">
                            <button type="button" class="btn btn-secondary btn-block" @click="showModal()">Изменить интервал</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <hr>

        <div class="container-fluid">
            <div class="row mb-3">
                <div class="col-12 col-sm-12 col-md-12 col-lg-6 col-xl-6">
                    <line-chart :id="`${fieldName}_chart`" v-if="chartData" :chart-data="chartData" :options="chartOptions"></line-chart>
                </div>
                <div class="col-12 col-sm-12 col-md-12 col-lg-6 col-xl-6">
                    <div :id="`${fieldName}-table-container`" class="table-container" style="overflow-x: auto;">
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

            <div v-if="$isWideScreen()" class="row">
                <div class="offset-md-2 offset-lg-3 offset-xl-3 col-12 col-sm-12 col-md-8 col-lg-6 col-xl-6">
                    <div class="row">
                        <div class="offset-0 offset-sm-1 offset-md-0 offset-lg-0 offset-xl-1 col-3 col-sm-3 col-md-3 col-lg-3 col-xl-3 pr-1">
                            <button type="button" class="btn btn-primary btn-block mb-2" @click="loadLeftPageData()" :disabled="!leftPageActive">&#10094;</button>
                        </div>
                        <div class="col-6 col-sm-4 col-md-6 col-lg-6 col-xl-4 pl-1 pr-1">
                            <button type="button" class="btn btn-secondary btn-block" @click="showModal()">Изменить интервал</button>
                        </div>
                        <div class="col-3 col-sm-3 col-md-3 col-lg-3 col-xl-3 pl-1">
                            <button type="button" class="btn btn-primary btn-block mb-2" @click="loadRightPageData()" :disabled="!rightPageActive">&#10095;</button>
                        </div>
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
import { catchErrorsWrapper } from '../helpers';
import { ClientExceptionModel } from '../models/ClientExceptionModel';

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
                    container: this.$isWideScreen() ? `#${this.fieldName}-table-container` : 'body',
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
            this.loader = this.$loading.show();

            await catchErrorsWrapper(this.$toaster, async () => {
                if (!this.robotName || !this.dbName || !this.fieldName) {
                    throw new ClientExceptionModel('Chart statistics: can\'t load data, one of required params is empty');
                }

                const response = await this.$store.state.requestService.getStatisticsInitChartData(
                    this.robotName, this.dbName, this.fieldName, this.intervalSize
                );

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
            });

            this.loader.hide();
        },
        async loadFilterData() {
            this.loader = this.$loading.show();

            await catchErrorsWrapper(this.$toaster, async () => {
                if (!this.robotName || !this.dbName || !this.fieldName) {
                    throw new ClientExceptionModel('Chart statistics: can\'t load data, one of required params is empty');
                }

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
            });

            this.loader.hide();
        },
        async loadLeftPageData() {
            this.loader = this.$loading.show();

            await catchErrorsWrapper(this.$toaster, async () => {
                if (!this.robotName || !this.dbName || !this.fieldName) {
                    throw new ClientExceptionModel('Chart statistics: can\'t load data, one of required params is empty');
                }

                this.intervalEndTime = this.intervalStartTime;
                this.intervalStartTime = this.$moment(this.intervalStartTime).subtract(this.intervalSize, 'm').toDate();
                this.intervalStartTime = this.intervalStartTime > this.minTime ? this.intervalStartTime : this.minTime;

                this.data = await this.$store.state.requestService.getStatisticsPageChartData(
                    this.robotName, this.dbName, this.fieldName, this.intervalStartTime, this.intervalEndTime
                );
            });

            this.loader.hide();
        },
        async loadRightPageData() {
            this.loader = this.$loading.show();

            await catchErrorsWrapper(this.$toaster, async () => {
                if (!this.robotName || !this.dbName || !this.fieldName) {
                    throw new ClientExceptionModel('Chart statistics: can\'t load data, one of required params is empty');
                }

                this.intervalStartTime = this.intervalEndTime;
                this.intervalEndTime = this.$moment(this.intervalEndTime).add(this.intervalSize, 'm').toDate();
                this.intervalEndTime = this.intervalEndTime < this.maxTime ? this.intervalEndTime : this.maxTime;

                this.data = await this.$store.state.requestService.getStatisticsPageChartData(
                    this.robotName, this.dbName, this.fieldName, this.intervalStartTime, this.intervalEndTime
                );
            });

            this.loader.hide();
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
    @import "../global_css/styles";

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

    @media only screen and (min-width: $min-wide-width) {
        .table-container {
            overflow-y: auto;
            max-height: 400px;
        }
    }
</style>
