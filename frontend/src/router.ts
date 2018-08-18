import Vue from 'vue';
import Router from 'vue-router';
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'font-awesome/css/font-awesome.css';
import './styles.scss';

import Test from './components/Test.vue';
import Home from './components/Home.vue';
import Settings from './components/Settings.vue';
import TableStatistics from './components/TableStatistics.vue';
import ChartStatistics from './components/ChartStatistics.vue';

Vue.use(Router);
Vue.use(BootstrapVue);

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
