import { Line, mixins } from 'vue-chartjs';
import zoom from 'chartjs-plugin-zoom';

export default {
    extends: Line,
    mixins: [mixins.reactiveProp],
    props: ['options'],
    mounted () {
        this.addPlugin(zoom);
        // this.chartData is created in the mixin.
        // If you want to pass options please create a local options object
        this.renderChart(this.chartData, this.options)
    }
}
