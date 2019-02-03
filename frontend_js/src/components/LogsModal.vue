<template>
    <modal name="login-modal" :clickToClose="false" :height="'auto'" :adaptive="true">
        <div style="height: 100%; margin: 0 10px 0 10px">
            <div class="header" v-if="logTitle">
                {{this.logTitle}}
            </div>

            <div class="flex-container">
                <div class="content">
                    <div class="row">
                        <div class="col-md-2">
                            <b>Уровень:</b>
                        </div>
                        <div class="col-md-9" align="left" v-if="logType">
                            {{this.logType | logLevelToString}}
                        </div>
                    </div>
                    <div class="row margin-top-sm">
                        <div class="col-md-2">
                            <b>Время:</b>
                        </div>
                        <div class="col-md-9" align="left" v-if="logTime">
                            {{this.logTime | moment("DD.MM.YYYY HH:mm:ss.SSS")}}
                        </div>
                    </div>
                    <div class="row margin-top-sm margin-bottom-sm">
                        <div class="col-md-2">
                            <b>Описание:</b>
                        </div>
                        <div class="col-md-9 scrollable-message-text" align="left" v-if="logMessage">
                            {{this.logMessage}}
                        </div>
                    </div>
                </div>

                <div class="footer" align="right">
                    <button class="btn btn-danger" @click="hideModal">Close</button>
                </div>
            </div>
        </div>
    </modal>
</template>

<script>
export default {
    name: 'LoginModal',
    data: function() {
        return {
            logTime: null,
            logType: null,
            logTitle: null,
            logMessage: null
        }
    },
    methods: {
        showModal: function(logModel) {
            this.logTime = logModel.time;
            this.logType = logModel.type;
            this.logTitle = logModel.title;
            this.logMessage = logModel.message;

            this.$modal.show('login-modal', {}, {
                clickToClose: false
            });
        },

        hideModal: function() {
            this.$modal.hide('login-modal');
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

    .scrollable-message-text {
        height: auto;
        max-height: 300px;
        overflow-y: auto;
    }
</style>
