import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import BootstrapVue from 'bootstrap-vue';
import Toaster from 'v-toaster';
import Datetime from 'vue-datetime';
import VueScrollTo from 'vue-scrollto';
import Loading from 'vue-loading-overlay';
import Moment from 'vue-moment';

import 'vue-loading-overlay/dist/vue-loading.css';
import 'vue-datetime/dist/vue-datetime.css';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import './global_css/styles.scss';
import 'v-toaster/dist/v-toaster.css'
import '@fortawesome/fontawesome-free/css/all.css';
// import { vsDivider } from 'vuesax'
// import 'vuesax/dist/vuesax.css'
import { LogLevel } from './models/LogModel';
import Config from './config';

Vue.config.productionTip = true;
Vue.use(BootstrapVue);
Vue.use(Moment);
Vue.use(Datetime);
Vue.use(Toaster, { timeout: 5000 });
Vue.use(Loading, {
    color: '#93a2f5',
    height: 100,
    width: 100,
    loader: 'bars',
    backgroundColor: '#000000',
    opacity: 0.8
});
// Vue.use(vsDivider);
Vue.use(VueScrollTo, {
    container: 'body',
    duration: 500,
    easing: 'ease',
    offset: 0,
    force: true,
    cancelable: true,
    onStart: false,
    onDone: false,
    onCancel: false,
    x: false,
    y: true
});

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

Vue.filter('toFixedPrecision', value => {
    return value.toFixed(Config.floatPrecision);
});

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app');
