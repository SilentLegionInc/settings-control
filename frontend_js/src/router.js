import Vue from 'vue';
import Router from 'vue-router';
import Home from './views/Home.vue';
import Settings from './views/Settings';
import TableStatistics from './views/TableStatistics';
import ChartStatistics from './views/ChartStatistics';
import Networks from './views/Networks';
import Logs from './views/Logs';
import Maps from './views/Maps';
import Modules from './views/Modules';
import ChangePassword from './views/ChangePassword';
import store from './store';
import MonitoringNavigation from './views/MonitoringNavigation';
import SystemInfo from './views/SystemInfo';
import ServerSettings from './views/ServerSettings'

Vue.use(Router);

// const ifNotAuthenticated = (to, from, next) => {
//     if (!store.getters.isAuthenticated) {
//         next()
//         return
//     }
//     next('/');
// }

const ifAuthenticated = (to, from, next) => {
    if (store.getters.isAuthenticated) {
        next()
        return
    }
    if (from) {
        next(from);
    } else {
        next('/');
    }
}

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home
        },
        {
            path: '/test',
            name: 'test',
            // route level code-splitting
            // this generates a separate chunk (about.[hash].js) for this route
            // which is lazy-loaded when the route is visited.
            component: () => import('./test/Test.vue')
        },
        {
            path: '/settings',
            name: 'settings',
            component: Settings,
            beforeEnter: ifAuthenticated
        },
        {
            path: '/wifi',
            name: 'network',
            component: Networks,
            beforeEnter: ifAuthenticated
        },
        {
            path: '/modules',
            name: 'module',
            component: Modules,
            beforeEnter: ifAuthenticated
        },
        {
            path: '/server_settings',
            name: 'server-settings',
            component: ServerSettings,
            beforeEnter: ifAuthenticated
        },
        {
            path: '/monitoring_navigation',
            name: 'monitoring-navigation',
            component: MonitoringNavigation
        },
        {
            path: '/table_statistics',
            name: 'table-statistics',
            component: TableStatistics
        },
        {
            path: '/chart_statistics',
            name: 'chart-statistics',
            component: ChartStatistics
        },
        {
            path: '/maps_statistics',
            name: 'maps-statistics',
            component: Maps
        },
        {
            path: '/logs',
            name: 'logs',
            component: Logs
        },
        {
            path: '/system_info',
            name: 'sytem-info',
            component: SystemInfo
        },
        {
            path: '/change_password',
            name: 'change-password',
            component: ChangePassword,
            beforeEnter: ifAuthenticated
        }
    ]
})
