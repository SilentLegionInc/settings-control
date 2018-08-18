<template>
    <div class="sidebar" v-bind:style="currentStyle">
        <a href="#" class="closebtn" @click="close">
            <i class="fa fa-times" aria-hidden="true"></i>
        </a>

        <ul>
            <li>
                <a href="#" @click="switchMonitorList">
                    Мониторинг

                    <transition name="flip" mode="out-in">
                        <i v-if="!monitorIsOpen" key="1" class="fa fa-chevron-down" aria-hidden="true"></i>
                        <i v-else key="2" class="fa fa-chevron-up" aria-hidden="true"></i>
                    </transition>
                </a>

                <transition name="monitor">
                    <ul v-if="monitorIsOpen" class="list-container">
                        <li>
                            <router-link to="/chart_statistics">
                                Графики
                            </router-link>
                        </li>

                        <li>
                            <router-link to="/table_statistics">
                                Таблицы
                            </router-link>
                        </li>
                    </ul>
                </transition>
            </li>

            <li>
                <router-link to="/settings">
                    Конфигурация
                </router-link>
            </li>
        </ul>
    </div>
</template>

<script lang="ts">
    import { Component, Prop, Vue } from 'vue-property-decorator';

    @Component
    export default class Sidebar extends Vue {
        @Prop() private isOpen: boolean = false;

        private monitorIsOpen: boolean = false;

        get currentStyle(): object {
            return {
                'width': this.isOpen ? '20%' : '0',
                'min-width': this.isOpen ? '250px' : '0',
            };
        }

        get monitorListStyle(): object {
            return { 'height': this.monitorIsOpen ? '20%' : '0' };
        }

        private created() {
            window.addEventListener('click', this.onClick);
        }

        private beforeDestroy() {
            window.removeEventListener('click', this.onClick);
        }

        private onClick(e: any) {
            if (!this.$el.contains(e.target) && this.isOpen) {
                this.close();
            }
        }

        private close() {
            this.$emit('closeSidebar');
        }

        private switchMonitorList() {
            this.monitorIsOpen = !this.monitorIsOpen;
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
        background-color: #e6e8e9;
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
        text-decoration: none;
        font-size: 25px;
        color: black;
        transition: 0.3s;
    }

    .sidebar a:hover {
        color: darkgrey;
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