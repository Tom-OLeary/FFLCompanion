import api from "../api";

export const searchPlayers = async (players) => {
    const { data } = await api.post('player-search/', {...players});
    return data;
}


export const getWaivers = async () => {
    const { data } = await api.get('waivers/' )
    return data;
}


export const getPlayerStats = async (roster_id, split_type) => {
    const { data } = await api.get(`player-stats/?roster_id=${roster_id}&split_type=${split_type}`);
    return data;
}
