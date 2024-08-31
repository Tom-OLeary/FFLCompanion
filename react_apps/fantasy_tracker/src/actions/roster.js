import api from "../api";

export const createRoster = async (player_ids) => {
    // create new roster where none exists
    const { data } = await api.post('rosters/', {
        player_ids: player_ids,
    });
    return data;
}

export const getRoster = async () => {
    // get user's latest roster
    const { data } = await api.get('rosters/user/?latest=true');
    return data;
}


export const getLeagueRosters = async () => {
    // get all latest rosters for entire league
    const {data} = await api.get('rosters/');
    return data;
}


export const deleteRoster = async (roster_id) => {
    const { data } = await api.delete(`rosters/${roster_id}/`);
    return data;
}


export const updateRoster = async (roster_id, player_updates) => {
    const { data } = await api.post(`rosters/${roster_id}/`, {...player_updates});
    return data;
}
