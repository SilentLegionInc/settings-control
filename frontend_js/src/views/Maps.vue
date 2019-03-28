<template>
    <div class="container-fluid">
        <div class="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12">
            <div class="row">
                <div class="col-12 col-sm-12 col-md-12 col-lg-10 col-xl-8">
                    <div class="row">
                        <div class="col-12 col-sm-6 col-md-4 col-lg-4 col-xl-4 pl-1 pr-1">
                            <span>Нач. время:</span>
                            <datetime v-model="filter.startTime" type="datetime" zone="UTC" value-zone="UTC" input-class="form-control"></datetime>
                        </div>

                        <div class="col-12 col-sm-6 col-md-4 col-lg-4 col-xl-4 pl-1 pr-1">
                            <span>Кон. время:</span>
                            <datetime v-model="filter.endTime" type="datetime" zone="UTC" value-zone="UTC" input-class="form-control" :class="{'mb-3': !$isWideScreen()}"></datetime>
                        </div>

                        <div class="col-12 col-sm-12 col-md-2 col-lg-2 col-xl-2 pl-1 pr-1">
                            <span v-if="$isWideScreen()">&nbsp;</span>
                            <button type="button" class="btn btn-success btn-block" :class="{'mb-1': !$isWideScreen()}" @click="loadData()">Применить</button>
                        </div>
                        <div class="col-12 col-sm-12 col-md-2 col-lg-2 col-xl-2 pl-1 pr-1">
                            <span v-if="$isWideScreen()">&nbsp;</span>
                            <button type="button" class="btn btn-secondary btn-block" @click="clearFilters()">Очистить</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <hr>

        <div class="row" style="margin: auto;">
            <div class="col-12 col-sm-12 col-md-6 col-lg-7 col-xl-8">
                <yandex-map
                    :coords="[centerLatitude, centerLongitude]"
                    zoom="3"
                    class="maps-size mb-2"
                    :cluster-options="{openBalloonOnClick: false}"
                    :behaviors="['drag', 'multiTouch', 'scrollZoom', 'dblClickZoom', 'rightMouseButtonMagnifier']"
                    :controls="['fullscreenControl', 'zoomControl', 'typeSelector', 'rulerControl']"
                    :placemarks="placemarks"
                >
                </yandex-map>
            </div>

            <div class="col-12 col-sm-12 col-md-6 col-lg-5 col-xl-4">
                <div class="scrollable-info">
                    <div class="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12">
                        <div class="row custom-list-header">
                            <div class="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12">
                                Информация
                            </div>
                        </div>
                        <div class="custom-list-body">
                            <div class="row">
                                <div class="col-8 col-sm-8 col-md-8 col-lg-8 col-xl-8">
                                    Широта:
                                </div>
                                <div class="col-4 col-sm-4 col-md-4 col-lg-4 col-xl-4">
                            <span v-if="selectedIndex !== null">
                                {{elements[selectedIndex].latitude.toFixed(6)}}
                            </span>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-8 col-sm-8 col-md-8 col-lg-8 col-xl-8">
                                    Долгота:
                                </div>
                                <div class="col-4 col-sm-4 col-md-4 col-lg-4 col-xl-4">
                            <span v-if="selectedIndex !== null">
                                {{elements[selectedIndex].longitude.toFixed(6)}}
                            </span>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-8 col-sm-8 col-md-8 col-lg-8 col-xl-8">
                                    Количество:
                                </div>
                                <div class="col-4 col-sm-4 col-md-4 col-lg-4 col-xl-4">
                            <span v-if="selectedIndex !== null">
                                {{elements[selectedIndex].count}}
                            </span>
                                </div>
                            </div>
                            <div class="inverse-color" v-if="selectedIndex !== null">
                                <div class="row" v-for="(elem, index) in elements[selectedIndex].average" :key="index">
                                    <div class="col-8 col-sm-8 col-md-8 col-lg-8 col-xl-8" style="word-wrap: break-word;">
                                        Средн. {{elem.name.toLowerCase()}}:
                                    </div>
                                    <div class="col-4 col-sm-4 col-md-4 col-lg-4 col-xl-4">
                                        {{elem.value | toFixedPrecision}}
                                    </div>
                                </div>
                            </div>
                            <div class="inverse-color" v-else>
                                <div class="row" v-for="(elem, index) in numericFields" :key="index">
                                    <div class="col-8 col-sm-8 col-md-8 col-lg-8 col-xl-8" style="word-wrap: break-word;">
                                        Средн. {{elem.name.toLowerCase()}}:
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="offset-md-6 offset-lg-7 offset-xl-7 col-12 col-sm-12 col-md-6 col-lg-5 col-xl-5 mt-2 mb-1">
                                <button type="button" class="btn btn-primary btn-block" @click="redirectToTableStatistics">Подробнее</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { yandexMap } from 'vue-yandex-maps';
