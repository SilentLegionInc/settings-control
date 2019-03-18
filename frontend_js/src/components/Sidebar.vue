<template>
    <div class="sidebar" v-bind:class="{'sidebar-opened': isOpen, 'sidebar-closed': !isOpen}">
        <a href="#" class="closebtn clickable" @click="close">
            <i class="fa fa-times" aria-hidden="true"></i>
        </a>

        <ul>
            <li>
                <router-link class="clickable" to="/" @click.native="close">
                    Домашняя страница
                </router-link>
            </li>

            <li>
                <router-link class="clickable" to="/system_info" @click.native="close">
                    Нагрузка
                </router-link>
            </li>

            <li>
                <router-link class="clickable" to="/monitoring_navigation" @click.native="close">
                    Мониторинг
                </router-link>
            </li>

            <li>
                <router-link class="clickable" to="/logs" @click.native="close">
                    Логи
                </router-link>
            </li>
        </ul>

        <ul>
            <li v-if="$store.getters.isAuthenticated">
                <router-link class="clickable" to="/settings" @click.native="close">
                    Конфигурация ядра
                </router-link>
            </li>

            <li v-if="$store.getters.isAuthenticated">
                <router-link class="clickable" to="/server_settings" @click.native="close">
                    Конфигурация сервера
                </router-link>
            </li>

            <li v-if="$store.getters.isAuthenticated">
                <router-link class="clickable" to="/wifi" @click.native="close">
                    Сети
                </router-link>
            </li>

            <li v-if="$store.getters.isAuthenticated">
                <router-link class="clickable" to="/modules" @click.native="close">
                    Модули
                </router-link>
            </li>
        </ul>

        <ul>
            <li v-if="!this.$store.getters.isAuthenticated">
                <router-link class="clickable" to="/login" @click.native="close">
                    Вход
                </router-link>
            </li>
            <li v-if="this.$store.getters.isAuthenticated">
                <a class="clickable" @click="logout()">
                    Выход
                </a>
            </li>
        </ul>
    </div>
</template>

<script>
import { ServerExceptionModel } from '../models/ServerExceptionModel';
import Logger from '../logger';

export default {
    name: 'Sidebar',
    props: ['isOpen'],
    data: function () {
        return {
            monitorIsOpen: false
        }
    },

    methods: {
        onClick: function(event) {
            if (!this.$el.contains(event.target) && this.isOpen) {
                this.close();
            }
        },

        close: function() {
            this.$emit('closeSidebar');
        },

        switchMonitorList: function() {
            this.monitorIsOpen = !this.monitorIsOpen;
        },

        async logout() {
            this.close();
            try {
                await this.$store.dispatch('deauthorize');
                this.$router.push('/');
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

    created: function() {
        window.addEventListener('click', this.onClick);
    },

    beforeDestroy: function() {
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
        padding-top: 40px;
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

    .sidebar-opened {
        @media  only screen and (min-resolution: 165dpi) and (max-resolution: 168dpi),
        only screen and (min-resolution: 155dpi) and (max-resolution: 160dpi),
        only screen and (min-resolution: 134dpi) and (max-resolution: 144dpi),
        only screen and (min-resolution: 120dpi) and (max-resolution: 130dpi),
        only screen and (max-resolution: 116dpi) {
            min-width: 300px;
            width: 22%;
        }

        @media  only screen and (min-resolution: 117dpi) and (max-resolution: 119dpi),
                only screen and (min-resolution: 131dpi) and (max-resolution: 133dpi),
                only screen and (min-resolution: 145dpi) and (max-resolution: 154dpi),
                only screen and (min-resolution: 162dpi) and (max-resolution: 164dpi),
                only screen and (min-resolution: 169dpi) {
            min-width: 100%;
            width: 100%;
        }
    }

    .sidebar-closed {
        min-width: 0;
        width: 0;
    }
</style>
