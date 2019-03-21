<template>
    <div>
        <test-animation></test-animation>
        <hr>
        <test-chart></test-chart>
        <hr>
        <test-select></test-select>
        <div class="my_container">
            <span style="flex-grow: 2"><hr></span><span style="flex-basis: auto" class="ml-2 mr-2">ОПРЛДЫОВАТЫОЛВИОЛЫВИТЛОЫВАТЫВЛОИТЛОЫВТАЛОЫВТМЛОЫВТМЛОЫВТМЛОДЫВМТЫЛДОВМТЫЛВО</span><span style="flex-grow: 2"><hr></span>
        </div>
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
    .my_container {
        display: flex;
        flex-direction: row;
        flex-wrap: nowrap;
        justify-content: center;
        align-items: center;
    }

</style>
