<template>
    <div class="container-fluid">
        <div class="row mb-3" style="margin: auto">
            <div class="col-12"  align="center">
                <h2>Настройки сервера</h2>
                <hr>
            </div>
        </div>
        <div class="row mb-3" style="margin: auto">
            <div class="col-12" align="center">
                <h3>Конфигурация подключения к серверу</h3>
            </div>
        </div>
        <app-server-connection></app-server-connection>
        <div class="row mb-3" style="margin: auto">
            <div class="col-12" align="center">
                <h3>Конфигурация сервера</h3>
            </div>
        </div>
        <app-server-config></app-server-config>
        <div class="row mb-3" style="margin: auto">
            <div class="col-12" align="center">
                <h3>Конфигурация ssh ключей</h3>
            </div>
        </div>
        <div class="container-fluid">
            <div class="row mb-3">
                <label class="col-xl-3 col-form-label" for="ssh">Новые ssh ключи:</label>
                <div class="col-12 col-xl-9">
                    <b-form-file
                        id="ssh"
                        v-model="file"
                        placeholder="Загрузить архив"
                        accept=".zip"
                        drop-placeholder="Перетащите архив сюда"
                    />
                </div>
            </div>
            <div class="row mb-2">
                <div class="offset-xl-9 col-xl-3 col-12">
                    <button class="btn btn-success btn-block mt-1" @click="updateSSH()">
                        Обновить
                    </button>
                </div>
            </div>
        </div>
        <div class="row mb-2" style="margin: auto">
            <div class="col-12" align="center">
                <h3>Смена пароля</h3>
            </div>
        </div>
        <div class="container-fluid">
            <div class="row mb-2">
                <label class="col-xl-3 col-form-label" for="oldPassword">Текущий пароль:</label>
                <div class="col-xl-9 col-12">
                    <input class="form-control" type="password" id="oldPassword" v-model="oldPassword"
                           :placeholder="'Введите текущий пароль'"/>
                </div>
            </div>
            <div class="row mb-2">
                <label class="col-xl-3 col-form-label" for="newPassword">Новый пароль:</label>
                <div class="col-xl-9 col-12">
                    <input class="form-control" type="password" id="newPassword" v-model="newPassword"
                           :placeholder="'Введите новый пароль'"/>
                </div>
            </div>
            <div class="row mb-2">
                <label class="col-xl-3 col-form-label" for="newPasswordAgain">Повторно новый пароль:</label>
                <div class="col-xl-9 col-12">
                    <input class="form-control" type="password" id="newPasswordAgain" v-model="newPasswordAgain"
                           :placeholder="'Повторно введите новый пароль'"/>
                </div>
            </div>
            <div class="row mb-2">
                <div class="offset-xl-6 col-xl-3 col-6 mt-1">
                    <button class="btn btn-danger btn-block" @click="resetPassword()">
                        Сбросить
                    </button>
                </div>
                <div class="col-xl-3 col-6 mt-1">
                    <button class="btn btn-success btn-block" @click="updatePassword()">
                        Обновить
                    </button>
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

export default {
    name: 'ServerSettings',
    components: {
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
                await this.$store.dispatch('changePassword', this.oldPassword, this.newPassword);
                this.$toaster.success('Пароль успешно обновлен');
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
        handleFileUpload(event) {
            this.file = event.target.files[0];
        }
    }
}
</script>

<style scoped>

</style>
