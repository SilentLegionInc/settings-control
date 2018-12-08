<template>
    <div id="app">
        <app-header @onHamburger="onSidebarOpened"></app-header>

        <app-sidebar :isOpen="sidebarIsOpened" @closeSidebar="onSidebarClosed"></app-sidebar>

        <router-view id="app-content"/>

        <app-footer id="app-footer"></app-footer>
    </div>
</template>

<style lang="scss">
    html, body {
        height: 100%;
    }

    #app {
        display: flex;
        flex-direction: column;
        height: 100%;
        font-family: Apercu, serif;
    }

    #app-content {
        padding: 10px;
        margin: 0;
        flex: 1 0 auto;
        background: #E8EBEA;
    }

    #app-footer {
        flex-shrink: 0;
    }
</style>
