<template>
    <div>
        <div v-if="settings">
            <div class="row form-group" v-for="(setting_value, setting_key) in settings">
                <div class="col-md-2"></div>
                <label class="col-md-3 col-form-label" :for="setting_key">{{setting_key}}</label>
                <div class="col-md-5">
                    <input class="form-control" type="text" :id="setting_key" v-model="settings[setting_key]" :placeholder="setting_key"/>
                </div>
                <div class="col-md-2"></div>
            </div>
            <div class="row">
                <div class="col-md-2"></div>
                <div class="col-md-3">
                    <button class="btn btn-lg btn-success" @click="UpdateConfig()">Update</button>
                </div>
                <div class="col-md-5" align="right">
                    <button class="btn btn-lg btn-danger" @click="ResetConfig()">Reset</button>
                </div>
                <div class="col-md-2"></div>
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
        private settings: object = null;
        private name: string = 'привет';

        private loadData() {
            axios.get('http://127.0.0.1:5000/api/config').then(answer => {
                this.settings = answer.data;
            });
        }

        private UpdateConfig() {
            console.log('New configs');
            console.log(this.settings);
            axios.post('http://127.0.0.1:5000/api/config', this.settings).then(answer => {
                console.log(answer);
            });
        }

        private ResetConfig() {
            console.log('Reset');
            axios.get('http://127.0.0.1:5000/api/config').then(answer => {
                this.settings = answer.data;
            });
        }
    }
</script>

<style scoped lang="scss">
</style>