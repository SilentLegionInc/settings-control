<template>
    <div class="flexbox">
        <div class="container-fluid">
            <div class="row">
                <div class="offset-0 offset-sm-0 offset-md-1 offset-lg-2 offset-xl-3 col-12 col-sm-12 col-md-10 col-lg-8 col-xl-6">
                    <b-card>
                        <div class="container-fluid">
                            <h2 align="center">Выбор сервера</h2>
                            <div class="row mb-3">
                                <label class="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12 mb-1" for="hostAddress" style="font-size: smaller">
                                    Адрес сервера:
                                </label>
                                <div class="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12">
                                    <input id="hostAddress"
                                           type="text"
                                           v-model="url"
                                           class="form-control"
                                           :placeholder="'Введите адрес сервера host:port'"
                                    />
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-12 col-sm-12 col-md-4 col-lg-4 col-xl-4 mb-1">
                                    <button class="btn btn-primary btn-block" @click="setClientUrl()">
                                        Адрес клиента
                                    </button>
                                </div>
                                <div class="col-12 col-sm-12 col-md-4 col-lg-4 col-xl-4 mb-1">
                                    <button class="btn btn-info btn-block" @click="checkConnectionStatus()">
                                        Проверить
                                    </button>
                                </div>
                                <div class="col-12 col-sm-12 col-md-4 col-lg-4 col-xl-4 mb-1">
                                    <button class="btn btn-success btn-block" @click="changeHostAddress()">
                                        Подключить
                                    </button>
                                </div>
                            </div>
                        </div>
                    </b-card>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { catchErrorsWrapper } from '../helpers';

export default {
    name: 'Home',
    data() {
        return {
            url: this.$store.state.url
        }
    },
    methods: {
        async checkConnectionStatus() {
            const loader = this.$loading.show();

            await catchErrorsWrapper(this.$toaster, async () => {
                try {
                    const connectionStatus = await this.$store.state.requestService.getServerInfo(this.url);
                    if (connectionStatus.ok) {
                        this.$toaster.info(`Сервер ${this.url} доступен`);
                    }
                } catch (exception) {
                    this.$toaster.error(`Сервер ${this.url} недоступен`);
                }
            });

            loader.hide();
        },

        async changeHostAddress() {
            this.$store.commit('changeHostAddress', this.url);
            try {
                const connectionStatus = await this.$store.state.requestService.getServerInfo();
                if (connectionStatus.ok) {
                    this.$toaster.success('Успешно подключено');
                    this.$store.commit('setRobotName', connectionStatus.robotType);
                    this.$store.commit('setRobotLabel', connectionStatus.robotName);
                }
            } catch (err) {
                this.$store.commit('setRobotName', null);
                this.$store.commit('setRobotLabel', 'UNK');
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

<style scoped lang="scss">
    .flexbox {
        display: flex;
        justify-content: center;
        flex-flow: column;
    }
</style>
