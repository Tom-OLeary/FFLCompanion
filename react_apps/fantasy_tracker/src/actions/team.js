import api from "../api";

export const getTeamStats = async () => {
    const { data } = await api.get('stats/');
    return data;
}
