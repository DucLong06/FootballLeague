import { defineStore } from 'pinia'
import { matchesApi, seasonsApi } from '../services/api'

export const useMatchesStore = defineStore('matches', {
    state: () => ({
        matches: [],
        recentMatches: [],
        currentMatch: null,
        seasons: [],
        loading: false,
        error: null,
    }),

    actions: {
        async fetchMatches(seasonId = null) {
            this.loading = true
            this.error = null
            try {
                const response = await matchesApi.list({ season: seasonId })
                this.matches = response.data.results || response.data
            } catch (err) {
                this.error = err.message
                console.error('Failed to fetch matches:', err)
            } finally {
                this.loading = false
            }
        },

        async fetchRecentMatches(limit = 5) {
            try {
                const response = await matchesApi.recent(limit)
                this.recentMatches = response.data
            } catch (err) {
                console.error('Failed to fetch recent matches:', err)
            }
        },

        async fetchMatch(id) {
            this.loading = true
            try {
                const response = await matchesApi.get(id)
                this.currentMatch = response.data
            } catch (err) {
                console.error('Failed to fetch match:', err)
            } finally {
                this.loading = false
            }
        },

        async fetchSeasons() {
            try {
                const response = await seasonsApi.list()
                this.seasons = response.data.results || response.data
            } catch (err) {
                console.error('Failed to fetch seasons:', err)
            }
        },
    },
})