import { catchErrorsWrapper } from '../helpers';

export default {
    name: 'Maps',
    components: { yandexMap },
    data() {
        return {
            placemarks: [],
            elements: [],
            numericFields: [],
            selectedIndex: null,
            centerLatitude: 0,
            centerLongitude: 0,
            robotName: null,
            databaseName: null,
            filter: {}
        }
    },
    mounted() {
        this.databaseName = this.$route.query.dbName;
        this.robotName = this.$store.state.robotName;
        this.loadStartData();
    },
    methods: {
        async loadStartData() {
            this.loader = this.$loading.show();

            await catchErrorsWrapper(this.$toaster, async () => {
                this.numericFields = await this.$store.state.requestService.getStatisticsMapsData(this.robotName, this.databaseName, true);
            });

            this.loader.hide();
        },
        async loadData() {
            this.loader = this.$loading.show();

            await catchErrorsWrapper(this.$toaster, async () => {
                const filter = JSON.parse(JSON.stringify(this.filter));
                filter.startTime = filter.startTime ? new Date(filter.startTime) : null;
                filter.endTime = filter.endTime ? new Date(filter.endTime) : null;
                const result = await this.$store.state.requestService.getStatisticsMapsData(this.robotName, this.databaseName, false, filter);

                this.placemarks = [];
                this.elements = [];

                this.centerLatitude = result.centerLatitude;
                this.centerLongitude = result.centerLongitude;
                result.points.forEach((elem, index) => {
                    const placemark = JSON.parse(JSON.stringify(placemarkConfig));
                    placemark.markerId = `${index}`;
                    placemark.coords = [elem.latitude, elem.longitude];
                    placemark.callbacks = { click: (event) => { this.placemarkClicked(event, index) } };
                    // TODO
                    // placemark.icon = {
                    //     color: 'green',
                    //     content: `${elem.count}`,
                    //     glyph: 'cinema'
                    // };
                    placemark.balloonTemplate = this.getBalloon(elem.latitude, elem.longitude, elem.count);
                    this.placemarks.push(placemark);
                    this.elements.push(elem);
                });
            });

            this.loader.hide();
        },
        clearFilters() {
            this.filter.startTime = null;
            this.filter.endTime = null;
        },
        redirectToTableStatistics() {
            const latitude = this.elements[this.selectedIndex].latitude;
            const longitude = this.elements[this.selectedIndex].longitude;
            this.$router.push(`/table_statistics?dbName=${this.databaseName}&latitude=${latitude}&longitude=${longitude}`);
        },
        placemarkClicked(event, markerIndex) {
            this.selectedIndex = markerIndex;
        },
        getBalloon(latitude, longitude, count) {
            return `
                <div class="row">
                    <div class="col-md-6">
                        Широта:
                    </div>
                    <div class="col-md-6">
                        ${latitude.toFixed(6)}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        Долгота:
                    </div>
                    <div class="col-md-6">
                        ${longitude.toFixed(6)}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        Кол-во:
                    </div>
                    <div class="col-md-6">
                        ${count}
                    </div>
                </div>
                <a href="/table_statistics?dbName=${this.databaseName}&latitude=${latitude}&longitude=${longitude}">Подробнее</a>
            `
        }
    }
}

const placemarkConfig = {
    properties: {}, // define properties here
    options: {}, // define options here
    clusterName: '1'
}
</script>

<style scoped lang="scss">
    @import "../global_css/styles";

    @media only screen and (min-width: $min-wide-width) {
        .scrollable-info {
            max-height: 500px;
            overflow-y: auto;
        }
    }

    .maps-size {
        width: 100%; height: 100%; min-height: 500px;
    }

    .inverse-color div.row {
        background: rgb(240, 240, 240);
    }

    .inverse-color div.row:nth-child(even) {
        background: white;
    }
</style>
