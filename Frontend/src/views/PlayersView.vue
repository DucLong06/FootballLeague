<template>
	<div class="players-page">
		<div class="page-header">
			<h1 class="page-title">👥 Danh Sách Cầu Thủ</h1>
			<p class="page-subtitle">Tất cả cầu thủ trong nhóm</p>
		</div>

		<!-- Search and Filter -->
		<div class="filters">
			<div class="search-box">
				<span class="search-icon">🔍</span>
				<input
					v-model="searchQuery"
					type="text"
					placeholder="Tìm kiếm cầu thủ..."
					class="search-input"
				/>
			</div>
			<div class="sort-box">
				<select v-model="sortBy" class="sort-select">
					<option value="name">Tên A-Z</option>
					<option value="goals">Nhiều bàn nhất</option>
					<option value="assists">Nhiều kiến tạo nhất</option>
					<option value="matches">Nhiều trận nhất</option>
				</select>
			</div>
		</div>

		<!-- Loading State -->
		<div v-if="playersStore.loading" class="loading-state">
			<div class="loader"></div>
			<p>Đang tải dữ liệu...</p>
		</div>

		<!-- Players Grid -->
		<div v-else class="players-grid">
			<PlayerCard
				v-for="player in filteredPlayers"
				:key="player.id"
				:player="player"
			/>
		</div>

		<!-- Empty State -->
		<div
			v-if="!playersStore.loading && !filteredPlayers.length"
			class="empty-state"
		>
			<p>Không tìm thấy cầu thủ nào</p>
		</div>

		<!-- Rankings Section -->
		<section class="rankings-section">
			<h2 class="section-title">🏅 Bảng Xếp Hạng Cá Nhân</h2>

			<div class="tabs">
				<button
					v-for="tab in tabs"
					:key="tab.value"
					:class="['tab', { active: activeTab === tab.value }]"
					@click="activeTab = tab.value"
				>
					{{ tab.icon }} {{ tab.label }}
				</button>
			</div>

			<div class="ranking-container">
				<RankingTable
					:rankings="playersStore.rankings"
					:type="activeTab"
					:show-ratio="activeTab === 'goals'"
				/>
			</div>
		</section>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { usePlayersStore } from "../stores/players";
import PlayerCard from "../components/cards/PlayerCard.vue";
import RankingTable from "../components/tables/RankingTable.vue";

const playersStore = usePlayersStore();

const searchQuery = ref("");
const sortBy = ref("name");
const activeTab = ref("goals");

const tabs = [
	{ value: "goals", label: "Ghi bàn", icon: "⚽" },
	{ value: "assists", label: "Kiến tạo", icon: "🎯" },
	{ value: "cards", label: "Thẻ phạt", icon: "🟨" },
];

const filteredPlayers = computed(() => {
	let players = [...playersStore.players];

	// Filter by search
	if (searchQuery.value) {
		const query = searchQuery.value.toLowerCase();
		players = players.filter(
			(p) =>
				p.name.toLowerCase().includes(query) ||
				(p.nickname && p.nickname.toLowerCase().includes(query))
		);
	}

	// Sort
	players.sort((a, b) => {
		if (sortBy.value === "name") return a.name.localeCompare(b.name);
		// For other sorts, would need stats data
		return a.name.localeCompare(b.name);
	});

	return players;
});

watch(activeTab, () => {
	playersStore.fetchRankings(activeTab.value, 10);
});

onMounted(() => {
	playersStore.fetchPlayers();
	playersStore.fetchRankings("goals", 10);
});
</script>

<style scoped>
.players-page {
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

.filters {
	display: flex;
	gap: 1rem;
	margin-bottom: 2rem;
}

.search-box {
	flex: 1;
	display: flex;
	align-items: center;
	background: rgba(255, 255, 255, 0.05);
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 12px;
	padding: 0 1rem;
}

.search-icon {
	font-size: 1rem;
	margin-right: 0.5rem;
}

.search-input {
	flex: 1;
	background: transparent;
	border: none;
	color: #fff;
	padding: 0.75rem 0;
	font-size: 1rem;
	outline: none;
}

.search-input::placeholder {
	color: #6b7280;
}

.sort-select {
	background: rgba(255, 255, 255, 0.05);
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 12px;
	padding: 0.75rem 1rem;
	color: #fff;
	font-size: 1rem;
	cursor: pointer;
	outline: none;
}

.sort-select option {
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

.players-grid {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
	gap: 1rem;
	margin-bottom: 3rem;
}

.empty-state {
	text-align: center;
	padding: 3rem;
	color: #6b7280;
}

.rankings-section {
	margin-top: 3rem;
}

.section-title {
	font-size: 1.5rem;
	font-weight: 700;
	color: #fff;
	margin: 0 0 1.5rem;
}

.tabs {
	display: flex;
	gap: 0.5rem;
	margin-bottom: 1.5rem;
}

.tab {
	padding: 0.75rem 1.5rem;
	background: rgba(255, 255, 255, 0.05);
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 8px;
	color: #9ca3af;
	font-size: 0.875rem;
	font-weight: 500;
	cursor: pointer;
	transition: all 0.2s;
}

.tab:hover {
	background: rgba(255, 255, 255, 0.1);
}

.tab.active {
	background: rgba(16, 185, 129, 0.2);
	border-color: rgba(16, 185, 129, 0.3);
	color: #10b981;
}

.ranking-container {
	background: rgba(255, 255, 255, 0.05);
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 16px;
	padding: 1.5rem;
}
</style>
