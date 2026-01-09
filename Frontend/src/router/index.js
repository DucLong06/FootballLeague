import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'Overview',
        component: () => import('../views/OverviewView.vue'),
        meta: { title: 'Tổng quan' }
    },
    {
        path: '/standings',
        name: 'Standings',
        component: () => import('../views/StandingsView.vue'),
        meta: { title: 'Bảng xếp hạng' }
    },
    {
        path: '/players',
        name: 'Players',
        component: () => import('../views/PlayersView.vue'),
        meta: { title: 'Cầu thủ' }
    },
    {
        path: '/players/:id',
        name: 'PlayerDetail',
        component: () => import('../views/PlayerDetailView.vue'),
        meta: { title: 'Chi tiết cầu thủ' }
    },
    {
        path: '/matches',
        name: 'Matches',
        component: () => import('../views/MatchesView.vue'),
        meta: { title: 'Trận đấu' }
    },
    {
        path: '/seasons/:id',
        name: 'SeasonStats',
        component: () => import('../views/SeasonStatsView.vue'),
        meta: { title: 'Thống kê mùa giải' }
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach((to, from, next) => {
    document.title = `${to.meta.title || 'CSOC Football'} | ⚽ CSOC Football`
    next()
})

export default router

