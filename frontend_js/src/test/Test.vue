<template>
    <div>
        <test-animation></test-animation>
        <hr>
        <test-file-upload></test-file-upload>
        <hr>
        <test-chart></test-chart>
        <hr>
        <test-select></test-select>
    </div>
</template>
<script>
import TestChart from './TestChart.vue';
import TestFileUpload from './TestFileUpload';
import TestSelect from './TestSelect';
import TestAnimation from './TestAnimation';

export default {
    name: 'Test',
    components: {
        'test-chart': TestChart,
        'test-file-upload': TestFileUpload,
        'test-select': TestSelect,
        'test-animation': TestAnimation
    }
}
</script>

<style scoped>

</style>
