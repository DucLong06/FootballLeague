<template>
	<div class="overview-page">
		<!-- Loading State -->
		<div v-if="overviewStore.loading" class="loading-state">
			<div class="loader"></div>
			<p>Đang tải dữ liệu...</p>
		</div>

		<!-- Content -->
		<template v-else>
			<!-- Hero Section -->
			<section class="hero-section">
				<h1 class="page-title">⚽ CSOC Football</h1>
				<p class="page-subtitle">Thống kê & Xếp hạng cầu thủ</p>

				<div class="stats-grid">
					<StatCard
						icon="👥"
						:value="stats?.totalPlayers || 0"
						label="Cầu Thủ"
					/>
					<StatCard
						icon="⚽"
						:value="stats?.totalGoals || 0"
						label="Bàn Thắng"
					/>
					<StatCard
						icon="🎮"
						:value="stats?.totalMatches || 0"
						label="Trận Đấu"
					/>
					<StatCard
						icon="🟨"
						:value="stats?.totalCards || 0"
						label="Thẻ Phạt"
					/>
				</div>
			</section>

			<!-- Season Selector -->
			<section class="season-selector">
				<div class="selector-header">
					<span class="selector-label"
						>📅 Xem thống kê theo mùa giải:</span
					>
					<select
						v-model="selectedSeason"
						@change="onSeasonChange"
						class="season-select"
					>
						<option value="">Tổng hợp tất cả</option>
						<option
							v-for="season in matchesStore.seasons"
							:key="season.id"
							:value="season.id"
						>
							{{ season.type === "WEEKLY" ? "🗓️" : "🏆" }}
							{{ season.name }}
						</option>
					</select>
					<router-link
						v-if="selectedSeason"
						:to="`/seasons/${selectedSeason}`"
						class="view-stats-btn"
					>
						📊 Xem chi tiết
					</router-link>
				</div>
			</section>

			<!-- Current Season Active -->
			<section
				v-if="overviewStore.currentSeason && !selectedSeason"
				class="season-banner"
			>
				<div class="season-content">
					<span class="season-type">{{
						overviewStore.currentSeason.type === "WEEKLY"
							? "🗓️ Đá Phong Trào"
							: "🏆 Giải Đấu"
					}}</span>
					<h2 class="season-name">
						{{ overviewStore.currentSeason.name }}
					</h2>
				</div>
				<router-link
					v-if="overviewStore.currentSeason.type === 'LEAGUE'"
					to="/standings"
					class="season-action"
				>
					Xem BXH →
				</router-link>
			</section>

			<!-- Hall of Fame Section -->
			<section
				v-if="overviewStore.gloryAwards.length"
				class="awards-section"
			>
				<h2 class="section-title">
					🏆 Hall of Fame {{ selectedSeasonName }}
				</h2>
				<div class="awards-grid">
					<AwardCard
						v-for="award in overviewStore.gloryAwards"
						:key="award.key"
						:award="award"
					/>
				</div>
			</section>

			<!-- Wall of Shame Section -->
			<section
				v-if="overviewStore.shameAwards.length"
				class="awards-section shame"
			>
				<h2 class="section-title">
					😈 Bảng Phong Thần {{ selectedSeasonName }}
				</h2>
				<div class="awards-grid">
					<AwardCard
						v-for="award in overviewStore.shameAwards"
						:key="award.key"
						:award="award"
						:is-shame="true"
					/>
				</div>
			</section>

			<!-- Top Charts Section -->
			<section class="charts-section">
				<h2 class="section-title">
					📊 Bảng Xếp Hạng Cá Nhân {{ selectedSeasonName }}
				</h2>
				<div class="charts-grid">
					<div class="chart-card">
						<h3 class="chart-title">⚽ Top Ghi Bàn</h3>
						<div
							class="chart-container"
							v-if="topScorersData.labels.length"
						>
							<BarChart
								:labels="topScorersData.labels"
								:data="topScorersData.data"
								label="Bàn"
								background-color="rgba(16, 185, 129, 0.8)"
							/>
						</div>
						<div v-else class="no-data">Chưa có dữ liệu</div>
					</div>

					<div class="chart-card">
						<h3 class="chart-title">🎯 Top Kiến Tạo</h3>
						<div
							class="chart-container"
							v-if="topAssistsData.labels.length"
						>
							<BarChart
								:labels="topAssistsData.labels"
								:data="topAssistsData.data"
								label="Assist"
								background-color="rgba(30, 64, 175, 0.8)"
							/>
						</div>
						<div v-else class="no-data">Chưa có dữ liệu</div>
					</div>

					<div class="chart-card">
						<h3 class="chart-title">🟨 Top Thẻ Phạt</h3>
						<div
							class="chart-container"
							v-if="topCardsData.labels.length"
						>
							<BarChart
								:labels="topCardsData.labels"
								:data="topCardsData.data"
								label="Thẻ"
								background-color="rgba(245, 158, 11, 0.8)"
							/>
						</div>
						<div v-else class="no-data">Chưa có dữ liệu</div>
					</div>
				</div>
			</section>

			<!-- Recent Matches Section -->
			<section class="matches-section">
				<div class="section-header">
					<h2 class="section-title">📅 Trận Đấu Gần Đây</h2>
					<router-link to="/matches" class="view-all"
						>Xem tất cả →</router-link
					>
				</div>
				<div
					v-if="matchesStore.recentMatches.length"
					class="matches-grid"
				>
					<MatchCard
						v-for="match in matchesStore.recentMatches"
						:key="match.id"
						:match="match"
					/>
				</div>
				<div v-else class="no-data-box">
					<p>Chưa có trận đấu nào</p>
				</div>
			</section>
		</template>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useOverviewStore } from "../stores/overview";
