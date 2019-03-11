<template>
    <div class="container-fluid">
        <div class="row margin-bottom-sm">
            <!--col-md-2 offset-md-2 col-sm-3 offset-sm-0 -->
            <div class="offset-md-2 col-2" @click="switchDetailedCore()">
                {{core.name}}
            </div>
            <!--col-md-5 col-sm-7-->
            <div class="col-md-4 col-0" align="right" @click="switchDetailedCore()">
                {{core.url}}
            </div>
            <!--col-md-1 col-sm-2 -->
            <div class="col-2" align="right">
                <!--TODO onclick download/build?-->
                <i class="fa fa-box-open"
                    :style="{color: core.isBuilt ? 'green': 'red'}"
                    @click="buildModule(core.name)"
                ></i>&nbsp;
                <i class="fa fa-download"
                   :style="{color: core.isCloned ? 'green': 'red'}"
                   @click="cloneModule(core.name)"
                ></i>
            </div>
        </div>
        <div v-if="core.detail" class="margin-bottom-sm">
            <div class="row margin-bottom-sm">
                <div class="col-6 offset-md-2 col-md-4">
                    Имя файла конфигурации:
                </div>
                <div class="col-6 col-md-4" align="right">
                    {{core.configPath}}
                </div>
            </div>
            <div class="row margin-bottom-sm">
                <div class="col-md-8 offset-md-2">
                    <b-form-file
                        v-model="file"
                        placeholder="Архив с исходниками для обновления"
                        accept=".zip"
                        drop-placeholder="Перетащите архив сюда"
                    />
                </div>
            </div>
            <div class="row">
                <div class="offset-md-2 col-md-8" align="right">
                    <button class="btn btn-success" @click="uploadModuleArchive(core.name)">
                        Обновить
                    </button>
                </div>
            </div>
        </div>
        <div v-if="modules.length > 0">
            <div v-for="(module_elem, index) of modules" v-bind:key="index">
                <div class="row margin-bottom-sm">
                    <div class="col-md-3 offset-md-2" v-on:click="switchDetailed(index)">
                        {{module_elem.name}}
                    </div>
                    <div class="col-md-4" v-on:click="switchDetailed(index)">
                        {{module_elem.url}}
                    </div>
                    <div class="col-md-1" align="right">
                        <i class="fa fa-box-open"
                            :style="{color: module_elem.isBuilt ? 'green': 'red'}"
                            @click="buildModule(module_elem.name)"
                        ></i>&nbsp;
                        <i class="fa fa-download"
                            :style="{color: module_elem.isCloned ? 'green': 'red'}"
                            @click="cloneModule(module_elem.name)"
                        ></i>
                    </div>
                </div>
                <div v-if="module_elem.detail" class="margin-bottom-sm">
                    <div class="row margin-bottom-sm">
                        <div class="col-md-8 offset-md-2">
                            <b-form-file
                                v-model="file"
                                placeholder="Архив с исходниками для обновления"
                                accept=".zip"
                                drop-placeholder="Перетащите архив сюда"
                            />
                        </div>
                    </div>
                    <div class="row">
                        <div class="offset-md-2 col-md-8" align="right">
                            <button class="btn btn-success" @click="uploadModuleArchive(module_elem.name)">
                                Обновить
                            </button>
                        </div>
                    </div>
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
    data: () => {
        return {
            core: {},
            modules: [],
            file: null
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
        },
        async uploadModuleArchive(moduleName) {
            const formData = new FormData();
            formData.append('file', this.file);
            try {
                await this.$store.state.requestService.uploadModuleArchive(formData, moduleName);
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Серверная ошибка');
                    Logger.error(err);
                }
            }
            delete this.file;
        },
        // TODO may be pass index\object to not loadData(), may be add status instead of is_built, is_cloned
        //  to change color while build/clone in process
        async cloneModule(moduleName) {
            try {
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
        },
        async buildModule(moduleName) {
            try {
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
        }
    }
}
</script>

<style scoped>

</style>
