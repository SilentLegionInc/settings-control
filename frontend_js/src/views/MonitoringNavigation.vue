<template>
    <div class="container-fluid">
        <div v-for="(elem, index) in databasesInfo" :key="index" class="row">
            <div class="col-3 col-sm-3 col-md-3 col-lg-3 col-xl-3">
                {{elem.name}}
            </div>

            <div class="col-3 col-sm-3 col-md-3 col-lg-3 col-xl-3">
                <router-link :to="`/chart_statistics?dbName=${elem.systemName}`">
                    Графики
                </router-link>
            </div>

            <div class="col-3 col-sm-3 col-md-3 col-lg-3 col-xl-3">
                <router-link :to="`/table_statistics?dbName=${elem.systemName}`">
                    Таблицы
                </router-link>
            </div>

            <div class="col-3 col-sm-3 col-md-3 col-lg-3 col-xl-3">
                <router-link :to="`/maps_statistics?dbName=${elem.systemName}`">
                    Карты
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>
import { catchErrorsWrapper } from '../helpers';

export default {
    name: 'MonitoringNavigation',
    data() {
        return {
            robotName: null,
            databasesInfo: []
        }
    },
    methods: {
        async loadDatabasesInfo() {
            this.loader = this.$loading.show();

            await catchErrorsWrapper(this.$toaster, async () => {
                this.robotName = this.$store.state.robotName;
                this.databasesInfo = await this.$store.state.requestService.getStatisticsDatabasesInfo(this.robotName);
            });

            this.loader.hide();
        }
    },
    mounted() {
        this.loadDatabasesInfo();
    }
}
</script>

<style scoped>

</style>
