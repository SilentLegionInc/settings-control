<template>
    <div id="app">
        <app-header @onHamburger="onSidebarOpened"></app-header>

        <app-sidebar :isOpen="sidebarIsOpened" @closeSidebar="onSidebarClosed"></app-sidebar>

        <router-view id="app-content"/>

        <app-footer id="app-footer"></app-footer>
    </div>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator';
    import Header from './components/Header.vue';
    import Sidebar from './components/Sidebar.vue';
    import Footer from './components/Footer.vue';
    import Settings from './components/Settings.vue';

    @Component({
        el: '#app',
        components: {
            'app-header': Header,
            'app-sidebar': Sidebar,
            'app-footer': Footer,
            'app-settings': Settings
        },
    })
    export default class App extends Vue {
        private sidebarIsOpened: boolean = false;

        private onSidebarOpened() {
            this.sidebarIsOpened = true;
        }

        private onSidebarClosed() {
            this.sidebarIsOpened = false;
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
    }

    #app-content {
        padding: 10px;
        flex: 1 0 auto;
    }

    #app-footer {
        flex-shrink: 0;
    }
</style>
