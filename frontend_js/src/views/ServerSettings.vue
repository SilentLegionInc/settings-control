<template>
    <div class="container-fluid">
        <div class="row mb-3" style="margin: auto">
            <div class="col-12"  align="center">
                <h2>Настройки сервера</h2>
            </div>
        </div>
        <divider class="mb-2"><h5 align="center">Конфигурация подключения к серверу</h5></divider>
        <div class="row mb-3" style="margin: auto">
            <div class="col-12 col-sm-12 col-md-12 col-lg-10 offset-lg-1 col-xl-10 offset-xl-1">
                <app-server-connection></app-server-connection>
            </div>
        </div>
        <divider class="mb-2"><h5 align="center">Конфигурация сервера</h5></divider>
        <div class="row mb-3" style="margin: auto">
            <div class="col-12 col-sm-12 col-md-12 col-lg-10 offset-lg-1 col-xl-10 offset-xl-1">
                <app-server-config></app-server-config>
            </div>
        </div>
        <divider class="mb-2"><h5 align="center">Конфигурация ssh ключей</h5></divider>
        <div class="container-fluid mb-3">
            <div class="row">
                <div class="col-12 col-sm-12 col-md-12 col-lg-10 offset-lg-1 col-xl-10 offset-xl-1">
                    <div class="container-fluid">
                        <div class="row mb-3">
                            <label class="col-xl-3 col-lg-3 col-form-label" for="ssh">Новые ssh ключи:</label>
                            <div class="col-xl-9 col-lg-9 col-12 ">
                                <b-form-file
                                    id="ssh"
                                    v-model="file"
                                    placeholder="Загрузить архив"
                                    accept=".zip"
                                    drop-placeholder="Перетащите архив сюда"
                                />
                                <p class="card-text" style="font-size: 0.75rem; color: rgba(16,8,13,0.54)">Передайте файл ssh.zip, внутри которого будет папка ssh, содержащая ssh-ключи.
                                    Все имеющиеся на удаленной машине ключи будут удалены</p>
                            </div>
                        </div>
                        <div class="row mb-2">
                            <div class="col-xl-3 offset-xl-6 col-lg-3 offset-lg-6 col-sm-6 offset-0 col-12 mb-1">
                                <button class="btn btn-danger btn-block" @click="resetSSH()">
                                    Сбросить
                                </button>
                            </div>
                            <div class="col-xl-3 col-lg-3 col-sm-6 col-12">
                                <button class="btn btn-success btn-block" @click="updateSSH()">
                                    Обновить
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <divider class="mb-2"><h5 align="center">Смена пароля</h5></divider>
        <div class="container-fluid mb-3">
            <div class="row">
                <div class="col-12 col-sm-12 col-md-12 col-lg-10 offset-lg-1 col-xl-10 offset-xl-1">
                    <div class="container-fluid">
                        <div class="row mb-2">
                            <label class="col-xl-3 col-lg-3 col-form-label" for="oldPassword">Текущий пароль:</label>
                            <div class="col-xl-9 col-lg-9 col-12">
                                <input class="form-control" type="password" id="oldPassword" v-model="oldPassword"
                                       :placeholder="'Введите текущий пароль'"/>
                            </div>
                        </div>
                        <div class="row mb-2">
                            <label class="col-xl-3 col-lg-3 col-form-label" for="newPassword">Новый пароль:</label>
                            <div class="col-xl-9 col-lg-9 col-12">
                                <input class="form-control" type="password" id="newPassword" v-model="newPassword"
                                       :placeholder="'Введите новый пароль'"/>
                            </div>
                        </div>
                        <div class="row mb-2">
                            <label class="col-xl-3 col-lg-3 col-form-label" for="newPasswordAgain">Повторно новый пароль:</label>
                            <div class="col-xl-9 col-lg-9 col-12">
                                <input class="form-control" type="password" id="newPasswordAgain" v-model="newPasswordAgain"
                                       :placeholder="'Повторно введите новый пароль'"/>
                            </div>
                        </div>
                        <div class="row mb-2">
                            <div class="col-xl-3 offset-xl-6 col-lg-3 offset-lg-6 col-sm-6 offset-0 col-12 mb-1">
                                <button class="btn btn-danger btn-block" @click="resetPassword()">
                                    Сбросить
                                </button>
                            </div>
                            <div class="col-xl-3 col-lg-3 col-sm-6 col-12">
                                <button class="btn btn-success btn-block" @click="updatePassword()">
                                    Обновить
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

import Logger from '../logger';
import { ServerExceptionModel } from '../models/ServerExceptionModel'
import ServerConnect from '../components/ServerConnect'
import ServerConfig from '../components/ServerConfig'
import Divider from '../components/Divider'

export default {
    name: 'ServerSettings',
    components: {
        Divider,
        'app-server-connection': ServerConnect,
        'app-server-config': ServerConfig
    },
    data() {
        return {
            oldPassword: '',
            newPassword: '',
            newPasswordAgain: '',
            file: null,
            _loader: null
        }
    },
    methods: {
        resetPassword() {
            this.oldPassword = '';
            this.newPassword = '';
            this.newPasswordAgain = '';
        },
        async updatePassword() {
            Logger.info(window.location.origin);
            if (!this.oldPassword) {
                this.$toaster.error('Необходимо ввести текущий пароль');
                return;
            }
            if (!this.newPassword) {
                this.$toaster.error('Нельзя задать пустой пароль');
                return;
            }
            if (this.newPassword !== this.newPasswordAgain) {
                this.$toaster.error('Введеные пароли не совпадают');
                return;
            }
            try {
                this._loader = this.$loading.show();
                console.log(this.oldPassword, this.newPassword);
                await this.$store.dispatch('changePassword', { 'oldPassword': this.oldPassword, 'newPassword': this.newPassword });
                this.$toaster.success('Пароль успешно обновлен');
                this._loader.hide();
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Ошибка сервера');
                    Logger.error(err);
                }
                this._loader.hide();
            }
        },
        async updateSSH() {
            const formData = new FormData();
            formData.append('file', this.file);
            try {
                this._loader = this.$loading.show();
                await this.$store.state.requestService.uploadSSHArchive(formData);
                this.$toaster.success('Ключи успешно обновлены');
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.file = null;
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Серверная ошибка');
                    Logger.error(err);
                }
            }
            this._loader.hide();
        },
        resetSSH() {
            this.file = null;
        }
    }
}
</script>

<style scoped>

</style>
