<template>
    <div>
        <h3>
            Test file upload
        </h3>

        <div class="container">
            <div class="large-12 medium-12 small-12 cell">
                <label>File
                    <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
                </label>
                <button v-on:click="submitFile()">Submit</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'TestFileUpload',
    data: function() {
        return {
            file: ''
        }
    },

    methods: {
        submitFile() {
            let formData = new FormData();
            formData.append('file', this.file);
            this.$store.state.requestService.uploadFile(formData);
        },

        handleFileUpload() {
            this.file = this.$refs.file.files[0];
        }
    }
}
</script>

<style scoped>

</style>
