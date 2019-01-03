<template>
    <div>
        <div class="mb-3">
            <h2 align="center">Конфигурация сети</h2>
        </div>
        <div v-if="networks">
            <div class="row form-group" v-for="network in networks">
                <div class="offset-md-2 col-md-10">{{network.name}}</div>

            </div>
        </div>

        <app-login-modal @logged="loadData"></app-login-modal>

    </div>
</template>

<script>
import { LoginModal } from '@/components/LoginModal';
import axios from 'axios';
export default {
    name: 'Networks',
    components: {
        'app-login-modal': LoginModal
    },
    mounted: function() {
        this.loadData();
    },
    methods: {
        loadData: async function() {
            console.log('Start update');
            const answer = await axios.get('http://127.0.0.1:5000/api/wifi');
            console.log(answer.data);
            this.settings = answer.data
        },

        UpdateConfig: async function() {
            console.log('New configs');
            const answer = await axios.post('http://127.0.0.1:5000/api/config', this.settings);
            console.log(answer)
        },

        ResetConfig: async function() {
            await this.loadData()
        }
    },
    data: () => {
        return {
            networks: []
        }
    }
}
</script>

<style scoped>

</style>
