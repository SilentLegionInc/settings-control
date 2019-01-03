import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Settings from './views/Settings'
import TableStatistics from './views/TableStatistics'
import ChartStatistics from './views/ChartStatistics'
import Logs from './views/Logs'

Vue.use(Router);

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home,
        },
        {
            path: '/test',
            name: 'test',
            // route level code-splitting
            // this generates a separate chunk (about.[hash].js) for this route
            // which is lazy-loaded when the route is visited.
            component: () => import('./views/Test.vue')
        },
        {
            path: '/settings',
            name: 'settings',
            component: Settings,
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
            path: '/logs',
            name: 'logs',
            component: Logs
        }
    ]
})
