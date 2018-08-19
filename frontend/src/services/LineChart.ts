import { Line } from 'vue-chartjs';
import { Component, Vue, Prop } from 'vue-property-decorator';

@Component
export default class LineChart extends Line {
    @Prop() public datasets!: any;
    @Prop() public options!: any;

    private mounted() {
        this.renderChart(this.datasets, this.options);
    }
}
