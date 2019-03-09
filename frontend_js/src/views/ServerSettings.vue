<template>
    <div>
        <div class="mb-3">
            <h2 align="center">Настройки сервера</h2>
        </div>
        <div class="row margin-bottom-sm">
            <div class="col-md-8 offset-md-2">
                <h3>Конфигурация подключения к серверу</h3>
            </div>
        </div>
        <app-server-connection></app-server-connection>

        <div class="row margin-bottom-sm">
            <div class="col-md-8 offset-md-2">
                <h3>Конфигурация сервера</h3>
            </div>
        </div>
        <div class="row margin-bottom-sm">
            <div class="col-md-8 offset-md-2">
                <h3>Конфигурация ssh ключей</h3>
            </div>
        </div>
        <div class="row margin-bottom-sm">
            <div class="col-md-8 offset-md-2">
                <b-form-file
                    v-model="file"
                    placeholder="Архив с ssh ключами для обновления"
                    accept=".zip"
                    drop-placeholder="Перетащите архив сюда"
                />

                <!--<div class="custom-file" id="customFile">-->
                    <!--<input type="file" class="custom-file-input" accept=".zip" id="ssh"-->
                           <!--@change="handleFileUpload($event)">-->
                    <!--<label class="custom-file-label" for="ssh">-->
                        <!--Архив с ssh ключами для обновления-->
                    <!--</label>-->
                <!--</div>-->

            </div>
        </div>
        <div class="row margin-bottom-sm">
            <div class="offset-md-2 col-md-8" align="right">
                <button class="btn btn-success" @click="updateSSH()">
                    Обновить
                </button>
            </div>
        </div>
        <div class="row margin-bottom-sm">
            <div class="col-md-8 offset-md-2">
                <h3>Смена пароля</h3>
            </div>
        </div>
        <div class="row margin-bottom-sm">
            <label class="offset-md-2 col-md-3 col-form-label" for="oldPassword">Текущий пароль</label>
            <div class="col-md-5">
                <input class="form-control" type="password" id="oldPassword" v-model="oldPassword"
                       :placeholder="'Текущий пароль'"/>
            </div>
        </div>
        <div class="row margin-bottom-sm">
            <label class="offset-md-2 col-md-3 col-form-label" for="newPassword">Новый пароль</label>
            <div class="col-md-5">
                <input class="form-control" type="password" id="newPassword" v-model="newPassword"
                       :placeholder="'Новый пароль'"/>
            </div>
        </div>
        <div class="row margin-bottom-sm">
            <label class="offset-md-2 col-md-3 col-form-label" for="newPasswordAgain">Повторно новый пароль</label>
            <div class="col-md-5">
                <input class="form-control" type="password" id="newPasswordAgain" v-model="newPasswordAgain"
                       :placeholder="'Повторно новый пароль'"/>
            </div>
        </div>
        <div class="row margin-bottom-sm">
            <div class="offset-md-2 col-md-8" align="right">
                <button class="btn btn-danger" @click="resetPassword()">
                    Сбросить
                </button>
                <button class="ml-3 btn btn-success" @click="updatePassword()">
                    Обновить
                </button>
            </div>
        </div>
    </div>
</template>

<script>

import Logger from '../logger';
import { ServerExceptionModel } from '../models/ServerExceptionModel'
import ServerConnect from '../components/ServerConnect'

export default {
    name: 'ServerSettings',
    components: {
        'app-server-connection': ServerConnect
    },
    data() {
        return {
            oldPassword: '',
            newPassword: '',
            newPasswordAgain: '',
            file: null
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
                await this.$store.dispatch('changePassword', this.oldPassword, this.newPassword);
                this.$toaster.success('Пароль успешно обновлен');
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Ошибка сервера');
                    Logger.error(err);
                }
            }
        },
        async updateSSH() {
            const formData = new FormData();
            formData.append('file', this.file);
            try {
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
        },
        handleFileUpload(event) {
            this.file = event.target.files[0];
        }
    }
}
</script>

<style scoped>

</style>
