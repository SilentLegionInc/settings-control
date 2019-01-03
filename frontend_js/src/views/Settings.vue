<template>
  <div>
    <div class="mb-3">
      <h2 align="center">Конфигурация ядра</h2>
    </div>
    <div v-if="settings">
      <div class="row form-group" v-for="network in networks">
          {{network}}
      </div>
    </div>

    <app-login-modal @logged="loadData"></app-login-modal>

  </div>
</template>

<script>
import axios from 'axios'
import LoginModal from '@/components/LoginModal';
export default {
    name: 'Settings',
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
    components: {
        'app-login-modal': LoginModal
    },
    data: () => {
        return {
            networks: []
        }
    }
}
</script>

<style scoped lang="scss">
</style>
