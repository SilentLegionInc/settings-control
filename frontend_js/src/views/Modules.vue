<template>
    <div class="container-fluid">

        <div role="tablist">
            <div class="row">
                <div class="col-xl-8 offset-xl-2 offset-0 col-12">
                    <b-card no-body class="mb-1">
                        <b-card-header header-tag="header" class="p-1" role="tab">
                            <!--<div v-b-toggle.accordion_core><p class="card-text">{{core.name}}</p></div>-->
                            <b-button block href="#" v-b-toggle.accordion_core variant="info">{{core.name}}</b-button>
                        </b-card-header>
                        <b-collapse id="accordion_core" visible accordion="my-accordion" role="tabpanel">
                            <b-card-body>
                                <div class="row mb-1">
                                    <div class="col-xl-3 col-4">
                                        Имя конфига:
                                    </div>
                                    <div class="col-xl-9 col-8">
                                        {{core.configPath}}
                                    </div>
                                </div>
                                <div class="row mb-1">
                                    <div class="col-xl-3 col-4">
                                        Имя исполняемого:
                                    </div>
                                    <div class="col-xl-9 col-6">
                                        {{core.executeName}}
                                    </div>
                                </div>
                                <div class="row mb-2">
                                    <div class="col-xl-3 col-6">
                                        Адрес git:
                                    </div>
                                    <div class="col-xl-9 col-6">
                                        {{core.url}}
                                    </div>
                                </div>
                                <!--<vs-divider>Обновление</vs-divider>-->
                                <div class="row mb-2">
                                    <label class="col-xl-3 col-form-label mb-1" for="core_update">Архив с исходниками для обновления:</label>
                                    <div class="col-xl-9 col-12 mb-1">
                                        <b-form-file
                                            v-model="file"
                                            placeholder="Архив с исходниками для обновления"
                                            accept=".zip"
                                            drop-placeholder="Перетащите архив сюда"
                                            id="core_update"
                                        />
                                    </div>
                                </div>
                            </b-card-body>
                        </b-collapse>
                    </b-card>
                </div>
            </div>

            <div v-if="modules.length > 0">
                <div v-for="(module_elem, index) of modules" v-bind:key="index">
                    <div class="row">
                        <div class="col-xl-8 offset-xl-2 offset-0 col-12">
                            <b-card no-body class="mb-1">
                                <b-card-header header-tag="header" class="p-1" role="tab">
                                    <b-button block href="#" v-b-toggle="'module' + index" variant="info">{{module_elem.name}}</b-button>
                                </b-card-header>
                                <b-collapse :id="'module' + index" accordion="my-accordion" role="tabpanel">
                                    <b-card-body>
                                        <p class="card-text">{{module_elem.url}}</p>
                                        <!--<vs-divider>Обновление</vs-divider>-->
                                        <div class="row mb-2">
                                            <label class="col-xl-3 col-form-label mb-1" :for="'module'+0+'update'">Архив с исходниками для обновления:</label>
                                            <div class="col-xl-9 col-12 mb-1">
                                                <b-form-file
                                                    v-model="file"
                                                    placeholder="Архив с исходниками для обновления"
                                                    accept=".zip"
                                                    drop-placeholder="Перетащите архив сюда"
                                                    :id="'module'+index+'update'"
                                                />
                                            </div>
                                        </div>
                                    </b-card-body>
                                </b-collapse>
                            </b-card>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!--<div class="row mb-2">-->
            <!--&lt;!&ndash;col-md-2 offset-md-2 col-sm-3 offset-sm-0 &ndash;&gt;-->
            <!--<div class="offset-md-2 col-2" @click="switchDetailedCore()">-->
                <!--{{core.name}}-->
            <!--</div>-->
            <!--&lt;!&ndash;col-md-5 col-sm-7&ndash;&gt;-->
            <!--<div class="col-md-4 col-0" align="right" @click="switchDetailedCore()">-->
                <!--{{core.url}}-->
            <!--</div>-->
            <!--&lt;!&ndash;col-md-1 col-sm-2 &ndash;&gt;-->
            <!--<div class="col-2" align="right">-->
                <!--&lt;!&ndash;TODO onclick download/build?&ndash;&gt;-->
                <!--<i class="fa fa-box-open"-->
                    <!--:style="{color: core.isBuilt ? 'green': 'red'}"-->
                    <!--@click="buildModule(core.name)"-->
                <!--&gt;</i>&nbsp;-->
                <!--<i class="fa fa-download"-->
                   <!--:style="{color: core.isCloned ? 'green': 'red'}"-->
                   <!--@click="cloneModule(core.name)"-->
                <!--&gt;</i>-->
            <!--</div>-->
        <!--</div>-->
        <!--<div v-if="core.detail" class="mb-2">-->
            <!--<div class="row mb-2">-->
                <!--<div class="col-6 offset-md-2 col-md-4">-->
                    <!--Имя файла конфигурации:-->
                <!--</div>-->
                <!--<div class="col-6 col-md-4" align="right">-->
                    <!--{{core.configPath}}-->
                <!--</div>-->
            <!--</div>-->
            <!--<div class="row mb-2">-->
                <!--<div class="col-md-8 offset-md-2">-->
                    <!--<b-form-file-->
                        <!--v-model="file"-->
                        <!--placeholder="Архив с исходниками для обновления"-->
                        <!--accept=".zip"-->
                        <!--drop-placeholder="Перетащите архив сюда"-->
                    <!--/>-->
                <!--</div>-->
            <!--</div>-->
            <!--<div class="row">-->
                <!--<div class="offset-md-2 col-md-8" align="right">-->
                    <!--<button class="btn btn-success" @click="uploadModuleArchive(core.name)">-->
                        <!--Обновить-->
                    <!--</button>-->
                <!--</div>-->
            <!--</div>-->
        <!--</div>-->
        <!--<div v-if="modules.length > 0">-->
            <!--<div v-for="(module_elem, index) of modules" v-bind:key="index">-->
                <!--<div class="row mb-2">-->
                    <!--<div class="col-md-3 offset-md-2" v-on:click="switchDetailed(index)">-->
                        <!--{{module_elem.name}}-->
                    <!--</div>-->
                    <!--<div class="col-md-4" v-on:click="switchDetailed(index)">-->
                        <!--{{module_elem.url}}-->
                    <!--</div>-->
                    <!--<div class="col-md-1" align="right">-->
                        <!--<i class="fa fa-box-open"-->
                            <!--:style="{color: module_elem.isBuilt ? 'green': 'red'}"-->
                            <!--@click="buildModule(module_elem.name)"-->
                        <!--&gt;</i>&nbsp;-->
                        <!--<i class="fa fa-download"-->
                            <!--:style="{color: module_elem.isCloned ? 'green': 'red'}"-->
                            <!--@click="cloneModule(module_elem.name)"-->
                        <!--&gt;</i>-->
                    <!--</div>-->
                <!--</div>-->
                <!--<div v-if="module_elem.detail" class="mb-2">-->
                    <!--<div class="row mb-2">-->
                        <!--<div class="col-md-8 offset-md-2">-->
                            <!--<b-form-file-->
                                <!--v-model="file"-->
                                <!--placeholder="Архив с исходниками для обновления"-->
                                <!--accept=".zip"-->
                                <!--drop-placeholder="Перетащите архив сюда"-->
                            <!--/>-->
                        <!--</div>-->
                    <!--</div>-->
                    <!--<div class="row">-->
                        <!--<div class="offset-md-2 col-md-8" align="right">-->
                            <!--<button class="btn btn-success" @click="uploadModuleArchive(module_elem.name)">-->
                                <!--Обновить-->
                            <!--</button>-->
                        <!--</div>-->
                    <!--</div>-->
                <!--</div>-->
            <!--</div>-->
        <!--</div>-->
    </div>
