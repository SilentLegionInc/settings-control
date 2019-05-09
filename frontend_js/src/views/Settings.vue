<template>
    <div class="container-fluid">
        <div class="row mb-3" style="margin: auto">
            <div class="col-12"  align="center">
                <h2>Конфигурация ядра</h2>
            </div>
        </div>
        <div v-if="settings">
            <!--<div v-if="!rawMode" class="mb-2">-->
                <!--<div class="row form-group" v-for="(_, settingKey) in settings" v-bind:key="settingKey">-->
                    <!--<label class="offset-xl-2 col-xl-3 col-form-label col-12" :for="settingKey">{{settingKey}}</label>-->
                    <!--<div class="col-xl-5 col-12">-->
                        <!--<input class="form-control" type="text" :id="settingKey" v-model="settings[settingKey]"-->
                               <!--:placeholder="settingKey"/>-->
                    <!--</div>-->
                <!--</div>-->
            <!--</div>-->
            <div class="mb-2">
                <div class="row" style="margin: auto">
                    <vue-json-editor class="offset-xl-1 col-xl-10 offset-lg-1 col-lg-10 offset-0 col-12" v-model="settings" :show-btns="false"></vue-json-editor>
                </div>
            </div>
            <div class="row" style="margin: auto">
                <div class="col-xl-3 offset-xl-5 col-lg-3 offset-lg-5 col-sm-6 offset-0 col-12 mb-1">
                    <!--<button class="btn btn-default" @click="rawMode = !rawMode">-->
                        <!--Change mode-->
                    <!--</button>-->
                    <button class="btn btn-danger btn-block" @click="ResetConfig()">
                        Сбросить
                    </button>
                </div>
                <div class="col-xl-3 col-lg-3 col-sm-6 col-12">
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
                this.settings = await this.$store.state.requestService.getCoreConfig();
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
                    this.$toaster.error('Серверная ошибка');
                    Logger.error(err)
                }
                this.settings = {}
            }
            this._loader.hide();
        },

        UpdateConfig: async function () {
            try {
                this._loader = this.$loading.show();
                Logger.info('Setting config: ' + JSON.stringify(this.settings, null, 2));
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
