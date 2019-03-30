<template>
    <div class="flexbox">
        <div class="container-fluid">
            <div class="row">
                <div class="offset-0 offset-sm-2"></div>
                <div class="col-12 col-sm-8">
                    <b-card>
                        <h2>Авторизация</h2>
                        <div class="container-fluid">
                            <div class="row mb-3">
                                <label class="col-form-label col-xl-3 col-12" for="password">Пароль:</label>
                                <div class="col-xl-9 col-12">
                                    <input class="form-control" id="password" type="password" v-model="password" name="password" autocomplete="password"/>
                                </div>
                            </div>
                            <div class="row">
                                <div class="offset-xl-6 col-xl-3 mb-3">
                                    <button class="btn btn-secondary btn-block" @click="serverSettings = !serverSettings">
                                        Выбрать сервер
                                        <i class="fa" :class="{'fa-angle-down': !serverSettings, 'fa-angle-up': serverSettings}"></i>
                                    </button>
                                </div>
                                <div class="col-xl-3">
                                    <button class="btn btn-primary btn-block" @click="login()">Войти</button>
                                </div>
                            </div>
                        </div>

                        <div v-if="serverSettings">
                            <app-server-connect @changedHost="login()"></app-server-connect>
                        </div>
                    </b-card>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import ServerConnect from '../components/ServerConnect'
import { ServerExceptionModel } from '../models/ServerExceptionModel'
import Logger from '../logger';

export default {
    data () {
        return {
            url: null,
            password: null,
            serverSettings: false
        }
    },
    components: {
        'app-server-connect': ServerConnect
    },
    methods: {
        async login() {
            const loader = this.$loading.show();
            try {
                await this.$store.dispatch('authorize', this.password);
                this.$toaster.success('Успешно авторизован');
                loader.hide();
                this.$emit('logged');
                this.$router.push('/');
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Серверная ошибка');
                    Logger.error(err);
                }
            }
            loader.hide();
        }
    }
};
</script>

<style scoped lang="scss">
    .flexbox {
        display: flex;
        justify-content: center;
        flex-flow: column;
    }
</style>
