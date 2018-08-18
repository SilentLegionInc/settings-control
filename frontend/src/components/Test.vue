<template>
    <div>
        <h1>
            Test page
        </h1>

        <div class="row">
            <div class="col-md-1" align="center">
                <i class="fa fa-tint my-anim" :class="{ 'my-anim-selected': activeElement === 0 }" @click="clicked(0)"></i>
            </div>

            <div class="col-md-1" align="center">
                <i class="fa fa-male my-anim" :class="{ 'my-anim-selected': activeElement === 1 }" @click="clicked(1)"></i>
            </div>

            <div class="col-md-1" align="center">
                <i class="fa fa-lock my-anim" :class="{ 'my-anim-selected': activeElement === 2 }" @click="clicked(2)"></i>
            </div>

            <div class="col-md-1" align="center">
                <i class="fa fa-user my-anim" :class="{ 'my-anim-selected': activeElement === 3 }" @click="clicked(3)"></i>
            </div>

            <div class="col-md-1" align="center">
                <i class="fa fa-plus my-anim" :class="{ 'my-anim-selected': activeElement === 4 }" @click="clicked(4)"></i>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator';

    @Component
    export default class Test extends Vue {
        private activeElement: number = -1;

        private clicked(index: number) {
            index = Number(index);
            if (this.activeElement === index) {
                this.activeElement = -1;
            } else {
                this.activeElement = index;
            }
        }
    }
</script>

<style scoped lang="scss">
    .my-anim {
        transition: transform 1s ease, font-size 1s ease, color 1s ease, text-shadow 1s ease;
        font-size: 50px;
        margin-bottom: 10px;
        color: #10707f;
    }

    .my-anim:hover {
        color: #1e7e34;
    }

    .my-anim-selected {
        transform: translateY(50px) rotateZ(360deg);
        font-size: 70px;
        color: #007bff;
        text-shadow: 2px 2px 5px black;
    }
</style>
