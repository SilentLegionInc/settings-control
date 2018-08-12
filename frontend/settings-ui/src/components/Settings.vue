<template>
    <div>
        {{data}}
    </div>
</template>

<script lang="ts">
    import {Component, Prop, Vue, Inject} from 'vue-property-decorator';
    import axios from 'axios';

    @Component
    export default class Settings extends Vue {
        // @Inject('getCurrentSettings') private getCurrentSettings: any;
        @Prop() private data: any;

        private created() {
            axios.get('http://127.0.0.1:5000/config', {
                headers: {
                    'Access-Control-Allow-Origin': '*',
                }}).then(answer => {
                this.data = answer.data;
                console.log(answer);
            });
            // this.getCurrentSettings.then((d: any) => {
            //     console.log(d.data);
            //     this.data = d.data;
            // });
        }
    }
</script>

<style scoped>

</style>