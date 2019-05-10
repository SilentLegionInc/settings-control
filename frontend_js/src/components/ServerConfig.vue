<template>
    <div class="container-fluid">
        <div class="row mb-2">
            <label class="col-xl-3 col-lg-3 col-form-label" for="sourcesPath">Путь до папки исходников:</label>
            <div class="col-xl-9 col-lg-9 col-12">
                <input class="form-control" type="text" id="sourcesPath" v-model="data.sourcesPath"
                       :placeholder="'...'"/>
            </div>
        </div>
        <div class="row mb-2">
            <label class="col-xl-3 col-lg-3 col-form-label" for="buildsPath">Путь до папки сборки:</label>
            <div class="col-xl-9 col-lg-9 col-12">
                <input class="form-control" type="text" id="buildsPath" v-model="data.buildsPath"
                       :placeholder="'...'"/>
            </div>
        </div>
        <div class="row mb-2">
            <label class="col-xl-3 col-lg-3 col-form-label" for="uploadPath">Путь до папки загрузки:</label>
            <div class="col-xl-9 col-lg-9 col-12">
                <input class="form-control" type="text" id="uploadPath" v-model="data.uploadPath"
                       :placeholder="'...'"/>
            </div>
        </div>
        <div class="row mb-2">
            <label class="col-xl-3 col-lg-3 col-form-label" for="qmakePath">Путь до qmake:</label>
            <div class="col-xl-9 col-lg-9 col-12">
                <input class="form-control" type="text" id="qmakePath" v-model="data.qmakePath"
                       :placeholder="'...'"/>
            </div>
        </div>
        <div class="row mb-2">
            <label class="col-xl-3 col-lg-3 col-form-label" for="repositoriesPlatform">Платформа git:</label>
            <div class="col-xl-9 col-lg-9 col-12">
                <input class="form-control" type="text" id="repositoriesPlatform" v-model="data.repositoriesPlatform"
                       :placeholder="'...'"/>
            </div>
        </div>
        <div class="row mb-2">
            <label class="col-xl-3 col-lg-3 col-form-label" for="machineType">Тип машинки:</label>
            <div class="col-xl-9 col-lg-9 col-12">
                <b-form-select id="machineType" v-model="data.machineType" :options="data.possibleMachinesTypes">
                </b-form-select>
            </div>

        </div>
        <div class="row mb-2">
            <div class="col-xl-3 offset-xl-6 col-lg-3 offset-lg-6 col-sm-6 offset-0 col-12 mb-1">
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
</template>

<script>
import { ServerExceptionModel } from '../models/ServerExceptionModel'
import Logger from '../logger';

export default {
    name: 'ServerConfig',
    data() {
        return {
            data: {}
        }
    },
    mounted() {
        if (this.$store.getters.isAuthenticated) {
            this.loadData();
        } else {
            this.$toaster.error('Для доступа к этой странице необходима авторизация');
            this.$router.push('/login');
        }
    },
    methods: {
        async loadData() {
            const loader = this.$loading.show();
            try {
                this.data = await this.$store.state.requestService.getServerConfig();
                if (this.data.machineType !== this.$store.state.robotName) {
                    this.$store.commit('setRobotName', this.data.machineType);
                }
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Серверная ошибка');
                    Logger.error(err);
                }
            }
            loader.hide();
        },

        UpdateConfig: async function() {
            const loader = this.$loading.show();
            try {
                await this.$store.state.requestService.setServerConfig(this.data.toPythonDict());
                if (this.data.machineType !== this.$store.state.robotName) {
                    this.$store.commit('setRobotName', this.data.machineType);
                }
                this.$toaster.success('Успешно обновлено');
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message)
                } else {
                    this.$toaster.error('Серверная ошибка')
                    Logger.error(err)
                }
            }
            loader.hide();
        },

        ResetConfig: async function() {
            await this.loadData();
        }

    }
}
</script>

<style scoped>

</style>
