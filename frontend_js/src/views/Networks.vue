<template>
    <div class="container-fluid">
        <div class="mb-3">
            <h2 align="center">Конфигурация сети</h2>
        </div>
        <divider text="Беспроводные соединения"></divider>
        <div v-if="wirelessNetworks.length > 0" role="tablist">
            <div v-for="(network, index) of wirelessNetworks" v-bind:key="index">
                <div class="row"  style="margin: auto">
                    <div class="col-xl-8 offset-xl-2 offset-0 col-12">
                        <b-card no-body class="mb-1">
                            <b-card-header header-tag="header" class="p-1" role="tab">
                                <b-button block href="#" v-b-toggle="'wireless' + index" variant="info">{{network.name}} ({{network.signalLevel}})</b-button>
                            </b-card-header>
                            <b-collapse :id="'wireless' + index" :visible="network.active" accordion="wireless-accordion" role="tabpanel">
                                <b-card-body>
                                    <div class="row mb-2">
                                        <div class="col-xl-3 col-4">
                                            Имя сети:
                                        </div>
                                        <div class="col-xl-9 col-8">
                                            {{network.name || '-'}}
                                        </div>
                                    </div>
                                    <div class="row mb-2">
                                        <div class="col-xl-3 col-4">
                                            Идентификатор сети:
                                        </div>
                                        <div class="col-xl-9 col-8">
                                            {{network.id || '-'}}
                                        </div>
                                    </div>
                                    <div class="row mb-2">
                                        <div class="col-xl-3 col-4">
                                            Режим:
                                        </div>
                                        <div class="col-xl-9 col-8">
                                            {{network.mode || '-'}}
                                        </div>
                                    </div>
                                    <div class="row mb-2">
                                        <div class="col-xl-3 col-4">
                                            Канал:
                                        </div>
                                        <div class="col-xl-9 col-8">
                                            {{network.channel || '-'}}
                                        </div>
                                    </div>
                                    <div class="row mb-2">
                                        <div class="col-xl-3 col-4">
                                            Частота:
                                        </div>
                                        <div class="col-xl-9 col-8">
                                            {{network.frequency || '-'}}
                                        </div>
                                    </div>
                                    <div class="row mb-2">
                                        <div class="col-xl-3 col-4">
                                            Пропускная способность:
                                        </div>
                                        <div class="col-xl-9 col-8">
                                            {{network.speedRate || '-'}}
                                        </div>
                                    </div>
                                    <div class="row mb-2">
                                        <div class="col-xl-3 col-4">
                                            Интерфейс:
                                        </div>
                                        <div class="col-xl-9 col-8">
                                            {{network.device || '-'}}
                                        </div>
                                    </div>
                                    <!--TODO finish me-->
                                    <div class="row mb-3">
                                        <div class="offset-xl-3 offset-0 col-xl-3 col-4">
                                            <button class="btn btn-block btn-primary">
                                                Подключение к сети
                                                <!--Подключение к сети&nbsp;<i class="fa" :class="{'fa-angle-down': !module_elem.detail, 'fa-angle-up': module_elem.detail}"></i>-->
                                            </button>
                                        </div>
                                        <div class="col-xl-3 col-4">
                                            <button :id="'wirelessParamsButton' + index" :disabled="!network.id" class="btn btn-block btn-primary" v-b-toggle="'wirelessParams' + index">
                                                Настройка параметров&nbsp;<i class="fa fa-angle-down"></i>
                                            </button>
                                        </div>
                                        <div class="col-xl-3 col-4">
                                            <button :disabled="!network.id || !password || network.active" class="btn btn-block btn-primary" @click="connect(network)">
                                                Подключиться
                                            </button>
                                        </div>
                                    </div>
                                    <b-collapse :id="'wirelessParams' + index">
                                        <div class="row mb-2">
                                            <div class="col-xl-3 col-4">
                                                DHCP:
                                            </div>
                                            <div class="col-xl-9 col-8">
                                                <b-form-checkbox v-model="network.requiredParams.ipv4method"  switch>
                                                    <b>(Checked: {{ network.requiredParams.ipv4method }})</b> {{network.requiredParams._ipv4method}}
                                                </b-form-checkbox>
                                            </div>
                                        </div>
                                        <!--TODO add validation like here https://bootstrap-vue.js.org/docs/components/form-input/-->
                                        <div class="row mb-2">
                                            <label class="col-xl-3 col-form-label" :for="'wireless' + index + 'ipv4address'">Ipv4 адрес:</label>
                                            <div class="col-xl-9 col-12">
                                                <input :disabled="network.requiredParams.ipv4method"
                                                       :id="'wireless' + index + 'ipv4address'"
                                                       :placeholder="'...'"
                                                       v-model="network.requiredParams.ipv4address"
                                                       class="form-control"
                                                       type="text"/>
                                            </div>
                                        </div>
                                        <div class="row mb-2">
                                            <label class="col-xl-3 col-form-label" :for="'wireless' + index + 'ipv4gateway'">Ipv4 gateway:</label>
                                            <div class="col-xl-9 col-12">
                                                <input :disabled="network.requiredParams.ipv4method"
                                                       :id="'wireless' + index + 'ipv4gateway'"
                                                       :placeholder="'...'"
                                                       v-model="network.requiredParams.ipv4gateway"
                                                       class="form-control"
                                                       type="text"/>
                                            </div>
                                        </div>
                                        <div class="row mb-2">
                                            <label class="col-xl-3 col-form-label" :for="'wireless' + index + 'ipv4dns'">Ipv4 dns:</label>
                                            <div class="col-xl-9 col-12">
                                                <input :disabled="network.requiredParams.ipv4method"
                                                       :id="'wireless' + index + 'ipv4dns'"
                                                       :placeholder="'...'"
                                                       v-model="network.requiredParams.ipv4dns"
                                                       class="form-control"
                                                       type="text"/>
                                            </div>
                                        </div>
                                    </b-collapse>
                                    <div class="row mb-2" v-if="!network.active">
                                        <label class="col-xl-3 col-form-label mb-1" :for="'wireless'+index+'password'">Архив с исходниками для обновления:</label>
                                        <div class="col-xl-9 col-12 mb-1">
                                            <input :id="'wireless'+index+'password'" type="password" v-model="password"
                                                   class="form-control" placeholder="Enter password">
                                        </div>
                                    </div>
                                </b-card-body>
                            </b-collapse>
                        </b-card>
                    </div>
                </div>
            </div>
        </div>
        <divider text="Проводные соединения"></divider>
        <div v-if="wiredNetworks.length > 0" role="tablist">
            <div v-for="(wiredNetwork, index) of wiredNetworks" v-bind:key="index">
                <div class="row" style="margin: auto">
                    <div class="col-xl-8 offset-xl-2 offset-0 col-12">
                        <b-card no-body class="mb-1">
                            <b-card-header header-tag="header" class="p-1" role="tab">
                                <!--<div v-b-toggle.accordion_core><p class="card-text">{{core.name}}</p></div>-->
                                <b-button block href="#" v-b-toggle="'accordion_core'" variant="info">{{wiredNetwork.name}}</b-button>
                            </b-card-header>
                            <b-collapse id="accordion_core" :visible="wiredNetwork.active" accordion="wired-accordion" role="tabpanel">
                                <b-card-body>
                                    <div class="row mb-2">
                                        <div class="col-xl-3 col-4">
                                            Идентификатор сети:
                                        </div>
                                        <div class="col-xl-9 col-8">
                                            {{wiredNetwork.id || '-'}}
                                        </div>
                                    </div>
                                    <div class="row mb-2">
                                        <div class="col-xl-3 col-4">
                                            Интерфейс:
                                        </div>
                                        <div class="col-xl-9 col-8">
                                            {{wiredNetwork.device || '-'}}
                                        </div>
                                    </div>
                                    <div class="row mb-2">
                                        <div class="col-xl-3 col-4">
                                            Активна:
                                        </div>
                                        <div class="col-xl-9 col-8">
                                            {{wiredNetwork.active}}
                                        </div>
                                    </div>
                                    <div class="row mb-2">
                                        <div class="col-xl-3 col-4">
                                            Автоподключение:
                                        </div>
                                        <div class="col-xl-9 col-8">
                                            {{wiredNetwork.autoconnect}}
                                        </div>
                                    </div>

                                    <!--TODO finish me-->
                                    <div class="row mb-3">
                                        <div class="offset-xl-3 offset-0 col-xl-3 col-4">
                                            <button class="btn btn-block btn-primary">
                                                Подключение к сети&nbsp;<i class="fa" :class="{'fa-angle-down': !wiredNetwork.active, 'fa-angle-up': wiredNetwork.active}"></i>
                                            </button>
                                        </div>
                                        <div class="col-xl-3 col-4">
                                            <button :id="'wiredParamsButton' + index" class="btn btn-block btn-primary" v-b-toggle="'wiredParams' + index">
                                                Настройка параметров&nbsp;<i class="fa fa-angle-down"></i>
                                            </button>
                                        </div>
                                        <div class="col-xl-3 col-4">
                                            <button :disabled="!wiredNetwork.id || password" class="btn btn-block btn-primary" @click="connect(wiredNetwork)">
                                                Подключиться
                                            </button>
                                        </div>
                                    </div>
                                    <b-collapse :id="'wiredParams' + index">
                                        <div class="row mb-2">
                                            <div class="col-xl-3 col-4">
                                                DHCP:
                                            </div>
                                            <div class="col-xl-9 col-8">
                                                <b-form-checkbox v-model="wiredNetwork.requiredParams.ipv4method"  switch>
                                                    <b>(Checked: {{ wiredNetwork.requiredParams.ipv4method }})</b> {{wiredNetwork.requiredParams._ipv4method}}
                                                </b-form-checkbox>
                                            </div>
                                        </div>
                                        <!--TODO add validation like here https://bootstrap-vue.js.org/docs/components/form-input/-->
                                        <div class="row mb-2">
                                            <label class="col-xl-3 col-form-label" :for="'wired' + index + 'ipv4address'">Ipv4 адрес:</label>
                                            <div class="col-xl-9 col-12">
                                                <input :disabled="wiredNetwork.requiredParams.ipv4method"
                                                       :id="'wired' + index + 'ipv4address'"
                                                       :placeholder="'...'"
                                                       v-model="wiredNetwork.requiredParams.ipv4address"
                                                       class="form-control"
                                                       type="text"/>
                                            </div>
                                        </div>
                                        <div class="row mb-2">
                                            <label class="col-xl-3 col-form-label" :for="'wired' + index + 'ipv4gateway'">Ipv4 gateway:</label>
                                            <div class="col-xl-9 col-12">
                                                <input :disabled="wiredNetwork.requiredParams.ipv4method"
                                                       :id="'wired' + index + 'ipv4gateway'"
                                                       :placeholder="'...'"
                                                       v-model="wiredNetwork.requiredParams.ipv4gateway"
                                                       class="form-control"
                                                       type="text"/>
                                            </div>
                                        </div>
                                        <div class="row mb-2">
                                            <label class="col-xl-3 col-form-label" :for="'wired' + index + 'ipv4dns'">Ipv4 dns:</label>
                                            <div class="col-xl-9 col-12">
                                                <input :disabled="wiredNetwork.requiredParams.ipv4method"
                                                       :id="'wired' + index + 'ipv4dns'"
                                                       :placeholder="'...'"
                                                       v-model="wiredNetwork.requiredParams.ipv4dns"
                                                       class="form-control"
                                                       type="text"/>
                                            </div>
                                        </div>
                                        <div class="row mb-2">
                                            <div class="offset-xl-9 offset-md-8 offset-0 col-xl-3 col-md-4 col-12">
                                                <button class="btn btn-success btn-block" @click="modifyConnectionParams(wiredNetwork)">Применить</button>
                                            </div>
                                        </div>
                                    </b-collapse>
                                </b-card-body>
                            </b-collapse>
                        </b-card>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ServerExceptionModel } from '../models/ServerExceptionModel';
