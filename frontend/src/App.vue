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
    import LineChart from './services/LineChart';

    @Component({
        el: '#app',
        components: {
            'app-header': Header,
            'app-sidebar': Sidebar,
            'app-footer': Footer,
            'app-settings': Settings,
            'app-line-chart': LineChart
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
        font-family: Apercu, serif;
    }

    #app-content {
        padding: 10px;
        margin: 0;
        flex: 1 0 auto;
        background: #9FB9CF;
    }

    #app-footer {
        flex-shrink: 0;
    }
</style>
