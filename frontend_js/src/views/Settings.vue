<template>
    <div>
        <div class="mb-3">
            <h2 align="center">Конфигурация ядра</h2>
        </div>
        <div v-if="settings">

            <div v-if="!rawMode" class="margin-bottom-sm">
                <div class="row form-group" v-for="(_, settingKey) in settings" v-bind:key="settingKey">
                    <label class="offset-md-2 col-md-3 col-form-label" :for="settingKey">{{settingKey}}</label>
                    <div class="col-md-5">
                        <input class="form-control" type="text" :id="settingKey" v-model="settings[settingKey]"
                               :placeholder="settingKey"/>
                    </div>
                </div>
            </div>
            <div v-else class="margin-bottom-sm">
                <div class="row">
                    <vue-json-editor class="offset-md-2 col-md-8" v-model="settings" :show-btns="false"></vue-json-editor>
                </div>
            </div>
            <div class="row form-group">
                <div class="col-md-6 offset-md-4" align="right">
                    <!--<button class="btn btn-default" @click="rawMode = !rawMode">-->
                        <!--Change mode-->
                    <!--</button>-->
                    <button class="btn btn-danger" @click="ResetConfig()">
                        Reset
                    </button>
                    <button class="ml-3 btn btn-success" @click="UpdateConfig()">
                        Update
                    </button>
                </div>
            </div>
        </div>

        <app-login-modal @logged="loadData"></app-login-modal>

    </div>
</template>

<script>
import LoginModal from '@/components/LoginModal'
import { ServerExceptionModel } from '../models/ServerExceptionModel'
import Logger from '../logger'
import VueJsonEditor from 'vue-json-editor'

export default {
    name: 'Settings',
    mounted: function () {
        if (this.$store.getters.isAuthenticated) {
            this.loadData()
        }
    },
    methods: {
        // TODO Add machine type to response. Create basic DTO?
        loadData: async function () {
            try {
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
                    this.$toaster.error('Internal server error')
                    Logger.error(err)
                }
                this.settings = {}
            }
        },

        UpdateConfig: async function () {
            try {
                const result = await this.$store.state.requestService.setCoreConfig(this.settings)
                if (result) {
                    this.$toaster.success('Config successfully updated')
                } else {
                    this.$toaster.warn('Deprecated. Check backend code')
                }
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message)
                } else {
                    this.$toaster.error('Internal server error')
                    Logger.error(err)
                }
            }
        },

        ResetConfig: async function () {
            await this.loadData()
        }
    },
    components: {
        VueJsonEditor,
        'app-login-modal': LoginModal
    },
    data: () => {
        return {
            settings: {},
            rawMode: true
        }
    }
}
</script>

<style scoped lang="scss">
</style>
