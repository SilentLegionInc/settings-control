<template>
    <div>
        <nav class="navbar">
            <ul class="navbar-nav">
                <li>
                    <a href="#" @click="onHamburgerClicked">
                        <i class="fa fa-bars clickable" style="font-size: 180%"></i>
                    </a>
                </li>
            </ul>

            <div class="navbar-brand">
                ToolBelt
            </div>

            <ul class="navbar-nav ml-auto">
                <li>
                    <router-link class="clickable" to="/">
                        {{$store.state.robotLabel}}
                    </router-link>
                </li>
            </ul>
        </nav>
    </div>
</template>

<script>
export default {
    name: 'Header',
    methods: {
        onHamburgerClicked() {
            this.$emit('onHamburger');
        }
    }
}
</script>

<style scoped lang="scss">
    .navbar-brand {
        margin-left: 15px;
        font-weight: bold;
        font-size: 25px;
        font-family: BookmanBold, serif;
    }

    .navbar {
        background-color: #6f7bbf;
        padding-top: 4px;
        padding-bottom: 4px;
    }
</style>
