<template>
    <div class="sidebar" v-bind:class="{'sidebar-opened': isOpen, 'sidebar-closed': !isOpen}">
        <a href="#" class="hamburgerbtn clickable" @click="close">
            <i class="fa fa-bars" aria-hidden="true"></i>
        </a>
        <a href="#" class="closebtn clickable" @click="close">
            <i class="fa fa-times" aria-hidden="true"></i>
        </a>
        <div v-if="$store.getters.isAuthenticated">
            <divider text="Конфигурация"></divider>
            <ul>
                <li>
                    <router-link class="clickable" to="/settings" @click.native="close">
                        <div class="row">
                            <div class="col-1 col-sm-1 col-md-1 col-lg-1 col-xl-1 pl-0" align="center">
                                <i class="fas fa-truck-monster"></i>
                            </div>
                            <div class="col-11 col-sm-11 col-md-11 col-lg-11 col-xl-11">
                                Конфигурация ядра
                            </div>
                        </div>
                    </router-link>
                </li>
                <li>
                    <router-link class="clickable" to="/server_settings" @click.native="close">
                        <div class="row">
                            <div class="col-1 col-sm-1 col-md-1 col-lg-1 col-xl-1 pl-0" align="center">
                                <i class="fas fa-sliders-h"></i>
                            </div>
                            <div class="col-11 col-sm-11 col-md-11 col-lg-11 col-xl-11">
                                Конфигурация сервера
                            </div>
                        </div>
                    </router-link>
                </li>
                <li>
                    <router-link class="clickable" to="/wifi" @click.native="close">
                        <div class="row">
                            <div class="col-1 col-sm-1 col-md-1 col-lg-1 col-xl-1 pl-0" align="center">
                                <i class="fas fa-broadcast-tower"></i>
                            </div>
                            <div class="col-11 col-sm-11 col-md-11 col-lg-11 col-xl-11">
                                Сети
                            </div>
                        </div>
                    </router-link>
                </li>
                <li>
                    <router-link class="clickable" to="/modules" @click.native="close">
                        <div class="row">
                            <div class="col-1 col-sm-1 col-md-1 col-lg-1 col-xl-1 pl-0" align="center">
                                <i class="fas fa-box-open"></i>
                            </div>
                            <div class="col-11 col-sm-11 col-md-11 col-lg-11 col-xl-11">
                                Модули
                            </div>
                        </div>
                    </router-link>
                </li>
            </ul>
        </div>
        <div v-if="$store.getters.isServerConnected">
            <divider text="Мониторинг"></divider>
            <ul>
                <li>
                    <router-link class="clickable" to="/system_info" @click.native="close">
                        <div class="row">
                            <div class="col-1 col-sm-1 col-md-1 col-lg-1 col-xl-1 pl-0" align="center">
                                <i class="fas fa-thermometer"></i>
                            </div>
                            <div class="col-11 col-sm-11 col-md-11 col-lg-11 col-xl-11">
                                Нагрузка системы
                            </div>
                        </div>
                    </router-link>
                </li>
                <li>
                    <router-link class="clickable" to="/monitoring_navigation" @click.native="close">
                        <div class="row">
                            <div class="col-1 col-sm-1 col-md-1 col-lg-1 col-xl-1 pl-0" align="center">
                                <i class="far fa-chart-bar"></i>
                            </div>
                            <div class="col-11 col-sm-11 col-md-11 col-lg-11 col-xl-11">
                                Данные датчиков
                            </div>
                        </div>
                    </router-link>
                </li>
                <li>
                    <router-link class="clickable" to="/logs" @click.native="close">
                        <div class="row">
                            <div class="col-1 col-sm-1 col-md-1 col-lg-1 col-xl-1 pl-0" align="center">
                                <i class="fas fa-book"></i>
                            </div>
                            <div class="col-11 col-sm-11 col-md-11 col-lg-11 col-xl-11">
                                Логи ядра
                            </div>
                        </div>
                    </router-link>
                </li>
            </ul>
        </div>
        <div>
            <divider text="Авторизация"></divider>
            <ul>
                <li v-if="!this.$store.getters.isAuthenticated">
                    <router-link class="clickable" to="/login" @click.native="close">
                        <div class="row">
                            <div class="col-1 col-sm-1 col-md-1 col-lg-1 col-xl-1 pl-0" align="center">
                                <i class="fa fa-key"></i>
                            </div>
                            <div class="col-11 col-sm-11 col-md-11 col-lg-11 col-xl-11">
                                Вход
                            </div>
                        </div>
                    </router-link>
                </li>
                <li v-if="this.$store.getters.isAuthenticated">
                    <router-link class="clickable" to="/" @click.native="logout()">
                        <div class="row">
                            <div class="col-1 col-sm-1 col-md-1 col-lg-1 col-xl-1 pl-0" align="center">
                                <i class="fa fa-lock"></i>
                            </div>
                            <div class="col-11 col-sm-11 col-md-11 col-lg-11 col-xl-11">
                                Выход
                            </div>
                        </div>
                    </router-link>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
