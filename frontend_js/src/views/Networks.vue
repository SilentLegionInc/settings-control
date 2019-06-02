<template>
    <div class="container-fluid">
        <div class="mb-3">
            <h2 align="center">Конфигурация сети &nbsp;<i class="fas fa-sync" @click="loadData()"></i></h2>
        </div>
        <divider>
            <h5>
            Беспроводные соединения &nbsp;
                <i class="fas fa-eraser" style="color: #dc3545" @click="dropAllWirelessConfirmation()"></i>
            </h5>
        </divider>
        <div v-if="wirelessNetworks.length > 0" role="tablist">
            <div v-for="(network, index) of wirelessNetworks" v-bind:key="index">
                <div class="row"  style="margin: auto">
                    <div class="col-xl-8 offset-xl-2 offset-0 col-12">
                        <b-card no-body class="mb-1">
                            <b-card-header header-tag="header" class="p-1" role="tab">
                                <b-button block href="#"
                                          v-b-toggle="'wireless' + index"
                                          variant="info">
                                    {{network.name}} ({{network.signalLevel}} <i class="fas fa-signal"></i>)
                                </b-button>
                            </b-card-header>
                            <b-collapse :ref="'wireless' + index" :id="'wireless' + index" :visible="network.active" accordion="wireless-accordion" role="tabpanel">
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
                                            Тип защиты:
                                        </div>
                                        <div class="col-xl-9 col-8">
                                            {{network.security || '-'}}
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
                                    <div class="row mb-2" v-if="!network.active">
                                        <label class="col-xl-3 col-form-label mb-1" :for="'wireless'+index+'password'">Пароль для подключения:</label>
                                        <div class="col-xl-9 col-12 mb-1">
                                            <input :id="'wireless'+index+'password'" type="password" v-model="network.password"
                                                   class="form-control" placeholder="Enter password">
                                        </div>
                                    </div>
                                    <div class="row mb-3">
                                        <div class="offset-xl-3 offset-0 col-xl-3 col-4">
                                            <button :disabled="network.active || !network.id" class="btn btn-block btn-danger" @click="deleteNetworkConfirmation(network)">
                                                Забыть подключение
                                            </button>
                                        </div>
                                        <div class="col-xl-3 col-4">
                                            <button :id="'wirelessParamsButton' + index"
                                                    :disabled="!network.id"
                                                    class="btn btn-block btn-primary"
                                                    v-b-toggle="'wirelessParams' + index"
                                                    @click="changeCollapseStatus(`wirelessParams${index}`)">
                                                Настройка параметров&nbsp;
                                                <i class="fa" :class="{'fa-angle-down': !collapseStatuses[`wirelessParams${index}`],
                                                'fa-angle-up': collapseStatuses[`wirelessParams${index}`]}"></i>
                                            </button>
                                        </div>
                                        <div class="col-xl-3 col-4">
                                            <button :disabled="(!network.id && !network.password) || network.active"
                                                    class="btn btn-block btn-success"
                                                    @click="changeNetworkConfirmation(network)">
                                                Подключиться
                                            </button>
                                        </div>
                                    </div>
                                    <b-collapse :id="'wirelessParams' + index" :ref="'wirelessParams' + index">
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
                                        <div class="row mb-2">
                                            <div class="offset-xl-9 offset-md-8 offset-0 col-xl-3 col-md-4 col-12">
                                                <button class="btn btn-success btn-block" @click="modifyConnectionParams(network)">Применить</button>
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
        <div v-else>
            <div class="row"  style="margin: auto">
                <div class="col-xl-8 offset-xl-2 offset-0 col-12">
                    Нет доступных беспроводных сетей или не подключен адаптер
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
                                            <button :disabled="wiredNetwork.active || !wiredNetwork.id" class="btn btn-block btn-danger" @click="deleteNetworkConfirmation(wiredNetwork)">
                                                Забыть подключение
                                            </button>
                                        </div>
                                        <div class="col-xl-3 col-4">
                                            <button :id="'wiredParamsButton' + index"
                                                    class="btn btn-block btn-primary"
                                                    v-b-toggle="'wiredParams' + index"
                                                    @click="changeCollapseStatus(`wiredParams${index}`)">
                                                Настройка параметров&nbsp;
                                                <i class="fa" :class="{'fa-angle-down': !collapseStatuses[`wiredParams${index}`],
                                                'fa-angle-up': collapseStatuses[`wiredParams${index}`]}"></i>
                                            </button>
                                        </div>
                                        <div class="col-xl-3 col-4">
                                            <button :disabled="(!wiredNetwork.id && !password) || wiredNetwork.active" class="btn btn-block btn-success" @click="connect(wiredNetwork)">
                                                Подключиться
                                            </button>
                                        </div>
                                    </div>
                                    <b-collapse :id="'wiredParams' + index" :ref="'wiredParams' + index">
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
        <div v-else>
            <div class="row"  style="margin: auto">
                <div class="col-xl-8 offset-xl-2 offset-0 col-12">
                    Нет доступных проводных сетей или не подключен адаптер
                </div>
            </div>
        </div>

        <networks-modal ref="change_network_modal"
                        id="change_network_modal"
                        title="Переключение сети"
                        @ok="connect(tempNetwork)"
        >
            <b>Внимание!</b>
            При изменении сети, необходимо будет на клиентском устройстве также переключиться в новую сеть и перейти по новому адресу клиента.
        </networks-modal>

        <networks-modal ref="drop_all_modal"
                        id="drop_all_modal"
                        title="Забыть все беспроводные соединения"
                        @ok="dropAllWirelessConnections()"
        >
            <b>Внимание!</b>
            Будут сброшены все беспроводные соединения.
        </networks-modal>

        <networks-modal ref="drop_one_modal"
                        id="drop_one_modal"
                        title="Забыть соединение"
                        @ok="deleteConnection(networkToDelete)"
        >
            <b>Внимание!</b>
            Будет сброшена вся информация об соединении {{networkToDelete.name}}.
        </networks-modal>
    </div>
