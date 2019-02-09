<template>
    <yandex-map
        :coords="[centerLatitude, centerLongitude]"
        zoom="10"
        style="width: 600px; height: 600px;"
        :cluster-options="{1: {clusterDisableClickZoom: true}}"
        :behaviors="['drag', 'multiTouch', 'scrollZoom', 'dblClickZoom', 'rightMouseButtonMagnifier']"
        :controls="['fullscreenControl', 'zoomControl', 'typeSelector', 'rulerControl']"
        :placemarks="placemarks"
    >
    </yandex-map>
</template>

<script>
import { yandexMap } from 'vue-yandex-maps';
export default {
    name: 'Maps',
    components: { yandexMap },
    data() {
        return {
            placemarks: [],
            currentRobot: 'AMTS', // TODO get if from $store
            centerLatitude: 0,
            centerLongitude: 0
        }
    },
    async mounted() {
        const result = await this.$store.state.requestService.getStatisticsMapsData(this.currentRobot);
        this.centerLatitude = result.centerLatitude;
        this.centerLongitude = result.centerLongitude;
        this.placemarks = result.points.map((elem, index) => {
            const placemark = JSON.parse(JSON.stringify(placemarkConfig));
            placemark.markerId = `${index}`;
            placemark.coords = [elem.latitude, elem.longitude];
            placemark.callbacks = { click: this.placemarkClicked };
            return placemark;
        });
    },
    methods: {
        placemarkClicked(event) {
            console.log(event);
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

</style>
