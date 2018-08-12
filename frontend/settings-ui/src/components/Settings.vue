<template>
    <div>
        <div class="row form-group" v-for="(setting_value, setting_key) in settings">
            <label class="col-md-3 col-form-label" :for="setting_key">{{setting_key}}</label>
            <div class="col-md-9">
                <input class="form-control" type="text" :id="setting_key" v-model="settings[setting_key]" :placeholder="setting_key"/>
            </div>
        </div>
        <div class="row">
            <div class="col-md-3">
                <button class="btn btn-lg btn-success" @click="UpdateConfig()">Update</button>
            </div>
            <div class="col-md-3">
                <button class="btn btn-lg btn-primary" @click="ResetConfig()">Reset</button>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import {Component, Prop, Vue, Inject} from 'vue-property-decorator';
    import axios from 'axios';

    @Component
    export default class Settings extends Vue {
        // @Inject('getCurrentSettings') private getCurrentSettings: any;
        private settings: any = {};
        private name: string = 'привет';

        private created() {
            axios.get('http://127.0.0.1:5000/config', {
                headers: {
                    'Access-Control-Allow-Origin': '*',
                }}).then(answer => {
                this.settings = answer.data;
                // console.log(answer);
                for(let setting in this.settings) {
                    console.log(setting);
                }
            });
            // this.getCurrentSettings.then((d: any) => {
            //     console.log(d.data);
            //     this.data = d.data;
            // });
        }

        private UpdateConfig() {
            console.log('New configs');
            console.log(this.settings);
        }

        private ResetConfig() {
            console.log('Reset');
            axios.get('http://127.0.0.1:5000/config', {
                headers: {
                    'Access-Control-Allow-Origin': '*',
                }}).then(answer => {
                this.settings = answer.data;
                // console.log(answer);
                for(let setting in this.settings) {
                    console.log(setting);
                }
            });
        }
    }
</script>

<style scoped>

</style>