</template>

<script>
import { ServerExceptionModel } from '../models/ServerExceptionModel';
import Logger from '../logger';
import Divider from '../components/Divider'
import NetworksModal from '../components/NetworksModal';

export default {
    name: 'Networks',
    components: {
        'divider': Divider,
        'networks-modal': NetworksModal
    },
    mounted: function() {
        if (this.$store.getters.isAuthenticated) {
            this.loadData();
        } else {
            this.$toaster.error('Для доступа к этой странице необходима авторизация');
            this.$router.push('/login');
        }
    },
    data: () => {
        return {
            wiredNetworks: [],
            wirelessNetworks: [],
            _loader: null,
            timeoutToRedirectMsecs: 7000,
            collapseStatuses: {},
            tempNetwork: {},
            networkToDelete: {}
        }
    },
    methods: {
        async loadData() {
            const loader = this.$loading.show();
            try {
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
            loader.hide();
        },

        // По истечению таймаута мы вынуждены редиректить пользователя на домашнюю страницу, т.к. нет вомзможности
        // получить ответ от сервера из другой сети
        timeoutRedirection(loaderToHide, newNetwork) {
            this.$router.push('/');
            loaderToHide.hide();
            newNetwork.password = '';
            this.tempNetwork = {};
            this.$toaster.success(`Текущая сеть: ${newNetwork.name}`);
        },

        async connect(network) {
            const loader = this.$loading.show();
            let timeout = null;
            try {
                let res = false;
                if (network.password) {
                    Logger.info(`Connecting to ${network.name} with password ${network.password}. Timeout ${this.timeoutToRedirectMsecs} msecs.`);
                    timeout = setTimeout(this.timeoutRedirection, this.timeoutToRedirectMsecs, loader, network);
                    res = await this.$store.state.requestService.createWifiConnection(network.name, network.password);
                } else if (network.id) {
                    Logger.info(`Connecting to ${network.name} via known id ${network.id}. Timeout ${this.timeoutToRedirectMsecs} msecs.`);
                    timeout = setTimeout(this.timeoutRedirection, this.timeoutToRedirectMsecs, loader, network);
                    res = await this.$store.state.requestService.connectionUp(network.id);
                } else {
                    this.$toaster.error('Не введено никаких данных для подключения к сети');
                }
                if (res) {
                    clearTimeout(timeout);
                    await this.loadData();
                    this.$toaster.success(`Текущая сеть: ${network.name}`);
                }
            } catch (err) {
                clearTimeout(timeout);
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Серверная ошибка');
                    Logger.error(err);
                }
            }
            network.password = '';
            this.tempNetwork = {};
            loader.hide();
        },

        deleteNetworkConfirmation(network) {
            this.networkToDelete = network;
            this.$refs.drop_one_modal.showModal();
        },

        async deleteConnection(network) {
            const loader = this.$loading.show();
            try {
                const res = this.$store.state.requestService.deleteConnection(network.id);
                if (res) {
                    this.$toaster.success(`Соединение ${network.name} успешно удалено`);
                    network.id = null;
                } else {
                    this.$toaster.error(`Ошибка удаления сети ${network.name}`);
                }
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Серверная ошибка');
                    Logger.error(err);
                }
            }
            this.networkToDelete = {};
            loader.hide();
        },

        changeNetworkConfirmation(network) {
            // TODO add timeout to change network then redirect to login
            this.tempNetwork = network;
            this.$refs.change_network_modal.showModal();
        },

        async modifyConnectionParams(network) {
            const loader = this.$loading.show();
            try {
                const res = await this.$store.state.requestService.modifyConnectionParams(network.id,
                    { ...network.requiredParams.toPythonDict(), ...network.additionalParams });
                if (res) {
                    this.$toaster.success(`Соединение ${network.name} успешно модифицированно`);
                    network.id = null;
                } else {
                    this.$toaster.error(`Ошибка модификации параметров ${network.name}`);
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

        async dropAllWirelessConfirmation() {
            this.$refs.drop_all_modal.showModal();
        },

        async dropAllWirelessConnections() {
            const loader = this.$loading.show();
            try {
                const res = await this.$store.state.requestService.deleteAllWirelessConnections();
                if (res) {
                    await this.loadData();
                    this.$toaster.success(`Все беспроводные соединения успешно стерты`);
                } else {
                    this.$toaster.error(`Не удалось очистить беспроводные соединения`);
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

        changeCollapseStatus(collapseId) {
            if (this.collapseStatuses[collapseId]) {
                this.collapseStatuses[collapseId] = !this.collapseStatuses[collapseId]
            } else {
                this.$set(this.collapseStatuses, collapseId, true);
            }
        }
    }
}
</script>

<style scoped>

</style>
