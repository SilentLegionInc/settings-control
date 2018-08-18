import Vue from 'vue';
import Router from 'vue-router';

import Test from './components/Test.vue';
import Home from './components/Home.vue';
import Settings from './components/Settings.vue';
import TableStatistics from './components/TableStatistics.vue';
import ChartStatistics from './components/ChartStatistics.vue';

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home,
        },
        {
            path: '/test',
            name: 'test',
            component: Test,
        },
        {
            path: '/settings',
            name: 'settings',
            component: Settings,
        },
        {
            path: '/table_statistics',
            name: 'table-statistics',
            component: TableStatistics,
        },
        {
            path: '/chart_statistics',
            name: 'chart-statistics',
            component: ChartStatistics,
        },
    ],
});
