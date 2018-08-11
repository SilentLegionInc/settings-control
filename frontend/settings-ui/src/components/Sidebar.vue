<template>
    <div class="sidebar">
        <ul class="sidebar-nav">
            <li>
                <a href="#">Element 1</a>
            </li>

            <li>
                <a href="#">Element 2</a>
            </li>

            <li>
                <a href="#">Element 3</a>
            </li>

            <li>
                <a href="#">Element 4</a>
            </li>
        </ul>
    </div>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator';

    @Component
    export default class Sidebar extends Vue {}
</script>

<style scoped lang="scss">
    .sidebar {
        background: lightgray;
        height: 100%;
    }

    .sidebar-nav {
        margin: 0;
        padding: 0;
    }

    .sidebar-nav li {
        text-indent: 20px;
        line-height: 40px;
    }

    .sidebar-nav li a {
        color: black;
    }
</style>