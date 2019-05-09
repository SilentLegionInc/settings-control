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
    async beforeCreate() {
        axios.interceptors.response.use((res) => res, (err) => {
            if (err.response != null) {
                if (err.response.status === 401) {
                    // if you ever get an unauthorized, logout the user
                    this.$store.commit('deleteAuthToken');
                    // this.$toaster.error(err.response.data.errorInfo);
                    this.$router.push('/login');
                } else {
                    // this.$toaster.error('Что-то страшное: ' + err.response.data.errorInfo)
                }
                return err.response;
            } else {
                return {
                    data: {
                        errorInfo: 'Неизвестная ошибка клиента'
                    },
                    status: 418
                };
            }
        });
        await this.$store.dispatch('initUrl');
        if (!this.$store.state.url) {
            this.$router.push('/');
        }
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
