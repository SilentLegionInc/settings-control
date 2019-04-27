<template>
    <div class="container-fluid">
        <div class="row mb-2">
            <label class="col-xl-3 col-lg-3 col-form-label" for="hostAddress">Адрес сервера: </label>
            <div class="col-xl-9 col-lg-9 col-12">
                <input class="form-control" type="text" id="hostAddress" v-model="url"
                       :placeholder="'Введите адрес сервера host:port'"/>
            </div>
        </div>
        <div class="row mb-2">
            <div class="offset-xl-3 col-xl-3 col-12 offset-lg-3 col-lg-3 col-md-4 mt-1">
                <button class="btn btn-primary btn-block" @click="setClientUrl()">
                    Ввести адрес клиента
                </button>
            </div>
            <div class="col-xl-3 col-lg-3 col-12 col-md-4 mt-1">
                <button class="btn btn-info btn-block" @click="checkConnectionStatus()">
                    Проверить адрес
                </button>
            </div>
            <div class="col-xl-3 col-lg-3 col-12 col-md-4 mt-1">
                <button class="btn btn-success btn-block" @click="changeHostAddress()">
                    Подключить
                </button>
                <!--<i class="fa fa-circle" :style="{'color': connectionStatus ? 'green': 'red'}"></i>-->
            </div>
        </div>
    </div>
</template>

<script>
import { catchErrorsWrapper } from '../helpers';

export default {
    name: 'ServerConnect',
    data() {
        return {
            url: this.$store.state.url
        }
    },
    methods: {
        async checkConnectionStatus() {
            const loader = this.$loading.show();

            await catchErrorsWrapper(this.$toaster, async () => {
                const connectionStatus = await this.$store.state.requestService.getServerInfo(this.url);
                if (connectionStatus.ok) {
                    this.$toaster.info(`Сервер ${this.url} доступен`);
                } else {
                    this.$toaster.error(`Сервер ${this.url} недоступен`);
                }
            });

            loader.hide();
        },

        async changeHostAddress() {
            this.$store.commit('changeHostAddress', this.url);
            try {
                const connectionStatus = await this.$store.state.requestService.getServerInfo();
                this.$emit('changedHost');
                if (connectionStatus.ok) {
                    this.$store.commit('setRobotName', connectionStatus.robotType);
                    this.$store.commit('setRobotLabel', connectionStatus.robotName);
                    this.$toaster.success('Успешно подключено');
                }
            } catch (err) {
                this.$store.commit('setRobotName', null);
                this.$store.commit('setRobotLabel', 'UNK')
                this.$toaster.error('Не удалось подключиться');
            }
        },

        setClientUrl() {
            const location = window.location.origin.split('://')[1];
            this.url = location.split(':')[0] + ':5000';
        }
    }
}
</script>

<style scoped>

</style>
