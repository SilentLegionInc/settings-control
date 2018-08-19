import Vue from 'vue';
import App from './App.vue';
import router from './router';
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'font-awesome/css/font-awesome.css';
import './styles.scss';
import vmodal from 'vue-js-modal';

const moment = require('vue-moment');

Vue.use(BootstrapVue);
Vue.use(vmodal);
Vue.use(moment);

Vue.config.productionTip = false;

new Vue({
    router,
    render: h => h(App),
}).$mount('#app');
