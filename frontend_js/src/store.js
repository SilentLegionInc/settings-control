import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import config from './config'
import { RequestService } from './services/RequestService'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        authToken: null,
        requestService: new RequestService(config.get('backendHost', config.get('backendPort')))
    },
    mutations: {

    },
    actions: {
        // Important! use need use only this function from vuex.
        async authorize(password) {
            this.state.requestService._authorize(password);
        }
    }
})
