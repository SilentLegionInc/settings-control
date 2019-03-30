<template>
    <div class="divider ml-2 mr-2">
        <span class="lines"><hr></span>
        <span class="inner-text ml-2 mr-2"><h5>{{text}}</h5></span>
        <span class="lines"><hr></span>
    </div>
</template>

<script>
export default {
    name: 'Divider',
    props: ['text']

}
</script>

<style scoped>
    .divider {
        display: flex;
        flex-direction: row;
        flex-wrap: nowrap;
        justify-content: center;
        align-items: center;
    }
    .inner-text {
        flex-basis: auto;
    }
    .lines {
        flex-grow: 2
    }
</style>
