<template>
	<div class="player-detail-page">
		<!-- Loading State -->
		<div v-if="playersStore.loading" class="loading-state">
			<div class="loader"></div>
			<p>Đang tải...</p>
		</div>

		<!-- Error State -->
		<div v-else-if="!player" class="error-state">
			<p>❌ Không tìm thấy cầu thủ</p>
			<router-link to="/players" class="back-link"
				>← Quay lại</router-link
			>
		</div>

		<!-- Content -->
		<template v-else>
			<!-- Header -->
			<div class="player-header">
				<router-link to="/players" class="back-btn"
					>← Quay lại</router-link
				>

				<div class="player-profile">
					<div class="player-avatar">
						<img
							v-if="player.avatar_url"
							:src="player.avatar_url"
							:alt="player.name"
						/>
						<div v-else class="avatar-placeholder">
							{{ initials }}
						</div>
					</div>
					<div class="player-info">
						<h1 class="player-name">{{ player.name }}</h1>
						<p v-if="player.nickname" class="player-nickname">
							"{{ player.nickname }}"
						</p>
					</div>
				</div>
			</div>

			<!-- Season Filter -->
			<div class="season-filter">
				<label>📊 Thống kê theo:</label>
				<select v-model="selectedSeason" @change="onSeasonChange">
					<option value="">Tất cả</option>
					<option
						v-for="season in seasons"
						:key="season.id"
						:value="season.id"
					>
						{{ season.type === "WEEKLY" ? "🗓️" : "🏆" }}
						{{ season.name }}
					</option>
				</select>
			</div>

			<!-- Stats Grid -->
			<section class="stats-section">
				<h2 class="section-title">
					📊 Thống Kê {{ selectedSeasonName }}
				</h2>
				<div class="stats-grid">
					<div class="stat-item">
						<span class="stat-icon">🎮</span>
						<span class="stat-value">{{
							stats?.matches_played || 0
						}}</span>
						<span class="stat-label">Trận</span>
					</div>
					<div class="stat-item success">
						<span class="stat-icon">⚽</span>
						<span class="stat-value">{{ stats?.goals || 0 }}</span>
						<span class="stat-label">Bàn thắng</span>
					</div>
					<div class="stat-item">
						<span class="stat-icon">🎯</span>
						<span class="stat-value">{{
							stats?.assists || 0
						}}</span>
						<span class="stat-label">Kiến tạo</span>
					</div>
					<div class="stat-item">
						<span class="stat-icon">📈</span>
						<span class="stat-value">{{
							stats?.goal_ratio || 0
						}}</span>
						<span class="stat-label">Bàn/Trận</span>
					</div>
					<div class="stat-item danger" v-if="stats?.own_goals > 0">
						<span class="stat-icon">🥅</span>
						<span class="stat-value">{{
							stats?.own_goals || 0
						}}</span>
						<span class="stat-label">Phản lưới</span>
					</div>
					<div class="stat-item warning">
						<span class="stat-icon">🟨</span>
						<span class="stat-value">{{
							stats?.yellow_cards || 0
						}}</span>
						<span class="stat-label">Thẻ vàng</span>
					</div>
					<div class="stat-item danger">
						<span class="stat-icon">🟥</span>
						<span class="stat-value">{{
							stats?.red_cards || 0
						}}</span>
						<span class="stat-label">Thẻ đỏ</span>
					</div>
					<div class="stat-item">
						<span class="stat-icon">💪</span>
						<span class="stat-value">{{
							stats?.contribution || 0
						}}</span>
						<span class="stat-label">Đóng góp</span>
					</div>
				</div>
			</section>

			<!-- Match History -->
			<section
				v-if="playersStore.playerMatches.length"
				class="matches-section"
			>
				<h2 class="section-title">📅 Lịch Sử Thi Đấu</h2>
				<div class="matches-list">
					<MatchCard
						v-for="match in playersStore.playerMatches"
						:key="match.id"
						:match="match"
					/>
				</div>
			</section>
		</template>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import { usePlayersStore } from "../stores/players";
import { useMatchesStore } from "../stores/matches";
import MatchCard from "../components/cards/MatchCard.vue";

const route = useRoute();
const playersStore = usePlayersStore();
const matchesStore = useMatchesStore();

const selectedSeason = ref("");
const seasons = computed(() => matchesStore.seasons);

const player = computed(() => playersStore.currentPlayer);
const stats = computed(() => playersStore.playerStats);

const selectedSeasonName = computed(() => {
	if (!selectedSeason.value) return "(Tất cả)";
	const season = seasons.value.find((s) => s.id === selectedSeason.value);
	return season ? `- ${season.name}` : "";
});

const initials = computed(() => {
	if (!player.value) return "";
	const names = player.value.name.split(" ");
	return names.length >= 2
		? names[0][0] + names[names.length - 1][0]
		: names[0].slice(0, 2).toUpperCase();
});

