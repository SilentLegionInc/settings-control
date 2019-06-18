<template>
    <div>
        <div class="row mt-2">
            <label class="offset-md-2 col-md-3 col-form-label" for="oldPassword">Текущий пароль</label>
            <div class="col-md-5">
                <input class="form-control" type="password" id="oldPassword" v-model="oldPassword" placeholder=""/>
            </div>
        </div>
        <div class="row mt-2">
            <label class="offset-md-2 col-md-3 col-form-label" for="newPassword">Новый пароль</label>
            <div class="col-md-5">
                <input class="form-control" type="password" id="newPassword" v-model="newPassword" placeholder=""/>
            </div>
        </div>
        <div class="row mt-2">
            <div class="offset-md-8 col-md-2" align="right">
                <button class="btn btn-success" @click="updatePassword()">Обновить</button>
            </div>
        </div>
    </div>
</template>

<script>
import { ServerExceptionModel } from '../models/ServerExceptionModel';
import Logger from '../logger';

export default {
    name: 'ChangePassword',
    data: () => {
        return {
            oldPassword: '',
            newPassword: ''
        }
    },
    methods: {
        async updatePassword() {
            const loader = this.$loading.show();
            try {
                await this.$store.state.requestService.changePassword(this.oldPassword, this.newPassword);
                this.$toaster.success('Password changed');
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

}
</script>

<style scoped>

</style>
