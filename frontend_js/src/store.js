import Vue from 'vue'
import Vuex from 'vuex'
import config from './config'
import { RequestService } from './services/RequestService'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        authToken: null,
        requestService: new RequestService(config.get('backendHost'), config.get('backendPort'))
    },
    getters: {
        isAuthenticated: state => {
            return !!state.authToken;
        }
    },
    mutations: {
        setAuthToken(context, newToken) {
            this.state.authToken = newToken;
            this.state.requestService._setAuthHeader(newToken)
        },
        deleteAuthToken(context) {
            this.state.authToken = null;
            this.state.requestService._deleteAuthHeader();
        }
    },
    actions: {
        // Important! use need use only this function from vuex.
        async authorize(context, password) {
            const token = await this.state.requestService._authorize(password);
            if (token) {
                this.commit('setAuthToken', token)
            } else {
                // Exception fly away
            }
        },
        async deauthorize(context) {
            const result = await this.state.requestService._deauthorize();
            if (result) {
                this.commit('deleteAuthToken');
            } else {
                // Exception fly away
            }
        }
    }
})
