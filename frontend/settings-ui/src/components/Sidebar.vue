<template>
    <div class="sidebar" v-bind:style="currentStyle">
        <a href="#" class="closebtn" @click="close"><i class="fa fa-times" aria-hidden="true"></i></a>
        <a href="#">Element 1</a>
        <a href="#">Element 2</a>
        <a href="#">Element 3</a>
        <a href="#">Element 4</a>
    </div>
</template>

<script lang="ts">
    import {Component, Prop, Vue} from 'vue-property-decorator';

    @Component
    export default class Sidebar extends Vue {
        @Prop() private isOpen: boolean = false;

        get currentStyle(): object {
            return {
                'width': this.isOpen ? '20%' : '0',
                'min-width': this.isOpen ? '200px' : '0',
            };
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
        padding-top: 30px;
        white-space: nowrap;
    }

    .sidebar a {
        padding: 8px 8px 8px 32px;
        text-decoration: none;
        font-size: 25px;
        color: black;
        display: block;
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
</style>