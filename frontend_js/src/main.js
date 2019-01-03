import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import BootstrapVue from 'bootstrap-vue';
import VModal from 'vue-js-modal'
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'font-awesome/css/font-awesome.css';
import './global_css/styles.scss';
import { RequestService } from './services/RequestService';

const moment = require('vue-moment');

Vue.config.productionTip = false;
Vue.use(VModal);
Vue.use(BootstrapVue);
Vue.use(moment);

// TODO move requestService to
new Vue({
    router,
    store,
    render: h => h(App),
    data: {
        requestService: new RequestService()
    }
}).$mount('#app');
