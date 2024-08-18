import axios from "axios";
import qs from 'qs';

export const baseURL = 'api/';
const api = axios.create({
    baseURL,
    paramsSerializer: (params) => qs.stringify(params, {arrayFormat: 'comma'}),
})

api.defaults.headers.post['Content-Type'] = 'application/json';

export const setAccessToken = (token) => {
    (token)
        ? api.defaults.headers.common.Authorization = `Token ${token}`
        : delete api.defaults.headers.common.Authorization;
}

export default api;