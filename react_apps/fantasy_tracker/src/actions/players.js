import api from "../api";

export const searchPlayers = async (players) => {
    const { data } = await api.post('player-search/', {...players});
    return data;
}
