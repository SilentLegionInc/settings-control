<template>
    <div>
        <h1>
            Chart statistics
        </h1>
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <!--<line-chart :chartData="datasets"-->
                                <!--:options="options"-->
                                <!--:width="800"-->
                                <!--:height="400">-->
                    <!--</line-chart>-->
                </div>
            </div>
            <div class="row">
                <div class="col-md-9 offset-md-2" align="right">
                    <button class="btn btn-primary" @click="generateDataSets()">Add a point</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'ChartStatistics',
        data: function() {
            return {
                datasets: {
                    labels: ['labelOne', 'labelTwo'],
                    datasets: [
                        {
                            label: 'Data One',
                            backgroundColor: '#f87979',
                            data: [0, 1]
                        }, {
                            label: 'Data One',
                            backgroundColor: '#f87979',
                            data: [1, 2]
                        }
                    ]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            };
        },
        methods: {
            addPoint: function() {
                this.datasets.labels.push(new Date().toDateString());
                this.datasets.datasets.forEach(elem => {
                    elem.data.push(3);
                })
            },

            generateDataSets: function() {
                this.datasets = {
                    labels: ['label One ' + new Date().toDateString(), 'label Two' + new Date().toDateString()],
                    datasets: [
                        {
                            label: 'Data One',
                            backgroundColor: '#f87979',
                            data: [Math.random() * 100, Math.random() * 100]
                        }, {
                            label: 'Data Two',
                            backgroundColor: '#f87979',
                            data: [Math.random() * 100, Math.random() * 100, Math.random() * 100]
                        }
                    ]
                }
            }
        }
    }
</script>

<style scoped lang="scss">
</style>