import { useMatchesStore } from "../stores/matches";
import StatCard from "../components/cards/StatCard.vue";
import AwardCard from "../components/cards/AwardCard.vue";
import MatchCard from "../components/cards/MatchCard.vue";
import BarChart from "../components/charts/BarChart.vue";

const overviewStore = useOverviewStore();
const matchesStore = useMatchesStore();

const selectedSeason = ref("");

const stats = computed(() => overviewStore.stats);

const selectedSeasonName = computed(() => {
	if (!selectedSeason.value) return "";
	const season = matchesStore.seasons.find(
		(s) => s.id === selectedSeason.value
	);
	return season ? `- ${season.name}` : "";
});

const topScorersData = computed(() => ({
	labels: overviewStore.topScorers
		.slice(0, 8)
		.map(
			(item) => item.player.nickname || item.player.name.split(" ").pop()
		),
	data: overviewStore.topScorers.slice(0, 8).map((item) => item.goals),
}));

const topAssistsData = computed(() => ({
	labels: overviewStore.topAssists
		.slice(0, 8)
		.map(
			(item) => item.player.nickname || item.player.name.split(" ").pop()
		),
	data: overviewStore.topAssists.slice(0, 8).map((item) => item.assists),
}));

const topCardsData = computed(() => ({
	labels: overviewStore.topCards
		.slice(0, 8)
		.map(
			(item) => item.player.nickname || item.player.name.split(" ").pop()
		),
	data: overviewStore.topCards.slice(0, 8).map((item) => item.total),
}));

const onSeasonChange = () => {
	// In a real app, you'd call API with season filter
	// For now, refetch overview (could add season param to API)
	overviewStore.fetchOverview();
};

onMounted(() => {
	overviewStore.fetchOverview();
	matchesStore.fetchSeasons();
	matchesStore.fetchRecentMatches(5);
});
</script>

