<template>
    <div>
        <label class="offset-md-2 col-md-3 col-form-label" for="oldPassword">Текущий пароль</label>
        <div class="col-md-5">
            <input class="form-control" type="password" id="oldPassword" v-model="oldPassword" placeholder=""/>
        </div>
        <label class="offset-md-2 col-md-3 col-form-label" for="newPassword">Новый пароль</label>
        <div class="col-md-5">
            <input class="form-control" type="password" id="newPassword" v-model="newPassword" placeholder=""/>
        </div>
    </div>
</template>

<script>
// TODO think where this component must be.
export default {
    name: 'ChangePassword',
    data: () => {
        return {
            oldPassword: '',
            newPassword: ''
        }
    },
    methods: {
        async updatePassword() {
            const res = await this.$store.state.requestService.changePassword(this.oldPassword, this.newPassword);
            // TODO
            if (res) {
                // ok
            } else {
                // error
            }
        }
    }

}
</script>

<style scoped>

</style>
