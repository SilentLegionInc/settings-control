<template>
    <div>
        <div class="mb-3">
            <h2 align="center">Конфигурация сети</h2>
        </div>
        <div v-if="networks.length > 0">
            <div v-for="(network, index) of networks" v-bind:key="index">
                <div class="row" @click="switchDetailed(index)">
                    <div class="offset-md-2 col-md-1">
                        <i class="fa fa-circle" :style="{'color': network.active ? 'green' : 'red'}"></i>
                    </div>
                    <div class="col-md-5">
                        {{network.name}}
                    </div>
                    <div class="col-md-2">
                        signal level: {{network.bars}} ({{network.bars.length}})
                    </div>
                </div>
                <div v-if="network.detail" class="margin-bottom-md">
                    <div class="row">
                        <div class="offset-md-3 col-md-6">
                            <div class="row">
                                <div class="col-md-12">
                                    Защита: {{network.security}}
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-12">
                                    Уровень сигнала: {{network.signal}}
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-12">
                                    Канал: {{network.channel}}
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-12">
                                    Режим: {{network.mode}}
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-12">
                                    Пропускная способность: {{network.rate}}
                                </div>
                            </div>
                            <div class="row" v-if="!network.active">
                                <div class="col-md-8">
                                    <input type="password" v-model="password"
                                           class="form-control" placeholder="Enter password">
                                </div>
                                <div class="col-md-4">
                                    <button v-on:click="connect(index)" class="btn-sm btn-success">Подключиться</button>
                                </div>
                            </div>
                            <!--<div class="row" v-if="network.active">-->
                                <!--<div class="col-md-12">-->
                                    <!--<button v-on:click="disconnect(network)" class="btn-sm btn-danger">Отключиться</button>-->
                                <!--</div>-->
                            <!--</div>-->
                        </div>
                    </div>
                </div>
                <div v-else class="margin-bottom-md">
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ServerExceptionModel } from '../models/ServerExceptionModel';
import Logger from '../logger';

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
    methods: {
        loadData: async function() {
            try {
                this.networks = await this.$store.state.requestService.getNetworks();
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Серверная ошибка');
                    Logger.error(err);
                }
                this.networks = [];
            }
        },
        switchDetailed: function (index) {
            this.networks[index].detail = !this.networks[index].detail;
        },
        disconnect: function (network) {
            // TODO warning modal window + request to disconnect, i think we don't need this
            Logger.info(`disconnecting from ${network.name}`)
        },
        connect: async function (index) {
            const newNetwork = this.networks[index];
            // TODO warning modal window + request to connect
            Logger.info(`connecting to ${newNetwork.name} with password ${this.password}`)
            try {
                const res = await this.$store.state.requestService.changeNetwork(newNetwork.name, this.password);
                if (res) {
                    this.$toaster.success(`Current network is ${newNetwork.name}`);
                    this.networks.map(net => {
                        net.active = false;
                        return net;
                    });
                    // TODO check this thing, may be need to reload wifi list
                    this.networks[index].active = true;
                }
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Серверная ошибка');
                    Logger.error(err);
                }
            }
        }
    },
    data: () => {
        return {
            networks: [],
            raw_networks: [],
            password: ''
        }
    }
}
</script>

<style scoped>

</style>
