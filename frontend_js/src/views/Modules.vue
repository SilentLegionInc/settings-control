<template>
    <div class="container-fluid">
        <h2 class="mb-3" align="center">Список модулей {{$store.state.robotName}}</h2>
        <div role="tablist">
            <div class="row" style="margin: auto">
                <div class="col-xl-8 offset-xl-2 offset-lg-1 col-lg-10 offset-md-0 col-md-12 offset-0 col-12">
                    <b-card no-body>
                        <b-card-header header-tag="header" class="p-1" role="tab">
                            <b-button block href="#" v-b-toggle="'accordion_core'" variant="info">{{core.name}}</b-button>
                        </b-card-header>
                        <b-collapse id="accordion_core" visible accordion="my-accordion" role="tabpanel">
                            <b-card-body class="pt-2 pb-0">
                                <div class="row mb-1">
                                    <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12 col-12 mb-1">
                                        <b>Имя конфига:</b>
                                    </div>
                                    <div class="col-xl-8 col-lg-8 col-md-8 col-sm-12 col-12">
                                        <span class="ml-1">{{core.configPath || '-'}}</span>
                                    </div>
                                </div>
                                <div class="row mb-1">
                                    <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12 col-12 mb-1">
                                        <b>Имя исполняемого:</b>
                                    </div>
                                    <div class="col-xl-8 col-lg-8 col-md-8 col-sm-12 col-12">
                                        <span class="ml-1">{{core.executeName || '-'}}</span>
                                    </div>
                                </div>
                                <div class="row mb-2">
                                    <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12 col-12 mb-1">
                                        <b>Адрес git:</b>
                                    </div>
                                    <div class="col-xl-8 col-lg-8 col-md-8 col-sm-12 col-12">
                                        <span class="ml-1">{{core.url || '-'}}</span>
                                    </div>
                                </div>
                                <div class="row mb-2">
                                    <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12 col-12 mb-1">
                                        <b>Время последней сборки:</b>
                                    </div>
                                    <div class="col-xl-8 col-lg-8 col-md-8 col-sm-12 col-12">
                                        <span v-if="core.isBuilt" class="ml-1">{{core.buildModifyTime | moment("DD.MM.YYYY HH:mm:ss")}}</span>
                                        <span v-else class="ml-1">Не был собран</span>
                                    </div>
                                </div>
                                <div class="row mb-2">
                                    <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12 col-12 mb-1">
                                        <b>Время последнего пула:</b>
                                    </div>
                                    <div class="col-xl-8 col-lg-8 col-md-8 col-sm-12 col-12">
                                        <span v-if="core.isCloned" class="ml-1">{{core.srcModifyTime | moment("DD.MM.YYYY HH:mm:ss")}}</span>
                                        <span v-else class="ml-1">Не был склонирован</span>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12 col-12 mb-1">
                                        <button v-if="!core.isActive" :disabled="!core.isBuilt" class="btn btn-block btn-success" @click="runCore()">
                                            Запустить
                                        </button>
                                        <button v-else class="btn btn-block btn-danger" @click="stopCore()">
                                            Остановить
                                        </button>
                                    </div>
                                    <div class="col-xl-4 col-lg-4 col-md-4 col-sm-6 col-12 mb-1">
                                        <button class="btn btn-block btn-primary" @click="buildModule(core.name)">
                                            Собрать
                                        </button>
                                    </div>
                                    <div class="col-xl-4 col-lg-4 col-md-4 col-sm-6 col-12 mb-1">
                                        <button class="btn btn-block btn-primary" @click="buildMachine()">
                                            Собрать всё
                                        </button>
                                    </div>
                                </div>
                                <div class="row mb-2">
                                    <div class="col-xl-4 col-lg-4 col-md-4 col-sm-6 col-12 mb-1">
                                        <button class="btn btn-block btn-primary" @click="cloneModule(core.name)">
                                            Обновить
                                        </button>
                                    </div>
                                    <div class="col-xl-4 col-lg-4 col-md-4 col-sm-6 col-12 mb-1">
                                        <button class="btn btn-block btn-primary" @click="cloneMachine()">
                                            Обновить все
                                        </button>
                                    </div>
                                    <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12 col-12 mb-1">
                                        <button id="coreUpdateButton"
                                                class="btn btn-block btn-primary"
                                                v-b-toggle="'coreUpdate'"
                                                @click="changeCollapseStatus('coreUpdate')">
                                            Ручное обновление
                                            <i class="fa"
                                               :class="{'fa-angle-down': !collapseStatuses[`coreUpdate`],
                                                'fa-angle-up': collapseStatuses[`coreUpdate`]}"
                                            ></i>
                                        </button>
                                    </div>

                                </div>
                                <b-collapse id="coreUpdate" ref="coreUpdate">
                                    <div class="row mb-2">
                                        <label class="col-xl-12 col-lg-12 col-form-label mb-1" for="core_update">
                                            <b>Архив с исходниками для обновления:</b>
                                        </label>
                                        <div class="col-xl-12 col-lg-12 col-12 mb-1">
                                            <b-form-file
                                                v-model="file"
                                                placeholder="..."
                                                accept=".zip"
                                                drop-placeholder="Перетащите архив сюда"
                                                id="core_update"
                                            />
                                            <p class="card-text ml-1" style="font-size: 0.75rem; color: rgba(16,8,13,0.54)">Внутри архива должна быть папка, с именем модуля, например, fomodel</p>
                                        </div>
                                    </div>
                                    <div class="row mb-2">
                                        <div class="offset-xl-8 offset-lg-8 offset-md-8 offset-sm-6 offset-0 col-xl-4 col-lg-4 col-md-4 col-sm-6 col-12">
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
                        <div class="col-xl-8 offset-xl-2 offset-lg-1 col-lg-10 offset-md-0 col-md-12 offset-0 col-12">
                            <b-card no-body>
                                <b-card-header header-tag="header" class="p-1" role="tab">
                                    <b-button block href="#" v-b-toggle="'module' + index" variant="info">{{module_elem.name}}</b-button>
                                </b-card-header>
                                <b-collapse :id="'module' + index" accordion="my-accordion" role="tabpanel">
                                    <b-card-body class="pt-2 pb-0">
                                        <div class="row mb-2">
                                            <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12 col-12 mb-1">
                                                <b>Адрес git:</b>
                                            </div>
                                            <div class="col-xl-8 col-lg-8 col-md-8 col-sm-12 col-12">
                                                <span class="ml-1">{{module_elem.url || '-'}}</span>
                                            </div>
                                        </div>
                                        <!--<vs-divider>Обновление</vs-divider>-->
                                        <div class="row mb-2">
                                            <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12 col-12 mb-1">
                                                <b>Время последней сборки:</b>
                                            </div>
                                            <div class="col-xl-8 col-lg-8 col-md-8 col-sm-12 col-12">
                                                <span v-if="module_elem.isBuilt" class="ml-1">{{module_elem.buildModifyTime | moment("DD.MM.YYYY HH:mm:ss")}}</span>
                                                <span v-else class="ml-1">Не был собран</span>
                                            </div>
                                        </div>
                                        <div class="row mb-2">
                                            <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12 col-12 mb-1">
                                                <b>Время последнего пула:</b>
                                            </div>
                                            <div class="col-xl-8 col-lg-8 col-md-8 col-sm-12 col-12">
                                                <span v-if="module_elem.isCloned" class="ml-1">{{module_elem.srcModifyTime | moment("DD.MM.YYYY HH:mm:ss")}}</span>
                                                <span v-else class="ml-1">Не был склонирован</span>
                                            </div>
                                        </div>
                                        <div class="row mb-2">
                                            <div class="col-xl-4 col-lg-4 col-md-4 col-sm-6 col-12 mb-1">
                                                <button class="btn btn-block btn-primary" @click="buildModule(module_elem.name)">
                                                    Собрать
                                                </button>
                                            </div>
                                            <div class="col-xl-4 col-lg-4 col-md-4 col-sm-6 col-12 mb-1">
                                                <button class="btn btn-block btn-primary" @click="cloneModule(module_elem.name)">
                                                    Обновить
                                                </button>
                                            </div>
                                            <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12 col-12 mb-1">
                                                <button :id="'moduleUpdateButton' + index"
                                                        class="btn btn-block btn-primary"
                                                        v-b-toggle="'moduleUpdate' + index"
                                                        @click="changeCollapseStatus(`moduleUpdate${index}`)">
                                                    Ручное обновление <i class="fa" :class="{'fa-angle-down': !collapseStatuses[`moduleUpdate${index}`],
                                                'fa-angle-up': collapseStatuses[`moduleUpdate${index}`]}"></i>
                                                </button>
                                            </div>
                                        </div>
                                        <b-collapse :id="'moduleUpdate' + index" :ref="'moduleUpdate' + index">
                                            <div class="row mb-1">
                                                <label class="col-xl-12 col-lg-12 col-12 col-form-label mb-1" :for="'module'+index+'update'">
                                                    <b>Архив с исходниками для обновления:</b>
                                                </label>
                                                <div class="col-xl-12 col-lg-12 col-12 mb-1">
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
                                                <div class="offset-xl-8 offset-lg-8 offset-md-8 offset-sm-6 offset-0 col-xl-4 col-lg-4 col-md-4 col-sm-6 col-12">
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

        async cloneMachine() {
            try {
                this._loader = this.$loading.show();
                await this.$store.state.requestService.cloneMachine();
                await this.loadData();
                this.$toaster.success(`Текущая конфигурация была успешно обновлена`);
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

        async buildMachine() {
            try {
                this._loader = this.$loading.show();
                await this.$store.state.requestService.buildMachine();
                await this.loadData();
                this.$toaster.success(`Текущая конфигурация была успешно собрана`);
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
