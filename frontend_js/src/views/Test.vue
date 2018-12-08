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

<script>
    export default {
        name: 'Test',
        data: function() {
            return {
                activeElement: -1
            };
        },
        methods: {
            clicked: function(index) {
                index = Number(index);
                if (this.activeElement === index) {
                    this.activeElement = -1;
                } else {
                    this.activeElement = index;
                }
            }
        }
    }
</script>

<style scoped lang="scss">
</style>
