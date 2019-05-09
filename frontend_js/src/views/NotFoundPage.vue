<template>
    <div class="container-fluid">
        <div class="row mt-3">
            <div class="col-xl-12 col-lg-12 col-md-12 col-xs-12  col-12">
                <h3 align="center">
                    Запрашиваемая вами страница не найдена, но вы всегда можете вернуться домой
                </h3>
            </div>
        </div>
        <div class="row mt-1">
            <div class="offset-xl-4 col-xl-4 offset-lg-3 col-lg-6 offset-md-2 col-md-8
                        offset-xs-1 col-xs-10 offset-0 col-12">
                <button class="btn btn-success btn-block" @click="goHome()">Домой</button>
            </div>
        </div>

    </div>
</template>

<script>
export default {
    name: 'NotFoundPage',
    methods: {
        goHome() {
            this.$router.push('/');
        }
    }
}
</script>

<style scoped>

</style>
