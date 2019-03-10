<template>
    <div>
        <h3>
            Test animation
        </h3>
        <a href="#" class="clickable" @click="isOpen = !isOpen">
            Статистика

            <transition name="flip" mode="out-in">
                <i v-if="!isOpen" key="1" class="fa fa-chevron-down" aria-hidden="true"></i>
                <i v-else key="2" class="fa fa-chevron-up" aria-hidden="true"></i>
            </transition>
        </a>
    </div>
</template>

<script>
export default {
    name: 'TestAnimation',
    data: function () {
        return {
            isOpen: false
        }
    }
}
</script>

<style scoped lang="scss">
    .flip-enter, .flip-leave-to {
        transform: rotateX(90deg);
    }

    .flip-leave, .flip-enter-to {
        transform: rotateX(0deg);
    }

    .flip-enter-active, .flip-leave-active {
        transition: transform 0.2s;
    }
</style>
