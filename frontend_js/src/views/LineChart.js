import { Line, mixins } from 'vue-chartjs'

export default {
    extends: Line,
    mixins: [mixins.reactiveProp],
    mounted () {
        // this.chartData is created in the mixin.
        // If you want to pass options please create a local options object
        this.renderChart(this.chartData, this.options)
    }
}
