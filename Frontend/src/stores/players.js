import { defineStore } from 'pinia'
import { playersApi } from '../services/api'

export const usePlayersStore = defineStore('players', {
    state: () => ({
        players: [],
        currentPlayer: null,
        playerStats: null,
        playerMatches: [],
        rankings: [],
        loading: false,
        error: null,
    }),

    actions: {
        async fetchPlayers() {
            this.loading = true
            this.error = null
            try {
                const response = await playersApi.list()
                this.players = response.data.results || response.data
            } catch (err) {
                this.error = err.message
                console.error('Failed to fetch players:', err)
            } finally {
                this.loading = false
            }
        },

        async fetchPlayer(id) {
            this.loading = true
            this.error = null
            try {
                const response = await playersApi.get(id)
                this.currentPlayer = response.data
            } catch (err) {
                this.error = err.message
                console.error('Failed to fetch player:', err)
            } finally {
                this.loading = false
            }
        },

        async fetchPlayerStats(id, seasonId = null) {
            try {
                const response = await playersApi.stats(id, seasonId)
                this.playerStats = response.data
            } catch (err) {
                console.error('Failed to fetch player stats:', err)
            }
        },

        async fetchPlayerMatches(id) {
            try {
                const response = await playersApi.matches(id)
                this.playerMatches = response.data
            } catch (err) {
                console.error('Failed to fetch player matches:', err)
            }
        },

        async fetchRankings(type = 'goals', limit = 10, seasonId = null) {
            this.loading = true
            try {
                const response = await playersApi.rankings(type, limit, seasonId)
                this.rankings = response.data
            } catch (err) {
                console.error('Failed to fetch rankings:', err)
            } finally {
                this.loading = false
            }
        },
    },
})
