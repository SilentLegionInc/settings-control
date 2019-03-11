<template>
    <div class="flexbox">
        <div class="container-fluid">
            <div class="row">
                <div class="offset-0 offset-sm-2 offset-md-3 offset-lg-4 offset-xl-4"></div>
                <div class="col-12 col-sm-8 col-md-6 col-lg-4 col-xl-4">
                    <b-card>
                        <h2>Login</h2>
                        <form>
                            <div class="form-group">
                                <label for="url">URL</label>
                                <input type="text" class="form-control" v-model="url" name="url" autocomplete="url"/>
                            </div>
                            <div class="form-group">
                                <label for="password">Password</label>
                                <input type="password" class="form-control" v-model="password" name="password" autocomplete="password"/>
                            </div>
                            <div align="right">
                                <button class="btn btn-secondary mr-2">Проверить адрес</button>
                                <button class="btn btn-primary">Войти</button>
                            </div>
                        </form>
                    </b-card>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data () {
        return {
            url: null,
            password: null
        }
    }
};
</script>

<style scoped lang="scss">
    .flexbox {
        display: flex;
        justify-content: center;
        flex-flow: column;
    }
</style>
