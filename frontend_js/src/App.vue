<template>
    <div id="app">
        <app-header @onHamburger="onSidebarOpened"></app-header>

        <app-sidebar :isOpen="sidebarIsOpened" @closeSidebar="onSidebarClosed"></app-sidebar>

        <router-view id="app-content"/>

        <app-footer id="app-footer"></app-footer>
    </div>
</template>

<script>
import Header from './components/Header.vue';
import Sidebar from './components/Sidebar.vue';
import Footer from './components/Footer.vue';
import axios from 'axios';

export default {
    name: 'App',
    components: {
        'app-header': Header,
        'app-sidebar': Sidebar,
        'app-footer': Footer
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
    },
    created: function () {
        const authToken = this.$cookies.get('toolBeltAuthToken');
        if (authToken) {
            this.$store.commit('setAuthToken', authToken);
        }
        // TODO check that is work as expected.
        axios.interceptors.response.use(undefined, function (err) {
            return new Promise(function (resolve, reject) {
                if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
                    // if you ever get an unauthorized, logout the user
                    this.$store.dispatch('deauthorize');
                    this.$toaster.error('You an unauthorize');
                    this.$router.push('/');
                    // you can also redirect to /login if needed !
                }
                throw err;
            });
        });
    }
}
</script>

<style lang="scss">
    html, body {
        height: 100%;
    }

    #app {
        display: flex;
        flex-direction: column;
        height: 100%;
        font-family: Apercu, serif;
    }

    #app-content {
        padding: 10px;
        margin: 0;
        flex: 1 0 auto;
        background: #E8EBEA;
    }

    #app-footer {
        flex-shrink: 0;
    }
</style>
