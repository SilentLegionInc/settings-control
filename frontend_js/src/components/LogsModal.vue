<template>
    <b-modal ref="logsModal" size="lg" id="logs-modal" title="Детальная информация" scrollable centered ok-only>
        <div class="container-fluid">
            <div class="row mb-2">
                <div class="col-4 col-sm-3 col-md-3 col-lg-2 col-xl-2">
                    <b>Заголовок:</b>
                </div>
                <div class="col-8 col-sm-9 col-md-9 col-lg-10 col-xl-10" align="left" v-if="logTitle">
                    {{this.logTitle}}
                </div>
            </div>
            <div class="row mb-2">
                <div class="col-4 col-sm-3 col-md-3 col-lg-2 col-xl-2">
                    <b>Уровень:</b>
                </div>
                <div class="col-8 col-sm-9 col-md-9 col-lg-10 col-xl-10" align="left" v-if="logType">
                    {{this.logType | logLevelToString}}
                </div>
            </div>
            <div class="row mb-2">
                <div class="col-4 col-sm-3 col-md-3 col-lg-2 col-xl-2">
                    <b>Время:</b>
                </div>
                <div class="col-8 col-sm-9 col-md-9 col-lg-10 col-xl-10" align="left" v-if="logTime">
                    {{this.logTime | moment("DD.MM.YYYY HH:mm:ss.SSS")}}
                </div>
            </div>
            <div class="row">
                <div class="col-4 col-sm-3 col-md-3 col-lg-2 col-xl-2">
                    <b>Описание:</b>
                </div>
                <div class="col-8 col-sm-9 col-md-9 col-lg-10 col-xl-10" align="left" v-if="logMessage">
                    {{this.logMessage}}
                </div>
            </div>
        </div>

        <template slot="modal-footer">
            <div class="container-fluid">
                <div class="row">
                    <div class="offset-0 offset-sm-6 offset-md-8 offset-lg-9 offset-xl-10 col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2">
                        <button type="button" class="btn btn-primary btn-block" @click="hideModal()">Ок</button>
                    </div>
                </div>
            </div>
        </template>
    </b-modal>
</template>

<script>
export default {
    name: 'LogsModal',
    data() {
        return {
            logTime: null,
            logType: null,
            logTitle: null,
            logMessage: null
        }
    },
    methods: {
        showModal(logModel) {
            this.logTime = logModel.time;
            this.logType = logModel.type;
            this.logTitle = logModel.title;
            this.logMessage = logModel.message;

            this.$refs.logsModal.show();
        },

        hideModal() {
            this.$refs.logsModal.hide();
        }
    }
}
</script>

<style scoped lang="scss">
</style>
