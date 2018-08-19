import { Line, mixins } from 'vue-chartjs';
import { Component, Vue, Prop } from 'vue-property-decorator';
const { reactiveProp } = mixins;

@Component({
    mixins: [Line, reactiveProp],
})
export default class LineChart extends Line {
    @Prop() public chartData!: any;
    @Prop() public options!: any;

    private mounted() {
        this.renderChart(this.chartData, this.options);
    }
}
