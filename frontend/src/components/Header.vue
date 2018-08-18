<template>
    <div>
        <nav class="navbar">
            <ul class="navbar-nav">
                <li>
                    <button type="button" class="btn btn-primary" @click="onHamburgerClicked">
                        <i class="fa fa-bars"></i>
                    </button>
                </li>
            </ul>

            <div class="navbar-brand">
                Configuration tool
            </div>

            <ul class="navbar-nav ml-auto">
                <li>
                    <router-link id="machine-name" to="/">
                        АМТС
                    </router-link>
                </li>
            </ul>
        </nav>
    </div>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator';

    @Component
    export default class Header extends Vue {
        private onHamburgerClicked() {
            this.$emit('onHamburger');
        }
    }
</script>

<style scoped>
    .navbar-brand {
        margin-left: 15px;
        font-weight: bold;
        font-size: 25px;
    }
    .navbar {
        background: #7395AE;
    }

     #machine-name {
         font-weight: bolder;
         text-decoration: none;
         font-size: 20px;
         color: black;
         transition: color 0.3s;
     }

    #machine-name:hover {
        color: #B0A295;
    }
</style>