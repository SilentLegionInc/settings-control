<template>
    <div class="sidebar" v-bind:style="currentStyle">
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
            <li>
                <router-link class="clickable" to="/connect_to_server" @click.native="close">
                    Выбор сервера
                </router-link>
            </li>

            <li v-if="$store.getters.isAuthenticated">
                <router-link class="clickable" to="/settings" @click.native="close">
                    Конфигурация ядра
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

            <li v-if="$store.getters.isAuthenticated">
                <router-link class="clickable" to="/server_settings" @click.native="close">
                    Конфигурация сервера
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
            <li v-if="this.$store.getters.isAuthenticated">
                <router-link class="clickable" to="/change_password" @click.native="close">
                    Смена пароля
                </router-link>
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
    computed: {
        currentStyle: function() {
            return {
                'width': this.isOpen ? '20%' : '0',
                'min-width': this.isOpen ? '300px' : '0'
            };
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

        // login() {
        //     this.close();
        //     this.$refs.modal_window.showModal();
        // },

        async logout() {
            this.close();
            try {
                await this.$store.dispatch('deauthorize');
                this.$router.push('/');
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Internal server error');
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
        z-index: 1;
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
</style>
