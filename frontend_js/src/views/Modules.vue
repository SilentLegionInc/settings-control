<template>
    <div>
        <div class="row">
            <div class="col-md-4 offset-md-2">
                {{core.name}}
            </div>
            <div class="col-md-4">
                {{core.url}}
            </div>
            <div class="col-md-2">
                <!--TODO onclick download/build?-->
                <i class="fa fa-box-open" :style="{color: core.is_built ? 'green': 'red'}"></i>&nbsp;
                <i class="fa fa-download" :style="{color: core.is_cloned ? 'green': 'red'}"></i>
            </div>
        </div>
        <div class="row" v-for="(module_elem, index) in modules" :key="index">
            <div class="offset-md-2 col-md-1">
                {{module_elem.index}}
            </div>
            <div class="col-md-3">
                {{module_elem.name}}
            </div>
            <div class="col-md-4">
                {{module_elem.url}}
            </div>
            <div class="col-md-2">
                <!--TODO onclick download/build?-->
                <i class="fa fa-box-open" :style="{color: module_elem.is_built ? 'green': 'red'}"></i>&nbsp;
                <i class="fa fa-download" :style="{color: module_elem.is_cloned ? 'green': 'red'}"></i>
            </div>
        </div>
    </div>
</template>

<script>
import { ServerExceptionModel } from '../models/ServerExceptionModel';
import Logger from '../logger';

export default {
    name: 'Modules',
    data() {
        return {
            core: {},
            modules: []
        }
    },
    async mounted() {
        await this.loadData();
    },
    methods: {
        loadData: async function() {
            try {
                const answer = await this.$store.state.requestService.getModules();
                this.modules = answer.dependencies;
                this.core = answer.core;
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Internal server error');
                    Logger.error(err);
                }
                this.modules = [];
                this.core = {}
            }
        },
        updateModule() {

        }
    }
}
</script>

<style scoped>

</style>