const onSeasonChange = () => {
	const id = route.params.id;
	playersStore.fetchPlayerStats(id, selectedSeason.value || null);
};

const fetchData = async () => {
	const id = route.params.id;
	await matchesStore.fetchSeasons();
	await playersStore.fetchPlayer(id);
	await playersStore.fetchPlayerStats(id, null);
	await playersStore.fetchPlayerMatches(id);
};

watch(() => route.params.id, fetchData);
onMounted(fetchData);
</script>

<style scoped>
.player-detail-page {
	max-width: 900px;
	margin: 0 auto;
	padding: 1.5rem 1rem;
}

.loading-state,
.error-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	min-height: 50vh;
	gap: 1rem;
	color: #9ca3af;
}

.loader {
	width: 40px;
	height: 40px;
	border: 3px solid rgba(30, 64, 175, 0.2);
	border-top-color: #1e40af;
	border-radius: 50%;
	animation: spin 1s linear infinite;
}

@keyframes spin {
	to {
		transform: rotate(360deg);
	}
}

.back-link {
	color: #10b981;
	text-decoration: none;
}

/* Header */
.player-header {
	margin-bottom: 1.5rem;
}

.back-btn {
	display: inline-block;
	color: #9ca3af;
	text-decoration: none;
	margin-bottom: 1rem;
	font-size: 0.875rem;
}

.back-btn:hover {
	color: #10b981;
}

.player-profile {
	display: flex;
	gap: 1.5rem;
	align-items: center;
}

.player-avatar {
	width: 80px;
	height: 80px;
	border-radius: 50%;
	overflow: hidden;
	flex-shrink: 0;
	border: 3px solid rgba(16, 185, 129, 0.3);
}

.player-avatar img {
	width: 100%;
	height: 100%;
	object-fit: cover;
}

.avatar-placeholder {
	width: 100%;
	height: 100%;
	background: linear-gradient(135deg, #10b981, #059669);
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 1.5rem;
	font-weight: 700;
	color: #fff;
}

.player-name {
	font-size: 1.75rem;
	font-weight: 800;
	color: #fff;
	margin: 0;
}

.player-nickname {
	font-size: 1rem;
	color: #10b981;
	font-style: italic;
	margin: 0.25rem 0 0;
}

/* Season Filter */
.season-filter {
	display: flex;
	align-items: center;
	gap: 0.75rem;
	margin-bottom: 1.5rem;
	padding: 1rem;
	background: rgba(255, 255, 255, 0.05);
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 12px;
}

.season-filter label {
	color: #9ca3af;
	font-size: 0.875rem;
}

.season-filter select {
	flex: 1;
	max-width: 300px;
	padding: 0.5rem 1rem;
	background: rgba(255, 255, 255, 0.05);
	border: 1px solid rgba(255, 255, 255, 0.2);
	border-radius: 8px;
	color: #fff;
	font-size: 0.875rem;
}

.season-filter select option {
	background: #1f2937;
}

/* Stats */
.stats-section {
	margin-bottom: 2rem;
}

.section-title {
	font-size: 1rem;
	font-weight: 700;
	color: #fff;
	margin: 0 0 1rem;
}

.stats-grid {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(90px, 1fr));
	gap: 0.75rem;
}

.stat-item {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 0.875rem 0.5rem;
	background: rgba(255, 255, 255, 0.05);
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 12px;
	text-align: center;
}

.stat-item.success {
	border-color: rgba(16, 185, 129, 0.3);
}
.stat-item.warning {
	border-color: rgba(245, 158, 11, 0.3);
}
.stat-item.danger {
	border-color: rgba(239, 68, 68, 0.3);
}

.stat-icon {
	font-size: 1.125rem;
	margin-bottom: 0.25rem;
}

.stat-value {
	font-size: 1.375rem;
	font-weight: 700;
	color: #10b981;
}

.stat-item.success .stat-value {
	color: #10b981;
}
.stat-item.warning .stat-value {
	color: #f59e0b;
}
.stat-item.danger .stat-value {
	color: #ef4444;
}

.stat-label {
	font-size: 0.6875rem;
	color: #9ca3af;
	margin-top: 0.125rem;
}

/* Matches */
.matches-section {
	margin-bottom: 2rem;
}

.matches-list {
	display: grid;
	gap: 0.75rem;
}

@media (max-width: 640px) {
	.player-profile {
		flex-direction: column;
		text-align: center;
	}

	.player-name {
		font-size: 1.5rem;
	}
	.stats-grid {
		grid-template-columns: repeat(4, 1fr);
	}
	.season-filter {
		flex-direction: column;
		align-items: stretch;
	}
	.season-filter select {
		max-width: none;
	}
}
</style>
