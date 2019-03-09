<template>
    <div>
        <div class="row margin-bottom-sm">
            <label class="offset-md-2 col-md-3 col-form-label" for="hostAddress">Адрес сервера</label>
            <div class="col-md-5">
                <input class="form-control" type="text" id="hostAddress" v-model="url"
                       :placeholder="'Введите адрес сервера host:port'"/>
            </div>
        </div>
        <div class="row margin-bottom-sm">
            <div class="offset-md-2 col-md-8" align="right">
                <button class="btn btn-default" @click="setClientUrl()">
                    Использовать адрес клиента
                </button>
                <button class="ml-3 btn btn-info" @click="checkConnectionStatus()">
                    Проверить адрес
                </button>
                <button class="ml-3 btn btn-success" @click="changeHostAddress()">
                    Подключить
                </button>
                <!--<i class="fa fa-circle" :style="{'color': connectionStatus ? 'green': 'red'}"></i>-->
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ServerConnect',
    data() {
        return {
            url: this.$store.state.url
        }
    },
    methods: {
        async checkConnectionStatus() {
            const connectionStatus = await this.$store.state.requestService.getHealth(this.url);
            if (connectionStatus) {
                this.$toaster.info(`Сервер ${this.url} доступен`);
            } else {
                this.$toaster.error(`Сервер ${this.url} недоступен`);
            }
        },

        async changeHostAddress() {
            this.$store.commit('changeHostAddress', this.url);
            const connectionStatus = await this.$store.state.requestService.getHealth();
            if (connectionStatus) {
                this.$toaster.success('Успешно подключено');
            } else {
                this.$toaster.error('Некорректный адрес');
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
