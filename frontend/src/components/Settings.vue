<template>
    <div>
        <div class="mb-3">
            <h2 align="center">Конфигурация сервера</h2>
        </div>
        <div v-if="settings">
            <div class="row form-group" v-for="(setting_value, setting_key) in settings">
                <label class="offset-md-2 col-md-3 col-form-label" :for="setting_key">{{setting_key}}</label>
                <div class="col-md-5">
                    <input class="form-control" type="text" :id="setting_key" v-model="settings[setting_key]" :placeholder="setting_key"/>
                </div>
            </div>
            <div class="row form-group">
                <div class="col-md-6 offset-md-4" align="right">
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

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator';
    import LoginModal from './LoginModal.vue';
    import axios from 'axios';

    @Component({
        components: {
            'app-login-modal': LoginModal,
        },
    })
    export default class Settings extends Vue {
        // @Inject('getCurrentSettings') private getCurrentSettings: any;
        private settings: any = null;

        private async loadData() {
            const answer = await axios.get('http://127.0.0.1:5000/api/config');
            this.settings = answer.data;
        }

        private async UpdateConfig() {
            console.log('New configs');
            const answer = await axios.post('http://127.0.0.1:5000/api/config', this.settings);
            console.log(answer);
        }

        private async ResetConfig() {
            await this.loadData();
        }
    }
</script>

<style scoped lang="scss">
</style>