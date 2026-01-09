import { defineStore } from 'pinia'
import { standingsApi, teamsApi } from '../services/api'

export const useStandingsStore = defineStore('standings', {
    state: () => ({
        standings: [],
        teams: [],
        currentSeason: null,
        loading: false,
        error: null,
    }),

    actions: {
        async fetchStandings(seasonId = null) {
            this.loading = true
            this.error = null
            try {
                const response = await standingsApi.list(seasonId)
                this.standings = response.data.results || response.data
            } catch (err) {
                this.error = err.message
                console.error('Failed to fetch standings:', err)
            } finally {
                this.loading = false
            }
        },

        async fetchCurrentStandings() {
            this.loading = true
            this.error = null
            try {
                const response = await standingsApi.current()
                this.standings = response.data.standings
                this.currentSeason = response.data.season
            } catch (err) {
                this.error = err.message
                console.error('Failed to fetch current standings:', err)
            } finally {
                this.loading = false
            }
        },

        async fetchTeams(seasonId = null) {
            try {
                const response = await teamsApi.list(seasonId)
                this.teams = response.data.results || response.data
            } catch (err) {
                console.error('Failed to fetch teams:', err)
            }
        },
    },
})
