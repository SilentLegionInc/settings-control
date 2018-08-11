<template>
    <div id="app">
        <app-header></app-header>

        <div class="row" style="width: 100%">
            <div class="col-md-2">
                <app-sidebar></app-sidebar>
            </div>

            <div class="content col-md-10">
                <router-view/>
            </div>
        </div>

	    <app-footer></app-footer>
    </div>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator';
    import Header from './components/Header.vue';
    import Sidebar from './components/Sidebar.vue';
    import Footer from './components/Footer.vue';

    @Component({
        el: '#app',
        components: {
            'app-header': Header,
            'app-sidebar': Sidebar,
	        'app-footer': Footer,
        },
    })
    export default class App extends Vue {
    }
</script>

<style lang="scss">
    .content {
        padding: 10px !important;
    }
</style>
