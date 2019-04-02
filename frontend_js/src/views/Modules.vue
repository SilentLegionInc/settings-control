<template>
    <div class="container-fluid">

        <div role="tablist">
            <div class="row" style="margin: auto">
                <div class="col-xl-8 offset-xl-2 offset-0 col-12">
                    <b-card no-body class="mb-1">
                        <b-card-header header-tag="header" class="p-1" role="tab">
                            <b-button block href="#" v-b-toggle="'accordion_core'" variant="info">{{core.name}}</b-button>
                        </b-card-header>
                        <b-collapse id="accordion_core" visible accordion="my-accordion" role="tabpanel">
                            <b-card-body>
                                <div class="row mb-1">
                                    <div class="col-xl-3 col-4">
                                        Имя конфига:
                                    </div>
                                    <div class="col-xl-9 col-8">
                                        {{core.configPath || '-'}}
                                    </div>
                                </div>
                                <div class="row mb-1">
                                    <div class="col-xl-3 col-4">
                                        Имя исполняемого:
                                    </div>
                                    <div class="col-xl-9 col-8">
                                        {{core.executeName || '-'}}
                                    </div>
                                </div>
                                <div class="row mb-2">
                                    <div class="col-xl-3 col-4">
                                        Адрес git:
                                    </div>
                                    <div class="col-xl-9 col-8">
                                        {{core.url || '-'}}
                                    </div>
                                </div>
                                <div class="row mb-2">
                                    <div class="col-xl-3 col-4">
                                        Время последней сборки:
                                    </div>
                                    <div class="col-xl-9 col-8">
                                        <span v-if="core.isBuilt">{{core.buildModifyTime | moment("DD.MM.YYYY HH:mm:ss")}}</span>
                                        <span v-else>-</span>
                                    </div>
                                </div>
                                <div class="row mb-2">
                                    <div class="col-xl-3 col-4">
                                        Время последнего пула:
                                    </div>
                                    <div class="col-xl-9 col-8">
                                        <span v-if="core.isCloned">{{core.srcModifyTime | moment("DD.MM.YYYY HH:mm:ss")}}</span>
                                        <span v-else>-</span>
                                    </div>
                                </div>
                                <div class="row mb-3">
                                    <div class="col-xl-3 col-12 mb-1">
                                        <button id="coreUpdateButton"
                                                class="btn btn-block btn-primary"
                                                v-b-toggle="'coreUpdate'"
                                                @click="changeCollapseStatus('coreUpdate')">
                                            Ручное обновление <i class="fa" :class="{'fa-angle-down': !collapseStatuses[`moduleUpdate${index}`],
                                                'fa-angle-up': collapseStatuses[`moduleUpdate${index}`]}"></i>
                                        </button>
                                    </div>
                                    <div class="col-xl-3 col-12 mb-1">
                                        <button class="btn btn-block btn-primary" @click="cloneModule(core.name)">
                                            Обновить
                                        </button>
                                    </div>
                                    <div class="col-xl-3 col-12 mb-1">
                                        <button class="btn btn-block btn-primary" @click="buildModule(core.name)">
                                            Собрать
                                        </button>
                                    </div>
                                    <div class="col-xl-3 col-12 mb-1">
                                        <!--TODO change to normal check-->
                                        <button v-if="!core.isActive" :disabled="!core.isBuilt" class="btn btn-block btn-success" @click="runCore()">
                                            Запустить
                                        </button>
                                        <button v-else class="btn btn-block btn-danger" @click="stopCore()">
                                            Остановить
                                        </button>
                                    </div>
                                </div>
                                <b-collapse id="coreUpdate" ref="coreUpdate">
                                    <div class="row mb-2">
                                        <label class="col-xl-3 col-form-label mb-1" for="core_update">Архив с исходниками для обновления:</label>
                                        <div class="col-xl-9 col-12 mb-1">
                                            <b-form-file
                                                v-model="file"
                                                placeholder="..."
                                                accept=".zip"
                                                drop-placeholder="Перетащите архив сюда"
                                                id="core_update"
                                            />
                                            <p class="card-text" style="font-size: 0.75rem; color: rgba(16,8,13,0.54)">Внутри архива должна быть папка, с именем модуля, например, fomodel</p>
                                        </div>
                                    </div>
                                    <div class="row mb-2">
                                        <div class="offset-xl-9 offset-md-8 offset-0 col-xl-3 col-md-4 col-12">
                                            <button :disabled="!file" class="btn btn-success btn-block" @click="uploadModuleArchive(module_elem.name)">Обновить</button>
                                        </div>
                                    </div>
                                </b-collapse>
                            </b-card-body>
                        </b-collapse>
                    </b-card>
                </div>
            </div>

            <div v-if="modules.length > 0">
                <div v-for="(module_elem, index) of modules" v-bind:key="index">
                    <div class="row" style="margin: auto">
                        <div class="col-xl-8 offset-xl-2 offset-0 col-12">
                            <b-card no-body class="mb-1">
                                <b-card-header header-tag="header" class="p-1" role="tab">
                                    <b-button block href="#" v-b-toggle="'module' + index" variant="info">{{module_elem.name}}</b-button>
                                </b-card-header>
                                <b-collapse :id="'module' + index" accordion="my-accordion" role="tabpanel">
                                    <b-card-body>
                                        <div class="row mb-2">
                                            <div class="col-xl-3 col-4">
                                                Адрес git:
                                            </div>
                                            <div class="col-xl-9 col-8">
                                                {{module_elem.url || '-'}}
                                            </div>
                                        </div>
                                        <!--<vs-divider>Обновление</vs-divider>-->
                                        <div class="row mb-2">
                                            <div class="col-xl-3 col-4">
                                                Время последней сборки:
                                            </div>
                                            <div class="col-xl-9 col-8">
                                                <span v-if="module_elem.isBuilt">{{module_elem.buildModifyTime | moment("DD.MM.YYYY HH:mm:ss")}}</span>
                                                <span v-else>-</span>
                                            </div>
                                        </div>
                                        <div class="row mb-2">
                                            <div class="col-xl-3 col-4">
                                                Время последнего пула:
                                            </div>
                                            <div class="col-xl-9 col-8">
                                                <span v-if="module_elem.isCloned">{{module_elem.srcModifyTime | moment("DD.MM.YYYY HH:mm:ss")}}</span>
                                                <span v-else>-</span>
                                            </div>
                                        </div>
                                        <div class="row mb-3">
                                            <div class="offset-xl-3 offset-0 col-xl-3 col-4">
                                                <button :id="'moduleUpdateButton' + index"
                                                        class="btn btn-block btn-primary"
                                                        v-b-toggle="'moduleUpdate' + index"
                                                        @click="changeCollapseStatus(`moduleUpdate${index}`)">
                                                    Ручное обновление <i class="fa" :class="{'fa-angle-down': !collapseStatuses[`moduleUpdate${index}`],
                                                'fa-angle-up': collapseStatuses[`moduleUpdate${index}`]}"></i>
                                                </button>
                                            </div>
                                            <div class="col-xl-3 col-4">
                                                <button class="btn btn-block btn-primary" @click="cloneModule(module_elem.name)">
                                                    Обновить
                                                </button>
                                            </div>
                                            <div class="col-xl-3 col-4">
                                                <button class="btn btn-block btn-primary" @click="buildModule(module_elem.name)">
                                                    Собрать
                                                </button>
                                            </div>
                                        </div>
                                        <b-collapse :id="'moduleUpdate' + index" :ref="'moduleUpdate' + index">
                                            <div class="row mb-1">
                                                <label class="col-xl-3 col-form-label mb-1" :for="'module'+index+'update'">Архив с исходниками для обновления:</label>
                                                <div class="col-xl-9 col-12 mb-1">
                                                    <b-form-file
                                                        v-model="file"
                                                        placeholder="..."
                                                        accept=".zip"
                                                        drop-placeholder="Перетащите архив сюда"
                                                        :id="'module'+index+'update'"
                                                    />
                                                    <p class="card-text" style="font-size: 0.75rem; color: rgba(16,8,13,0.54)">Внутри архива должна быть папка, с именем модуля, например, fomodel</p>
                                                </div>
                                            </div>
                                            <div class="row mb-2">
                                                <div class="offset-xl-9 offset-md-8 offset-0 col-xl-3 col-md-4 col-12">
                                                    <button :disabled="!file" class="btn btn-success btn-block" @click="uploadModuleArchive(module_elem.name)">Обновить</button>
                                                </div>
                                            </div>
                                        </b-collapse>
                                    </b-card-body>
                                </b-collapse>
                            </b-card>
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
            file: null,
            collapseStatuses: {},
            _loader: null
        }
    },
    async mounted() {
        await this.loadData();
    },
    methods: {
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
            this.file = null;
        },
        // TODO may be pass index\object to not loadData(), may be add status instead of is_built, is_cloned
        //  to change color while build/clone in process
        async cloneModule(moduleName) {
            try {
                this._loader = this.$loading.show();
                await this.$store.state.requestService.cloneModule(moduleName);
                await this.loadData();
                this.$toaster.success(`Модуль ${moduleName} успешно обновлен`);
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
        },

        async runCore() {
            try {
                if (!this.core.isBuilt) {
                    this.$toaster.warning('Необходимо собрать ядро для его запуска');
                    return;
                }
                this._loader = this.$loading.show();
                const res = await this.$store.state.requestService.runCore();
                await this.loadData();
                if (res) {
                    this.$toaster.success('Ядро запущено');
                } else {
                    this.$toaster.error('Не удалось запустить ядро');
                }
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

        async stopCore() {
            try {
                this._loader = this.$loading.show();
                const res = await this.$store.state.requestService.stopCore();
                await this.loadData();
                if (res) {
                    this.$toaster.success('Ядро остановлено');
                } else {
                    this.$toaster.error('Не удалось остановить ядро');
                }
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

        changeCollapseStatus(collapseId) {
            if (this.collapseStatuses[collapseId]) {
                this.collapseStatuses[collapseId] = !this.collapseStatuses[collapseId]
            } else {
                this.$set(this.collapseStatuses, collapseId, true);
            }
        }
    }
}
</script>

<style scoped>

</style>