import { ServerExceptionModel } from '../models/ServerExceptionModel';
import Divider from './Divider';
import Logger from '../logger';

export default {
    name: 'Sidebar',
    props: ['isOpen'],
    components: {
        'divider': Divider
    },
    data() {
        return {
            monitorIsOpen: false
        }
    },
    methods: {
        onClick(event) {
            if (!this.$el.contains(event.target) && this.isOpen) {
                this.close();
            }
        },

        close() {
            this.$emit('closeSidebar');
        },

        switchMonitorList() {
            this.monitorIsOpen = !this.monitorIsOpen;
        },

        async logout() {
            this.close();
            try {
                await this.$store.dispatch('deauthorize');
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

    created() {
        window.addEventListener('click', this.onClick);
    },

    beforeDestroy() {
        window.removeEventListener('click', this.onClick);
    }
}
</script>

<style scoped lang="scss">
    .sidebar {
        height: 100%;
        position: fixed;
        z-index: 100;
        top: 0;
        left: 0;
        background-color: #7b88d3;
        overflow-x: hidden;
        transition: 0.5s;
        padding-top: 50px;
        white-space: nowrap;
    }

    .sidebar ul {
        padding-left: 30px;
    }

    .sidebar ul li {
        list-style-type: none;
    }

    .sidebar a {
        font-size: 25px;
    }

    .sidebar .closebtn {
        position: absolute;
        top: 0;
        right: 0;
        font-size: 30px;
        padding: 0 10px 0 0;
    }

    .sidebar .hamburgerbtn {
        position: absolute;
        top: 0;
        left: 0;
        font-size: 180%;
        padding: 3px 10px 0 15px;
    }

    .sidebar-opened {
        @media (min-width:320px)  {
            /* smartphones, iPhone, portrait 480x320 phones */
            min-width: 100%;
            width: 100%;
        }
        @media (min-width:481px)  {
            /* portrait e-readers (Nook/Kindle), smaller tablets @ 600 or @ 640 wide. */
            min-width: 340px;
            width: 70%;
        }
        @media (min-width:641px)  {
            /* portrait tablets, portrait iPad, landscape e-readers, landscape 800x480 or 854x480 phones */
            min-width: 340px;
            width: 50%;
        }
        @media (min-width:961px)  {
            /* tablet, landscape iPad, lo-res laptops ands desktops */
            min-width: 340px;
            width: 35%;
        }
        @media (min-width:1025px) {
            /* big landscape tablets, laptops, and desktops */
            min-width: 360px;
            width: 30%;
        }
        @media (min-width:1281px) {
            /* hi-res laptops and desktops */
            min-width: 360px;
            width: 25%;
        }
    }

    .sidebar-closed {
        min-width: 0;
        width: 0;
    }
</style>
