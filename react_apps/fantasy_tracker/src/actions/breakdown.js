import api from "../api";

export const getLeaders = async () => {
    const { data } = await api.get('breakdown/');
    return data;
}
