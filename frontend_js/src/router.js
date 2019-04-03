import Vue from 'vue';
import Router from 'vue-router';
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
import ServerConnect from './components/ServerConnect'
import LoginPage from './views/LoginPage';

Vue.use(Router);

const ifAuthenticated = (to, from, next) => {
    if (store.getters.isAuthenticated) {
        next();
        return
    } else {
        const authToken = Vue.prototype.$cookies.get('toolBeltAuthToken');
        if (authToken && authToken !== 'undefined') {
            store.commit('setAuthToken', authToken);
            next();
            return;
        }
    }
    if (from) {
        Vue.prototype.$toaster.error('Для доступа к этой странице необходима авторизация');
        next('/login');
    } else {
        Vue.prototype.$toaster.error('Для доступа к этой странице необходима авторизация');
        next('/login');
    }
};

const isServerConnected = (to, from, next) => {
    if (store.state.robotName) {
        next();
    } else {
        Vue.prototype.$toaster.error('Для доступа к этой странице необходимо подключиться к серверу');
        next('/');
    }
};

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'connect-to-server',
            component: ServerConnect
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
            component: MonitoringNavigation,
            beforeEnter: isServerConnected
        },
        {
            path: '/table_statistics',
            name: 'table-statistics',
            component: TableStatistics,
            beforeEnter: isServerConnected
        },
        {
            path: '/chart_statistics',
            name: 'chart-statistics',
            component: ChartStatistics,
            beforeEnter: isServerConnected
        },
        {
            path: '/maps_statistics',
            name: 'maps-statistics',
            component: Maps,
            beforeEnter: isServerConnected
        },
        {
            path: '/logs',
            name: 'logs',
            component: Logs,
            beforeEnter: isServerConnected
        },
        {
            path: '/system_info',
            name: 'system-info',
            component: SystemInfo,
            beforeEnter: isServerConnected
        },
        {
            path: '/change_password',
            name: 'change-password',
            component: ChangePassword,
            beforeEnter: ifAuthenticated
        },
        {
            path: '/login',
            name: 'login-page',
            component: LoginPage
        }
    ]
})
