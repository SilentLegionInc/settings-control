import {Prop, Provide} from 'vue-property-decorator';
import axios, {AxiosPromise} from 'axios';

export class RequestService {
    private serverPath: string = 'http://127.0.0.1:5000/config';
    @Provide('getCurrentSettings') public GetCurrentSettings(): AxiosPromise {
        return axios.get(this.serverPath + '/config');
    }
}
