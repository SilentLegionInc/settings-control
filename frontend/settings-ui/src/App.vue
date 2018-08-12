<template>
    <div id="app">
        <app-header @onHamburger="onSidebarOpened"></app-header>

        <app-sidebar :isOpen="sidebarIsOpened" @closeSidebar="onSidebarClosed"></app-sidebar>

        <router-view class="content"></router-view>

	    <app-footer></app-footer>
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
    .content {
        padding: 10px !important;
    }
</style>
