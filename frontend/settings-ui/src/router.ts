import Vue from 'vue';
import Router from 'vue-router';
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'font-awesome/css/font-awesome.css';
import './styles.scss';

import Example from './components/Example.vue';
import Settings from './components/Settings.vue';

Vue.use(Router);
Vue.use(BootstrapVue);

export default new Router({
    routes: [
        {
            path: '/',
            name: 'home',
            component: Example,
        },
        {
            path: '/settings',
            name: 'settings',
            component: Settings,
        },
    ],
});
