<template>
    <div>
        <div class="row margin-top-sm" @click="switchDetailedCore()">
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
        {{core.detail}}
        <div v-if="core.detail" class="row margin-top-sm">
            <div class="col-md-12">
                {{core.name}} DETAILED
                <label>Update by archive
                    <input type="file" id="core_file" ref="core_file" v-on:change="handleFileUpload()"/>
                </label>
                <button v-on:click="submitFile()">Submit</button>
                Hello
            </div>
        </div>
        <div v-for="(module_elem, index) in modules" v-bind:key="index">
            <div class="row margin-top-sm" v-on:click="switchDetailed(index)">
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
            <div v-if="module_elem.detail" class="row margin-top-sm">
                <div class="col-md-12">
                    Module {{module_elem.index}} detailed
                    <!--<label>Update by archive-->
                        <!--<input type="file" :id="index" :ref="index" v-on:change="handleFileUpload()"/>-->
                    <!--</label>-->
                    <!--<button v-on:click="submitFile()">Submit</button>-->
                </div>
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
            modules: [],
            file: null
        }
    },
    watch: {
    },
    async mounted() {
        await this.loadData();
    },
    methods: {
        switchDetailedCore: function() {
            this.core.detail = !this.core.detail;
            console.log('core switched ' + this.core.detail);
        },
        switchDetailed: function(index) {
            console.log(`module ${index} switched`);
            this.modules[index].detail = !this.modules[index].detail;
        },
        loadData: async function() {
            try {
                const answer = await this.$store.state.requestService.getModules();
                this.modules = answer.dependencies;
                this.core = answer.core;
                // this.core.detail = false;
                this.core.active = false;
                this.modules = this.modules.map(moduleElem => {
                    moduleElem.active = false;
                    // moduleElem.detail = false;
                    return moduleElem;
                });
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
        handleFileUpload(event) {
            Logger.info(event);
            this.file = this.$refs.file.files[0];
        },
        async updateCore() {
            const formData = new FormData();
            formData.append('file', this.file);
            try {
                await this.$store.state.requestService.uploadModuleArchive(formData);
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Internal server error');
                    Logger.error(err);
                }
            }
        },
        updateModule() {

        }
    }
}
</script>

<style scoped>

</style>
