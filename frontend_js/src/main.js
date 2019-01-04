import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import BootstrapVue from 'bootstrap-vue';
import VModal from 'vue-js-modal';
import Datetime from 'vue-datetime';
import 'vue-datetime/dist/vue-datetime.css';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'font-awesome/css/font-awesome.css';
import './global_css/styles.scss';

const moment = require('vue-moment');

Vue.config.productionTip = false;
Vue.use(VModal);
Vue.use(BootstrapVue);
Vue.use(moment);
Vue.use(Datetime);

// TODO move requestService to
new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app');
