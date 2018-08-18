<template>
    <modal name="login-modal" :clickToClose="false" :height="'auto'" :adaptive="true">
        <div style="height: 100%; margin: 0 10px 0 10px">
            <div class="header">
                Sign in
            </div>

            <div class="flex-container">
                <div class="content">
                    <div class="row form-group">
                        <div class="col-md-12">
                            <label for="login-input">Username</label>
                            <input type="text" class="form-control" id="login-input" placeholder="Username">
                        </div>
                    </div>

                    <div class="row form-group">
                        <div class="col-md-12">
                            <label for="password-input">Password</label>
                            <input type="text" class="form-control" id="password-input" placeholder="Password">
                        </div>
                    </div>
                </div>

                <div class="footer" align="right">
                    <button class="btn btn-danger" @click="onCancel">Cancel</button>
                    <button class="btn btn-success" @click="onLogin">Sign in</button>
                </div>
            </div>
        </div>
    </modal>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator';

    @Component
    export default class LoginModal extends Vue {

        private mounted() {
            this.showModal();
        }

        private showModal () {
            this.$modal.show('login-modal', {}, {
                clickToClose: false
            });
        }
        private hideModal () {
            this.$modal.hide('login-modal');
        }

        private onCancel() {
            this.hideModal();
        }

        private onLogin() {
            this.hideModal();
            this.$emit('logged');
        }
    }
</script>

<style scoped lang="scss">
    .header {
        height: 20%;
        text-align: center;
        font-size: 40px;
    }

    .content {
        flex: 1 1 auto;
        margin-top: 15px;
    }

    .footer {
        flex: 0 1 auto;
        margin-bottom: 10px;
    }

    .flex-container {
        display: flex;
        flex-direction: column;
        flex-wrap: nowrap;
        height: 80%;
    }

    .btn {
        margin-left: 10px;
    }

    label {
        font-size: 13px;
        font-weight: bold;
        margin-left: 5px;
        margin-bottom: 0;
    }
</style>