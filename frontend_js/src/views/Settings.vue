<template>
  <div>
    <div class="mb-3">
      <h2 align="center">Конфигурация ядра</h2>
    </div>
    <div v-if="settings">
      <div class="row form-group" v-for="(_, settingKey) in settings">
        <label class="offset-md-2 col-md-3 col-form-label" :for="settingKey">{{settingKey}}</label>
        <div class="col-md-5">
          <input class="form-control" type="text" :id="settingKey" v-model="settings[settingKey]" :placeholder="settingKey"/>
        </div>
      </div>
      <div class="row form-group">
        <div class="col-md-6 offset-md-4" align="right">
          <button class="btn btn-danger" @click="ResetConfig()">
            Reset
          </button>
          <button class="ml-3 btn btn-success" @click="UpdateConfig()">
            Update
          </button>
        </div>
      </div>
    </div>

    <app-login-modal @logged="loadData"></app-login-modal>

  </div>
</template>

<script>
import LoginModal from '@/components/LoginModal';
import { ServerExceptionModel } from '../models/ServerExceptionModel';
import logger from '../logger';

export default {
    name: 'Settings',
    mounted: function() {
        this.loadData();
    },
    methods: {
        // TODO Add machine type to response. Create basic DTO?
        loadData: async function() {
            try {
                this.settings = await this.$store.requestService.getCoreConfig();
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Internal server error');
                    logger.error(err);
                }
                this.settings = {};
            }
        },

        UpdateConfig: async function() {
            try {
                const result = await this.$store.requestService.setCoreConfig(this.settings);
                if (result) {
                    this.$toaster.success('Config successfully updated')
                } else {
                    this.$toaster.warn('Deprecated. Check backend code');
                }
            } catch (err) {
                if (err instanceof ServerExceptionModel) {
                    this.$toaster.error(err.message);
                } else {
                    this.$toaster.error('Internal server error');
                    logger.error(err);
                }
            }
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
            settings: {}
        }
    }
}
</script>

<style scoped lang="scss">
</style>