import Logger from '../logger';
import Divider from '../components/Divider'

export default {
    name: 'Networks',
    mounted: function() {
        if (this.$store.getters.isAuthenticated) {
            this.loadData();
        } else {
            this.$toaster.error('Для доступа к этой странице необходима авторизация');
            this.$router.push('/login');
        }
    },
    components: {
        'divider': Divider
    },
    methods: {
        async loadData() {
            try {
                this._loader = this.$loading.show();
                const result = await this.$store.state.requestService.getNetworks();
                this.wiredNetworks = result.wiredNetworks;
                this.wirelessNetworks = result.wirelessNetworks;
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Серверная ошибка');
                    Logger.error(err);
                }
                this.wirelessNetworks = [];
                this.wiredNetworks = [];
            }
            this._loader.hide();
        },

        async switchConnection(network) {
            const newNetwork = {};
            // TODO warning modal window + request to connect
            Logger.info(`connecting to ${newNetwork.name} with password ${this.password}`);
            try {
                this._loader = this.$loading.show();
                const res = await this.$store.state.requestService.createWifiConnection(newNetwork.name, this.password);
                if (res) {
                    this.$toaster.success(`Current network is ${newNetwork.name}`);
                }
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Серверная ошибка');
                    Logger.error(err);
                }
            }
            this._loader.hide();
        },

        async connect(network) {
            // TODO warning modal window + request to connect
            Logger.info(`connecting to ${network.name} with password ${this.password}`);
            try {
                this._loader = this.$loading.show();
                let res = false;
                if (this.password) {
                    res = await this.$store.state.requestService.createWifiConnection(network.name, this.password);
                } else if (network.id) {
                    res = await this.$store.state.requestService.connectionUp(network.id)
                } else {
                    this.$toaster.error('Не введено никаких данных для подключения к сети');
                }
                if (res) {
                    this.$toaster.success(`Текущая сеть: ${network.name}`);
                }
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Серверная ошибка');
                    Logger.error(err);
                }
            }
            this.password = '';
            this._loader.hide();
        },
        async modifyConnectionParams(connection) {

        }
    },
    data: () => {
        return {
            wiredNetworks: [],
            wirelessNetworks: [],
            password: '',
            _loader: null
        }
    }
}
</script>

<style scoped>

</style>
