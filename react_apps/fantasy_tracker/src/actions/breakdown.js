import api from "../api";

export const getBreakdown = async () => {
    const { data } = await api.get('breakdown/');
    return data;
}

export const getProjections = async () => {
    const { data } = await api.get('projections/');
    return data;
}

export const getTrends = async () => {
    const { data } = await api.get('trends/');
    return data;
}

export const getLeagueURL = async () => {
    const { data } = await api.get('leagues/?get_url=true');
    return data;
}

