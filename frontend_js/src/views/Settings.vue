<template>
    <div>
        <div class="mb-3">
            <h2 align="center">Конфигурация ядра</h2>
        </div>
        <div v-if="settings">
            <div v-if="!rawMode" class="mb-2">
                <div class="row form-group" v-for="(_, settingKey) in settings" v-bind:key="settingKey">
                    <label class="offset-xl-2 col-xl-3 col-form-label col-12" :for="settingKey">{{settingKey}}</label>
                    <div class="col-xl-5 col-12">
                        <input class="form-control" type="text" :id="settingKey" v-model="settings[settingKey]"
                               :placeholder="settingKey"/>
                    </div>
                </div>
            </div>
            <div v-else class="mb-2">
                <div class="row">
                    <vue-json-editor class="offset-xl-2 col-xl-8 offset-0 col-12" v-model="settings" :show-btns="false"></vue-json-editor>
                </div>
            </div>
            <div class="row">
                <div class="col-xl-3 offset-xl-4 col-sm-6 offset-0 col-12 mb-2">
                    <!--<button class="btn btn-default" @click="rawMode = !rawMode">-->
                        <!--Change mode-->
                    <!--</button>-->
                    <button class="btn btn-danger btn-block" @click="ResetConfig()">
                        Сбросить
                    </button>
                </div>
                <div class="col-xl-3 col-12 col-sm-6">
                    <button class="btn btn-success btn-block" @click="UpdateConfig()">
                        Обновить
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ServerExceptionModel } from '../models/ServerExceptionModel'
import Logger from '../logger'
import VueJsonEditor from 'vue-json-editor'

export default {
    name: 'Settings',
    mounted: function () {
        if (this.$store.getters.isAuthenticated) {
            this.loadData()
        } else {
            this.$toaster.error('Для доступа к этой странице необходима авторизация');
            this.$router.push('/login');
        }
    },
    methods: {
        // TODO Add machine type to response. Create basic DTO?
        loadData: async function () {
            try {
                this._loader = this.$loading.show();
                this.settings = await this.$store.state.requestService.getCoreConfig()
                for (const key in this.settings) {
                    if (this.settings.hasOwnProperty(key)) {
                        const value = this.settings[key];
                        if (value instanceof Object || value instanceof Array) {
                            this.rawMode = true;
                            Logger.info('Forced raw mode enabled');
                            break;
                        }
                    }
                }
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message)
                } else {
                    this.$toaster.error('Серверная ошибка')
                    Logger.error(err)
                }
                this.settings = {}
            }
            this._loader.hide();
        },

        UpdateConfig: async function () {
            try {
                this._loader = this.$loading.show();
                const result = await this.$store.state.requestService.setCoreConfig(this.settings);
                if (result) {
                    this.$toaster.success('Успешно обновлено');
                } else {
                    this.$toaster.warn('Deprecated. Check backend code');
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

        ResetConfig: async function () {
            await this.loadData()
        }
    },
    components: {
        VueJsonEditor
    },
    data: () => {
        return {
            settings: {},
            rawMode: true,
            _loader: null
        }
    }
}
</script>

<style scoped lang="scss">
</style>
