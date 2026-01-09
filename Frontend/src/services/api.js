import axios from 'axios'

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
    headers: {
        'Content-Type': 'application/json',
    },
})

// API Services
export const overviewApi = {
    get: () => api.get('/overview/'),
}

export const playersApi = {
    list: (params = {}) => api.get('/players/', { params }),
    get: (id) => api.get(`/players/${id}/`),
    stats: (id, seasonId = null) => api.get(`/players/${id}/stats/`, { params: { season: seasonId } }),
    matches: (id) => api.get(`/players/${id}/matches/`),
    rankings: (type = 'goals', limit = 10, seasonId = null) =>
        api.get('/players/rankings/', { params: { type, limit, season: seasonId } }),
}

export const seasonsApi = {
    list: () => api.get('/seasons/'),
    get: (id) => api.get(`/seasons/${id}/`),
    current: () => api.get('/seasons/current/'),
    matches: (id) => api.get(`/seasons/${id}/matches/`),
    stats: (id) => api.get(`/seasons/${id}/stats/`),
}

export const teamsApi = {
    list: (seasonId = null) => api.get('/teams/', { params: { season: seasonId } }),
    get: (id) => api.get(`/teams/${id}/`),
}

export const matchesApi = {
    list: (params = {}) => api.get('/matches/', { params }),
    get: (id) => api.get(`/matches/${id}/`),
    recent: (limit = 5) => api.get('/matches/recent/', { params: { limit } }),
}

export const standingsApi = {
    list: (seasonId = null) => api.get('/standings/', { params: { season: seasonId } }),
    current: () => api.get('/standings/current/'),
}

export const awardsApi = {
    get: (seasonId = null) => api.get('/awards/', { params: { season: seasonId } }),
}

export default api