<style scoped>
.overview-page {
	max-width: 1200px;
	margin: 0 auto;
	padding: 1.5rem 1rem;
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

/* Hero */
.hero-section {
	text-align: center;
	margin-bottom: 2rem;
}

.page-title {
	font-size: 2.5rem;
	font-weight: 800;
	margin: 0;
	background: linear-gradient(135deg, #1e40af, #10b981);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
}

.page-subtitle {
	font-size: 1rem;
	color: #9ca3af;
	margin: 0.5rem 0 1.5rem;
}

.stats-grid {
	display: grid;
	grid-template-columns: repeat(4, 1fr);
	gap: 1rem;
	max-width: 800px;
	margin: 0 auto;
}

/* Season Selector */
.season-selector {
	margin-bottom: 1.5rem;
}

.selector-header {
	display: flex;
	align-items: center;
	gap: 1rem;
	padding: 1rem;
	background: rgba(255, 255, 255, 0.05);
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 12px;
	flex-wrap: wrap;
}

.selector-label {
	color: #9ca3af;
	font-size: 0.875rem;
}

.season-select {
	flex: 1;
	max-width: 350px;
	padding: 0.5rem 1rem;
	background: rgba(255, 255, 255, 0.05);
	border: 1px solid rgba(255, 255, 255, 0.2);
	border-radius: 8px;
	color: #fff;
	font-size: 0.875rem;
}

.season-select option {
	background: #1f2937;
}

.view-stats-btn {
	padding: 0.5rem 1rem;
	background: linear-gradient(135deg, #1e40af, #10b981);
	color: #fff;
	border-radius: 8px;
	text-decoration: none;
	font-weight: 600;
	font-size: 0.875rem;
	transition: transform 0.2s, box-shadow 0.2s;
}

.view-stats-btn:hover {
	transform: translateY(-2px);
	box-shadow: 0 4px 12px rgba(30, 64, 175, 0.4);
}

/* Season Banner */
.season-banner {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 1rem 1.5rem;
	background: linear-gradient(
		135deg,
		rgba(30, 64, 175, 0.2),
		rgba(16, 185, 129, 0.1)
	);
	border: 1px solid rgba(30, 64, 175, 0.3);
	border-radius: 12px;
	margin-bottom: 2rem;
	flex-wrap: wrap;
	gap: 1rem;
}

.season-type {
	font-size: 0.75rem;
	color: #10b981;
}

.season-name {
	font-size: 1.25rem;
	font-weight: 700;
	color: #fff;
	margin: 0.25rem 0 0;
}

.season-action {
	padding: 0.5rem 1rem;
	background: #1e40af;
	color: #fff;
	border-radius: 6px;
	text-decoration: none;
	font-weight: 600;
	font-size: 0.875rem;
}

/* Section */
.section-title {
	font-size: 1.125rem;
	font-weight: 700;
	color: #fff;
	margin: 0 0 1rem;
}

.section-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 1rem;
}

.view-all {
	color: #10b981;
	text-decoration: none;
	font-size: 0.875rem;
}

/* Awards */
.awards-section {
	margin-bottom: 2rem;
	padding: 1.5rem;
	background: rgba(16, 185, 129, 0.05);
	border: 1px solid rgba(16, 185, 129, 0.2);
	border-radius: 16px;
}

.awards-section.shame {
	background: rgba(239, 68, 68, 0.05);
	border-color: rgba(239, 68, 68, 0.2);
}

.awards-grid {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
	gap: 1rem;
}

/* Charts */
.charts-section {
	margin-bottom: 2rem;
}

.charts-grid {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
	gap: 1rem;
}

.chart-card {
	background: rgba(255, 255, 255, 0.05);
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 12px;
	padding: 1rem;
}

.chart-title {
	font-size: 0.875rem;
	font-weight: 600;
	color: #fff;
	margin: 0 0 0.75rem;
}

.chart-container {
	height: 220px;
}

.no-data {
	display: flex;
	align-items: center;
	justify-content: center;
	height: 150px;
	color: #6b7280;
	font-size: 0.875rem;
}

/* Matches */
.matches-section {
	margin-bottom: 2rem;
}

.matches-grid {
	display: grid;
	gap: 0.75rem;
}

.no-data-box {
	text-align: center;
	padding: 2rem;
	background: rgba(255, 255, 255, 0.02);
	border: 1px dashed rgba(255, 255, 255, 0.1);
	border-radius: 12px;
	color: #6b7280;
}

@media (max-width: 768px) {
	.page-title {
		font-size: 1.75rem;
	}
	.stats-grid {
		grid-template-columns: repeat(2, 1fr);
	}
	.charts-grid {
		grid-template-columns: 1fr;
	}
	.selector-header {
		flex-direction: column;
		align-items: stretch;
	}
	.season-select {
		max-width: none;
	}
}
</style>
