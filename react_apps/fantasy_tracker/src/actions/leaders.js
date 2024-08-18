import api from "../api";

export const getLeaders = async () => {
    const { data } = await api.get('leaders/');
    return data;
}