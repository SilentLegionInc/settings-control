<template>
    <b-modal ref="networksModal"
             size="lg"
             :title="title"
             centered
    >
        <div class="container-fluid">
            <div class="row mb-2">
                <div class="col-12 col-sm-12 col-md-12 col-lg-12 col-xl-12">
                    <slot>Network test modal</slot>
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
    name: 'NetworksModal',
    props: {
        title: {
            type: String,
            required: true
        }
    },
    methods: {
        onOk() {
            this.hideModal();
            this.$emit('ok');
        },
        showModal() {
            this.$refs.networksModal.show();
        },
        hideModal() {
            this.$refs.networksModal.hide();
        }
    }
};
</script>

<style scoped>

</style>
