<template>
    <div>
        <h1>
            Test page
        </h1>

        <hr>
        <i class="fa fa-tint my-anim" :class="{ 'my-anim-selected': activeElement === 0 }" @click="clicked(0)"></i><br>
        <i class="fa fa-male my-anim" :class="{ 'my-anim-selected': activeElement === 1 }" @click="clicked(1)"></i><br>
        <i class="fa fa-lock my-anim" :class="{ 'my-anim-selected': activeElement === 2 }" @click="clicked(2)"></i><br>
        <i class="fa fa-user my-anim" :class="{ 'my-anim-selected': activeElement === 3 }" @click="clicked(3)"></i><br>
        <i class="fa fa-plus my-anim" :class="{ 'my-anim-selected': activeElement === 4 }" @click="clicked(4)"></i><br>

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
        transition: transform 1s ease, font-size 1s ease, color 1s ease;
        font-size: 50px;
        margin-bottom: 10px;
        color: #10707f;
    }

    .my-anim-selected {
        transform: translateX(50px) rotateZ(45deg);
        font-size: 70px;
        color: #007bff;
    }
</style>
