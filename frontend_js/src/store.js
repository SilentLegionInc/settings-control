import Vue from 'vue'
import Vuex from 'vuex'
import Config from './config'
import { RequestService } from './services/RequestService'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        authToken: null,
        url: Config.backendUrl,
        requestService: new RequestService(Config.backendUrl),
        robotName: 'AMTS'
    },
    getters: {
        isAuthenticated: state => {
            return !!state.authToken;
        }
    },
    mutations: {
        setAuthToken(ctxt, newToken) {
            Vue.prototype.$cookies.set('toolBeltAuthToken', newToken, '10MIN');
            this.state.authToken = newToken;
            this.state.requestService._setAuthHeader(newToken)
        },
        deleteAuthToken(ctxt) {
            this.state.authToken = null;
            this.state.requestService._deleteAuthHeader();
        },
        changeHostAddress(ctxt, newUrl) {
            this.state.url = newUrl;
            this.state.requestService._changeHostUrl(this.state.url)
        }
    },
    actions: {
        // Important! use need use only this function from vuex.
        async authorize(ctxt, password) {
            const token = await this.state.requestService._authorize(password);
            if (token) {
                this.commit('setAuthToken', token);
            } else {
                // Exception fly away
            }
        },
        async deauthorize(ctxt) {
            const result = await this.state.requestService._deauthorize();
            if (result) {
                this.commit('deleteAuthToken');
            } else {
                // Exception fly away
            }
        },
        async changePassword(ctxt, oldPassword, newPassword) {
            const token = await this.state.requestService._changePassword(oldPassword, newPassword);
            if (token) {
                this.commit('setAuthToken', token);
            } else {
                // Exception fly away
            }
        }
    }
})
