<template>
    <div>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <ul class="navbar-nav">
                <li>
                    <button type="button" class="btn btn-dark">
                        <i class="fa fa-bars"></i>
                    </button>
                </li>
            </ul>

            <div class="navbar-brand">
                Project name
            </div>

            <ul class="navbar-nav ml-auto">
                <li>
                    Current user
                </li>
            </ul>
        </nav>
    </div>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator';

    @Component
    export default class Header extends Vue {}
</script>

<style scoped>
    .navbar-brand {
        margin-left: 15px;
    }
</style>