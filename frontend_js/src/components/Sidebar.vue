<template>
    <div class="sidebar" v-bind:style="currentStyle">
        <a href="#" class="closebtn clickable" @click="close">
            <i class="fa fa-times" aria-hidden="true"></i>
        </a>

        <ul>
            <li>
                <router-link class="clickable" to="/">Home</router-link>
            </li>
            <li>
                <a href="#" class="clickable" @click="switchMonitorList">
                    Statistics

                    <transition name="flip" mode="out-in">
                        <i v-if="!monitorIsOpen" key="1" class="fa fa-chevron-down" aria-hidden="true"></i>
                        <i v-else key="2" class="fa fa-chevron-up" aria-hidden="true"></i>
                    </transition>
                </a>

                <transition name="monitor">
                    <ul v-if="monitorIsOpen" class="list-container">
                        <li>
                            <router-link class="clickable" to="/chart_statistics" @click.native="close">
                                Charts
                            </router-link>
                        </li>

                        <li>
                            <router-link class="clickable" to="/table_statistics" @click.native="close">
                                Tables
                            </router-link>
                        </li>
                    </ul>
                </transition>
            </li>

            <li>
                <router-link class="clickable" to="/settings" @click.native="close">
                    Configuration
                </router-link>
            </li>

            <li>
                <router-link class="clickable" to="/wifi" @click.native="close">
                    Network
                </router-link>
            </li>

            <li>
                <router-link class="clickable" to="/modules" @click.native="close">
                    Module
                </router-link>
            </li>

            <li>
                <router-link class="clickable" to="/monitoring_navigation" @click.native="close">
                    Monitoring
                </router-link>
            </li>

            <li>
                <router-link class="clickable" to="/logs" @click.native="close">
                    Logs
                </router-link>
            </li>
        </ul>
        <ul>
            <li v-if="!this.$store.getters.isAuthenticated">
                <a class="clickable" @click="login()">Log in</a>
            </li>
            <li v-if="this.$store.getters.isAuthenticated">
                <a class="clickable" @click="logout()">Log out</a>
            </li>
            <li v-if="this.$store.getters.isAuthenticated">
                <router-link class="clickable" to="/change_password">Change password</router-link>
            </li>
        </ul>
        <app-login-modal ref="modal_window" :open-on-mount="false"></app-login-modal>
    </div>
</template>

<script>
import { ServerExceptionModel } from '../models/ServerExceptionModel';
import Logger from '../logger';
import LoginModal from './LoginModal';

export default {
    name: 'Sidebar',
    props: ['isOpen'],
    data: function () {
        return {
            monitorIsOpen: false
        }
    },
    components: {
        'app-login-modal': LoginModal
    },
    computed: {
        currentStyle: function() {
            return {
                'width': this.isOpen ? '20%' : '0',
                'min-width': this.isOpen ? '250px' : '0'
            };
        },

        monitorListStyle: function() {
            return { 'height': this.monitorIsOpen ? '20%' : '0' };
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

        login() {
            this.$refs.modal_window.showModal();
        },

        async logout() {
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

    .list-container {
        overflow: hidden;
    }

    .flip-enter, .flip-leave-to {
        transform: rotateX(90deg);
    }

    .flip-leave, .flip-enter-to {
        transform: rotateX(0deg);
    }

    .flip-enter-active, .flip-leave-active {
        transition: transform 0.2s;
    }

    .monitor-enter, .monitor-leave-to {
        height: 0;
    }

    .monitor-enter-to, .monitor-leave {
        height: 73px;
    }

    .monitor-enter-active, .monitor-leave-active {
        transition: height 0.4s;
    }
</style>
