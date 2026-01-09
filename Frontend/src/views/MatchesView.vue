<template>
	<div class="matches-page">
		<div class="page-header">
			<h1 class="page-title">📅 Lịch Sử Trận Đấu</h1>
			<p class="page-subtitle">Tất cả các trận đấu đã diễn ra</p>
		</div>

		<!-- Filters -->
		<div class="filters">
			<select v-model="selectedSeason" class="filter-select">
				<option value="">Tất cả mùa giải</option>
				<option
					v-for="season in matchesStore.seasons"
					:key="season.id"
					:value="season.id"
				>
					{{ season.type === "WEEKLY" ? "🗓️" : "🏆" }}
					{{ season.name }}
				</option>
			</select>
		</div>

		<!-- Loading State -->
		<div v-if="matchesStore.loading" class="loading-state">
			<div class="loader"></div>
			<p>Đang tải dữ liệu...</p>
		</div>

		<!-- Matches List -->
		<div v-else class="matches-list">
			<MatchCard
				v-for="match in matchesStore.matches"
				:key="match.id"
				:match="match"
			/>
		</div>

		<!-- Empty State -->
		<div
			v-if="!matchesStore.loading && !matchesStore.matches.length"
			class="empty-state"
		>
			<div class="empty-icon">📅</div>
			<h2>Chưa có trận đấu nào</h2>
			<p>
				Các trận đấu sẽ được hiển thị ở đây sau khi được thêm vào hệ
				thống.
			</p>
		</div>
	</div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import { useMatchesStore } from "../stores/matches";
import MatchCard from "../components/cards/MatchCard.vue";

const matchesStore = useMatchesStore();
const selectedSeason = ref("");

watch(selectedSeason, (seasonId) => {
	matchesStore.fetchMatches(seasonId || null);
});

onMounted(() => {
	matchesStore.fetchSeasons();
	matchesStore.fetchMatches();
});
</script>

<style scoped>
.matches-page {
	max-width: 900px;
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

.filters {
	display: flex;
	gap: 1rem;
	margin-bottom: 2rem;
}

.filter-select {
	background: rgba(255, 255, 255, 0.05);
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 12px;
	padding: 0.75rem 1rem;
	color: #fff;
	font-size: 1rem;
	cursor: pointer;
	outline: none;
	min-width: 200px;
}

.filter-select option {
	background: #1f2937;
	color: #fff;
}

.loading-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	min-height: 30vh;
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

.matches-list {
	display: grid;
	gap: 1rem;
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
	margin: 0;
}
</style>
