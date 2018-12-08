import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import BootstrapVue from 'bootstrap-vue';
import VModal from 'vue-js-modal'
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import Header from '@/components/Header.vue';
import Sidebar from '@/components/Sidebar.vue';
import Footer from '@/components/Footer.vue';
import Settings from '@/views/Settings.vue';

Vue.config.productionTip = false
Vue.use(VModal);
Vue.use(BootstrapVue);

new Vue({
    router,
    store,
    render: h => h(App),
    components: {
        'app-header': Header,
        'app-sidebar': Sidebar,
        'app-footer': Footer,
        'app-settings': Settings
    },
    data: function() {
        return {
            sidebarIsOpened: false
        }
    },
    methods: {
        onSidebarOpened: function() {
            this.sidebarIsOpened = true;
        },
    
        onSidebarClosed: function() {
            this.sidebarIsOpened = false;
        }
    }
}).$mount('#app')
