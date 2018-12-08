<template>
    <div class="sidebar" v-bind:style="currentStyle">
        <a href="#" class="closebtn clickable" @click="close">
            <i class="fa fa-times" aria-hidden="true"></i>
        </a>

        <ul>
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
                <router-link class="clickable" to="/logs" @click.native="close">
                    Logs
                </router-link>
            </li>
        </ul>
    </div>
</template>

<script>
    export default {
        name: 'Sidebar',
        props: ['isOpen'],
        data: function () {
            return {
                monitorIsOpen: false
            }
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