</template>

<script>
import { ServerExceptionModel } from '../models/ServerExceptionModel';
import Logger from '../logger';

export default {
    name: 'Modules',
    data: () => {
        return {
            core: {},
            modules: [],
            file: null,
            _loader: null
        }
    },
    async mounted() {
        await this.loadData();
    },
    methods: {
        switchDetailedCore() {
            this.core.detail = !this.core.detail;
        },
        switchDetailed(index) {
            this.modules[index].detail = !this.modules[index].detail;
        },
        async loadData() {
            const loader = this.$loading.show();
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
                    this.$toaster.error('Серверная ошибка');
                    Logger.error(err);
                }
                this.modules = [];
                this.core = {}
            }
            loader.hide();
        },
        async uploadModuleArchive(moduleName) {
            const formData = new FormData();
            formData.append('file', this.file);
            try {
                this._loader = this.$loading.show();
                await this.$store.state.requestService.uploadModuleArchive(formData, moduleName);
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Серверная ошибка');
                    Logger.error(err);
                }
            }
            this._loader.hide();
            delete this.file;
        },
        // TODO may be pass index\object to not loadData(), may be add status instead of is_built, is_cloned
        //  to change color while build/clone in process
        async cloneModule(moduleName) {
            try {
                this._loader = this.$loading.show();
                await this.$store.state.requestService.cloneModule(moduleName);
                await this.loadData();
                this.$toaster.success(`Модуль ${moduleName} успешно склонирован`);
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Серверная ошибка');
                    Logger.error(err);
                }
            }
            this._loader.hide();
        },
        async buildModule(moduleName) {
            try {
                this._loader = this.$loading.show();
                await this.$store.state.requestService.buildModule(moduleName);
                await this.loadData();
                this.$toaster.success(`Модуль ${moduleName} успешно собран`);
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Серверная ошибка');
                    Logger.error(err);
                }
            }
            this._loader.hide();
        }
    }
}
</script>

<style scoped>

</style>
