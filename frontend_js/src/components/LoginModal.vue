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
                            <label for="password-input">Password</label>
                            <input type="password" class="form-control" id="password-input" placeholder="Password" required v-model="password">
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

<script>
import { ServerExceptionModel } from '../models/ServerExceptionModel';
import logger from '../logger';
export default

{
    name: 'LoginModal',
    data: function () {
        return {
            password: ''
        }
    },
    mounted: function() {
        if (!this.$store.getters.isAuthenticated) {
            this.showModal();
        }
    },
    methods: {
        showModal: function() {
            this.$modal.show('login-modal', {}, {
                clickToClose: false
            });
        },

        hideModal: function() {
            this.$modal.hide('login-modal');
        },

        onCancel: function() {
            this.hideModal();
        },

        onLogin: async function() {
            try {
                await this.$store.dispatch('authorize', this.password);
                this.$toaster.success('Log in successful');
                this.hideModal();
                this.$emit('logged');
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Internal server error');
                    logger.error(err);
                }
            }
        }
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
