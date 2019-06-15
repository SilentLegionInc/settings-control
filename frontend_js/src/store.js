import Vue from 'vue';
import Vuex from 'vuex';
// import Config from './config';
import { RequestService } from './services/RequestService';
import Logger from './logger';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        authToken: null,
        url: null,
        requestService: new RequestService(null),
        robotName: null,
        robotLabel: 'UNK'
    },
    getters: {
        isAuthenticated: state => {
            return !!state.authToken;
        },
        isServerConnected: state => {
            return !!state.robotName;
        }
    },
    mutations: {
        setAuthToken(ctxt, newToken) {
            Vue.prototype.$cookies.set('toolBeltAuthToken', newToken, '10MIN');
            this.state.authToken = newToken;
            this.state.requestService._setAuthHeader(newToken)
        },
        deleteAuthToken(ctxt) {
            Vue.prototype.$cookies.remove('toolBeltAuthToken');
            this.state.authToken = null;
            this.state.requestService._deleteAuthHeader();
        },
        changeHostAddress(ctxt, newUrl) {
            this.state.url = newUrl;
            this.state.requestService._changeHostUrl(this.state.url)
        },
        setRobotName(ctxt, robotName) {
            this.state.robotName = robotName;
        },
        setRobotLabel(ctxt, robotLabel) {
            this.state.robotLabel = robotLabel;
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
        async changePassword(ctxt, passwordsPayload) {
            const token = await this.state.requestService._changePassword(passwordsPayload.oldPassword, passwordsPayload.newPassword);
            if (token) {
                this.commit('setAuthToken', token);
            } else {
                // Exception fly away
            }
        },
        async initUrl(ctxt) {
            let connected = false;
            if (!this.state.url) {
                const urlFromCookies = Vue.prototype.$cookies.get('toolbeltServerUrl');
                try {
                    if (urlFromCookies && urlFromCookies !== 'undefined') {
                        const tempUrl = urlFromCookies;
                        const res = await this.state.requestService.getServerInfo(tempUrl, false);
                        if (res.ok) {
                            connected = true;
                            this.commit('changeHostAddress', tempUrl);
                            this.commit('setRobotName', res.robotType);
                            this.commit('setRobotLabel', res.robotName);
                        }
                    }
                    if (!connected) {
                        // TODO catch
                        const tempUrl = '127.0.0.1:5000';
                        const res = await this.state.requestService.getServerInfo(tempUrl, false)
                        if (res.ok) {
                            connected = true;
                            this.commit('changeHostAddress', tempUrl);
                            this.commit('setRobotName', res.robotType)
                            this.commit('setRobotLabel', res.robotName)
                        }
                    }
                    if (!connected) {
                        Logger.info('Not connected');
                    }
                } catch {
                    // do nothing
                }
                return connected;
            }
        }
    }
})
