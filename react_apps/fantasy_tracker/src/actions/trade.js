import api from "../api";

export const getTrades = async () => {
    const { data } = await api.get('trades/');
    return data;
}
