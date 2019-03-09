<template>
    <div>
        <h3>
            Test file upload
        </h3>

        <div class="container">
            <div class="large-12 medium-12 small-12 cell">
                <label>File
                    <input type="file" @change="handleFileUpload($event)"/>
                </label>
                <button v-on:click="submitFile()">Submit</button>
            </div>
        </div>
    </div>
</template>

<script>
import { ServerExceptionModel } from '../models/ServerExceptionModel';
import Logger from '../logger';
export default {
    name: 'TestFileUpload',
    data: function() {
        return {
            file: ''
        }
    },

    methods: {
        submitFile: async function() {
            const formData = new FormData();
            formData.append('file', this.file);
            try {
                // TODO add module name and build on download variables to request.
                await this.$store.state.requestService.uploadModuleArchive(formData);
                this.$toaster.success('Загружено, сучечка');
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Internal server error');
                    Logger.error(err);
                }
            }
        },

        handleFileUpload(event) {
            this.file = event.target.files[0];
        }
    }
}
</script>

<style scoped>

</style>
