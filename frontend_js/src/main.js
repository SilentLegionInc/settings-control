import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import BootstrapVue from 'bootstrap-vue';
import Toaster from 'v-toaster'
import VModal from 'vue-js-modal';
import Datetime from 'vue-datetime';

import 'vue-datetime/dist/vue-datetime.css';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
// import 'font-awesome/css/font-awesome.css';
import './global_css/styles.scss';
import 'v-toaster/dist/v-toaster.css'
import '@fortawesome/fontawesome-free/css/all.css'

import { LogLevel } from './models/LogModel';

const moment = require('vue-moment');

Vue.config.productionTip = false;
Vue.use(VModal);
Vue.use(BootstrapVue);
Vue.use(moment);
Vue.use(Datetime);
Vue.use(Toaster, { timeout: 5000 })

Vue.filter('logLevelToString', level => {
    switch (level) {
    case LogLevel.INFO:
        return 'Info';
    case LogLevel.DEBUG:
        return 'Debug';
    case LogLevel.WARNING:
        return 'Warning';
    case LogLevel.CRITICAL:
        return 'Critical';
    default:
        return 'Unknown';
    }
});

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app');
