<template>
    <div>
        <capacity-component :percent-value="percentValue" :free-value="freeValue" :max-value="maxValue"></capacity-component>
    </div>
</template>

<script>
import CapacityComponent from '../components/CapacityComponent';

export default {
    name: 'SystemInfo',
    components: { CapacityComponent },
    data: function() {
        return {
            percentValue: 72.1,
            freeValue: 70947196928,
            maxValue: 254721126400,

            diskInfo: null,
            memoryInfo: null
        }
    },
    methods: {
        async loadFullData() {
            const response = await this.$store.state.requestService.getSystemInfo();
            this.diskInfo = response.diskInfo;
            this.memoryInfo = response.memoryInfo;
            // TODO increment cpu info array
        }
    }
}
</script>

<style scoped>

</style>
