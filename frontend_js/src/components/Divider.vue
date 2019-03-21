<template>
    <div class="divider ml-2 mr-2">
        <span style="flex-grow: 2"><hr></span>
        <span style="flex-basis: auto" class="ml-2 mr-2">{{text}}</span>
        <span style="flex-grow: 2"><hr></span>
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
</style>
