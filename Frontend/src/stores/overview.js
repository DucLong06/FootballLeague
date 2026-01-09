import { defineStore } from 'pinia'
import { overviewApi, awardsApi } from '../services/api'

export const useOverviewStore = defineStore('overview', {
    state: () => ({
        stats: null,
        topScorers: [],
        topAssists: [],
        topCards: [],
        gloryAwards: [],
        shameAwards: [],
        currentSeason: null,
        loading: false,
        error: null,
    }),

    actions: {
        async fetchOverview() {
            this.loading = true
            this.error = null
            try {
                const response = await overviewApi.get()
                const data = response.data

                this.stats = {
                    totalPlayers: data.total_players,
                    totalMatches: data.total_matches,
                    totalGoals: data.total_goals,
                    totalCards: data.total_cards,
                    yellowCards: data.yellow_cards,
                    redCards: data.red_cards,
                }
                this.topScorers = data.top_scorers
                this.topAssists = data.top_assists
                this.topCards = data.top_cards
                this.gloryAwards = data.glory_awards
                this.shameAwards = data.shame_awards
                this.currentSeason = data.current_season
            } catch (err) {
                this.error = err.message
                console.error('Failed to fetch overview:', err)
            } finally {
                this.loading = false
            }
        },
    },
})
