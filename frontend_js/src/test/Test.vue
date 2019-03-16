<template>
    <div>
        <test-animation></test-animation>
        <hr>
        <test-chart></test-chart>
        <hr>
        <test-select></test-select>
    </div>
</template>
<script>
import TestChart from './TestChart.vue';
import TestSelect from './TestSelect';
import TestAnimation from './TestAnimation';

export default {
    name: 'Test',
    components: {
        'test-chart': TestChart,
        'test-select': TestSelect,
        'test-animation': TestAnimation
    }
}
</script>

<style scoped>
</style>
