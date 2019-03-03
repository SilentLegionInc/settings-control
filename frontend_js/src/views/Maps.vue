<template>
    <div class="row">
        <div class="col-xs-12 col-sm-12 col-md-7 col-lg-7 margin-bottom-sm">
            <yandex-map
                :coords="[centerLatitude, centerLongitude]"
                zoom="10"
                style="width: 100%; height: 100%;"
                :cluster-options="{openBalloonOnClick: false}"
                :behaviors="['drag', 'multiTouch', 'scrollZoom', 'dblClickZoom', 'rightMouseButtonMagnifier']"
                :controls="['fullscreenControl', 'zoomControl', 'typeSelector', 'rulerControl']"
                :placemarks="placemarks"
            >
            </yandex-map>
        </div>

        <div v-if="selectedIndex !== null" class="col-xs-12 col-sm-12 col-md-5 col-lg-5 scrollable-info">
            <div class="row custom-list-header">
                <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
                    Информация
                </div>
            </div>
            <div class="custom-list-body">
                <div class="row">
                    <div class="col-xs-8 col-sm-8 col-md-8 col-lg-8">
                        Широта:
                    </div>
                    <div class="col-xs-4 col-sm-4 col-md-4 col-lg-4">
                        {{elements[selectedIndex].latitude}}
                    </div>
                </div>
                <div class="row">
                    <div class="col-xs-8 col-sm-8 col-md-8 col-lg-8">
                        Долгота:
                    </div>
                    <div class="col-xs-4 col-sm-4 col-md-4 col-lg-4">
                        {{elements[selectedIndex].longitude}}
                    </div>
                </div>
                <div class="row">
                    <div class="col-xs-8 col-sm-8 col-md-8 col-lg-8">
                        Количество:
                    </div>
                    <div class="col-xs-4 col-sm-4 col-md-4 col-lg-4">
                        {{elements[selectedIndex].count}}
                    </div>
                </div>
                <div class="row" v-for="(elem, index) in elements[selectedIndex].average" :key="index">
                    <div class="col-xs-8 col-sm-8 col-md-8 col-lg-8" style="word-wrap: break-word;">
                        Средн. {{elem.name.toLowerCase()}}:
                    </div>
                    <div class="col-xs-4 col-sm-4 col-md-4 col-lg-4">
                        {{elem.value}}
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12 margin-top-sm" style="padding-right: 0 !important;" align="right">
                    <button type="button" class="btn btn-primary" @click="redirectToTableStatistics">Подробнее</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { yandexMap } from 'vue-yandex-maps'
export default {
    name: 'Maps',
    components: { yandexMap },
    data() {
        return {
            placemarks: [],
            elements: [],
            selectedIndex: null,
            centerLatitude: 0,
            centerLongitude: 0,
            robotName: null,
            databaseName: null
        }
    },
    async mounted() {
        this.databaseName = this.$route.query.dbName;
        this.robotName = this.$store.state.robotName;
        const result = await this.$store.state.requestService.getStatisticsMapsData(this.robotName, this.databaseName);
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
    },
    methods: {
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
                        ${latitude}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        Долгота:
                    </div>
                    <div class="col-md-6">
                        ${longitude}
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

<style scoped>
    .scrollable-info {
        height: auto;
        max-height: 90%;
        overflow-y: auto;
    }
</style>
