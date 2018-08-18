<template>
    <modal name="login-modal" :clickToClose="false">
        <div style="height: 100%; margin: 0 10px 0 10px">
            <div class="header">
                Sign in
            </div>

            <div class="flex-container">
                <div class="content">
                    Content
                </div>

                <div class="footer" align="right">
                    <button class="btn btn-danger" @click="hideModal">Cancel</button>
                    <button class="btn btn-success" @click="hideModal">Sign in</button>
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
</style>