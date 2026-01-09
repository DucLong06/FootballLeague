<template>
	<div class="standings-page">
		<div class="page-header">
			<h1 class="page-title">🏆 Bảng Xếp Hạng</h1>
			<p class="page-subtitle">Thứ hạng các đội trong giải đấu</p>
		</div>

		<!-- Loading State -->
		<div v-if="standingsStore.loading" class="loading-state">
			<div class="loader"></div>
			<p>Đang tải dữ liệu...</p>
		</div>

		<!-- Error/Empty State -->
		<div v-else-if="!standingsStore.standings.length" class="empty-state">
			<div class="empty-icon">🏆</div>
			<h2>Chưa có bảng xếp hạng</h2>
			<p>
				Chưa có giải đấu League nào đang diễn ra hoặc chưa có dữ liệu
				BXH.
			</p>
			<router-link to="/" class="back-link"
				>← Quay lại trang chủ</router-link
			>
		</div>

		<!-- Content -->
		<template v-else>
			<!-- Season Info -->
			<div v-if="standingsStore.currentSeason" class="season-info">
				<span class="season-badge">{{
					standingsStore.currentSeason.type_display
				}}</span>
				<h2 class="season-name">
					{{ standingsStore.currentSeason.name }}
				</h2>
			</div>

			<!-- Standings Table -->
			<section class="standings-section">
				<StandingsTable
					:standings="standingsStore.standings"
					:show-form="true"
				/>
			</section>

			<!-- Form Legend -->
			<div class="form-legend">
				<span class="legend-item"
					><span class="badge">✅</span> Thắng</span
				>
				<span class="legend-item"
					><span class="badge">⬜</span> Hòa</span
				>
				<span class="legend-item"
					><span class="badge">❌</span> Thua</span
				>
			</div>
		</template>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useStandingsStore } from "../stores/standings";
import StandingsTable from "../components/tables/StandingsTable.vue";
import { playersApi } from "../services/api";

const standingsStore = useStandingsStore();
const players = ref([]);

// Fetch player rankings
const fetchPlayerRankings = async () => {
	try {
		const response = await playersApi.rankings("goals", 20);
		players.value = response.data;
	} catch (err) {
		console.error("Failed to fetch player rankings:", err);
	}
};

// Player stats computed - sắp xếp theo bàn thắng
const playerStats = computed(() => {
	return players.value
		.map((item) => ({
			id: item.player.id,
			name: item.player.name,
			nickname: item.player.nickname,
			goals: item.goals || 0,
			assists: item.assists || 0,
			contribution: (item.goals || 0) + (item.assists || 0),
			yellowCards: item.yellow_cards || 0,
			redCards: item.red_cards || 0,
		}))
		.sort((a, b) => b.goals - a.goals || b.contribution - a.contribution);
});

const getRankClass = (idx) => {
	if (idx === 0) return "gold";
	if (idx === 1) return "silver";
	if (idx === 2) return "bronze";
	return "";
};

const getRankIcon = (idx) => {
	if (idx === 0) return "🥇";
	if (idx === 1) return "🥈";
	if (idx === 2) return "🥉";
	return idx + 1;
};

onMounted(() => {
	standingsStore.fetchCurrentStandings();
	fetchPlayerRankings();
});
</script>

<style scoped>
.standings-page {
	max-width: 1200px;
	margin: 0 auto;
	padding: 2rem 1.5rem;
}

.page-header {
	text-align: center;
	margin-bottom: 2rem;
}

.page-title {
	font-size: 2.5rem;
	font-weight: 800;
	color: #fff;
	margin: 0;
}

.page-subtitle {
	font-size: 1rem;
	color: #9ca3af;
	margin: 0.5rem 0 0;
}

.loading-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	min-height: 50vh;
	gap: 1rem;
	color: #9ca3af;
}

.loader {
	width: 48px;
	height: 48px;
	border: 4px solid rgba(16, 185, 129, 0.2);
	border-top-color: #10b981;
	border-radius: 50%;
	animation: spin 1s linear infinite;
}

@keyframes spin {
	to {
		transform: rotate(360deg);
	}
}

.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	min-height: 50vh;
	text-align: center;
}

.empty-icon {
	font-size: 4rem;
	margin-bottom: 1rem;
}

.empty-state h2 {
	font-size: 1.5rem;
	color: #fff;
	margin: 0 0 0.5rem;
}

.empty-state p {
	color: #9ca3af;
	margin: 0 0 1.5rem;
}

.back-link {
	color: #10b981;
	text-decoration: none;
}

.season-info {
	display: flex;
	align-items: center;
	gap: 1rem;
	margin-bottom: 2rem;
}

.season-badge {
	padding: 0.5rem 1rem;
	background: rgba(16, 185, 129, 0.2);
	color: #10b981;
	border-radius: 8px;
	font-size: 0.875rem;
	font-weight: 600;
}

.season-name {
	font-size: 1.5rem;
	font-weight: 700;
	color: #fff;
	margin: 0;
}

.standings-section {
	background: rgba(255, 255, 255, 0.05);
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 16px;
	padding: 1.5rem;
	margin-bottom: 1.5rem;
}

.form-legend {
	display: flex;
	justify-content: center;
	gap: 2rem;
	padding: 1rem;
	color: #9ca3af;
	font-size: 0.875rem;
}

.legend-item {
	display: flex;
	align-items: center;
	gap: 0.5rem;
}

.players-section {
	margin-top: 2rem;
}

.section-title {
	font-size: 1.25rem;
	font-weight: 700;
	color: #fff;
	margin: 0 0 1rem;
}

.players-table-container {
	background: rgba(255, 255, 255, 0.05);
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 16px;
	padding: 1rem;
	overflow-x: auto;
}

.players-table {
	width: 100%;
	border-collapse: collapse;
}

.players-table th,
.players-table td {
	padding: 0.75rem 0.5rem;
	text-align: left;
	border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.players-table th {
	font-size: 0.75rem;
	font-weight: 600;
	color: #9ca3af;
	text-transform: uppercase;
}

.players-table td {
	color: #d1d5db;
	font-size: 0.875rem;
}

.players-table .rank {
	width: 50px;
	text-align: center;
}

.players-table .player {
	min-width: 150px;
}

.players-table .number {
	width: 60px;
	text-align: center;
}

.rank-badge {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	width: 28px;
	height: 28px;
	border-radius: 50%;
	font-size: 0.875rem;
	background: rgba(255, 255, 255, 0.1);
	color: #9ca3af;
}

.rank-badge.gold {
	background: #eab308;
	color: #000;
}
.rank-badge.silver {
	background: #9ca3af;
	color: #000;
}
.rank-badge.bronze {
	background: #b45309;
	color: #fff;
}

.player-link {
	color: #fff;
	text-decoration: none;
	font-weight: 600;
}

.player-link:hover {
	color: #10b981;
}

.players-table .goals {
	color: #10b981;
	font-weight: 700;
}
.players-table .assists {
	color: #3b82f6;
}
.players-table .contribution {
	color: #8b5cf6;
	font-weight: 600;
}
.players-table .yellow {
	color: #f59e0b;
}
.players-table .red {
	color: #ef4444;
}

.players-table tr.top-3 {
	background: rgba(255, 255, 255, 0.02);
}

.players-table tr:hover {
	background: rgba(255, 255, 255, 0.05);
}
</style>
