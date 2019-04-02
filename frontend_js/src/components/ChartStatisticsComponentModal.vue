<template>
    <b-modal ref="chartModal"
             size="md"
             title="Изменение интервала"
             centered
    >
        <div class="container-fluid">
            <div class="row mb-2">
                <div class="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12">
                    <b>Внимание!</b> Большой интервал может замедлить работу приложения. Рекомендуемый размер - 3 минуты.
                </div>
            </div>
            <div class="row">
                <div class="col-8 col-sm-7 col-md-7 col-lg-6 col-xl-5">
                    <b>Интервал в минутах:</b>
                </div>
                <div class="col-4 col-sm-5 col-md-5 col-lg-6 col-xl-7" align="left">
                    <input v-model="content" @input="handleInput" type="number" class="form-control">
                </div>
            </div>
        </div>

        <template slot="modal-footer">
            <div class="container-fluid">
                <div class="row">
                    <div class="offset-0 offset-sm-0 offset-md-2 offset-lg-4 offset-xl-4 col-12 col-sm-6 col-md-5 col-lg-4 col-xl-4 mb-1">
                        <button type="button" class="btn btn-secondary btn-block" @click="onCancel()">Отмена</button>
                    </div>
                    <div class="col-12 col-sm-6 col-md-5 col-lg-4 col-xl-4">
                        <button type="button" class="btn btn-success btn-block" @click="onOk()">Применить</button>
                    </div>
                </div>
            </div>
        </template>
    </b-modal>
</template>

<script>
export default {
    name: 'ChartStatisticsComponentModal',
    props: {
        value: {
            required: true
        }
    },
    data() {
        return {
            content: this.value
        }
    },
    methods: {
        handleInput(e) {
            this.$emit('input', this.content)
        },
        onOk() {
            this.hideModal();
            this.$emit('ok');
        },
        onCancel() {
            this.hideModal();
            this.$emit('cancel');
        },
        showModal() {
            this.$refs.chartModal.show();
        },
        hideModal() {
            this.$refs.chartModal.hide();
        }
    }
};
</script>

<style scoped>
</style>
