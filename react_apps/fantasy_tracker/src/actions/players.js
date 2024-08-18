import api from "../api";

export const searchPlayers = async (players) => {
    return await api.post('player-search/', {...players});
}
