<template>
    <div>
        <div class="mb-3">
            <h2 align="center">Конфигурация сети</h2>
        </div>
        <div v-if="networks.length > 0">
            <div v-for="(network, index) of networks" v-bind:key="index" v-on:click="switchDetailed(index)">
                <div class="row">
                    <div class="offset-md-2 col-md-1">
                        <i class="fa fa-circle" v-bind:style="{'color': network.active ? 'green' : 'red'}"></i>
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
                                <div class="col-md-12">
                                    <button v-on:click="connect(network)" class="btn-sm btn-success">Подключиться</button>
                                </div>
                            </div>
                            <div class="row" v-if="network.active">
                                <div class="col-md-12">
                                    <button v-on:click="disconnect(network)" class="btn-sm btn-danger">Отключиться</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-else class="margin-bottom-md">
                </div>
            </div>
        </div>

        <app-login-modal @logged="loadData"></app-login-modal>

    </div>
</template>

<script>
import LoginModal from '@/components/LoginModal';
import { ServerExceptionModel } from '../models/ServerExceptionModel';
import logger from '../logger';

export default {
    name: 'Networks',
    components: {
        'app-login-modal': LoginModal
    },
    mounted: function() {
        if (this.$store.getters.isAuthenticated) {
            this.loadData();
        }
    },
    methods: {
        loadData: async function() {
            try {
                logger.info(this.$store);
                this.networks = await this.$store.state.requestService.getNetworks();
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Internal server error');
                    logger.error(err);
                }
                this.networks = [];
            }
        },
        switchDetailed: function (index) {
            this.networks[index].detail = !this.networks[index].detail;
        },
        disconnect: function (network) {
            // TODO warning modal window + request to disconnect
            logger.info(`disconnecting from ${network.name}`)
        },
        connect: function (network) {
            // TODO warning modal window + request to connect
            logger.info(`connecting to ${network.name}`)
        }
    },
    data: () => {
        return {
            networks: [],
            raw_networks: []
        }
    }
}
</script>

<style scoped>

</style>
