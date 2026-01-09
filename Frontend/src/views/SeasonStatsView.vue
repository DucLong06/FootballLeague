<template>
	<div class="season-stats-page">
		<!-- Loading -->
		<div v-if="loading" class="loading-state">
			<div class="loader"></div>
			<p>Đang tải thống kê...</p>
		</div>

		<!-- Content -->
		<template v-else-if="stats">
			<!-- Header -->
			<div class="page-header">
				<router-link to="/" class="back-btn">← Trang chủ</router-link>
				<div
					class="season-badge"
					:class="
						stats.season?.type === 'LEAGUE' ? 'league' : 'weekly'
					"
				>
					{{ stats.season?.type === "LEAGUE" ? "🏆" : "🗓️" }}
				</div>
				<h1 class="page-title">{{ stats.season?.name }}</h1>
				<p class="page-subtitle">Thống kê chi tiết mùa giải</p>
			</div>

			<!-- Overview Stats -->
			<section class="stats-overview">
				<div class="stat-card primary">
					<span class="stat-icon">👥</span>
					<span class="stat-value">{{ stats.total_players }}</span>
					<span class="stat-label">VĐV Tham Gia</span>
				</div>
				<div class="stat-card">
					<span class="stat-icon">🎮</span>
					<span class="stat-value">{{ stats.total_matches }}</span>
					<span class="stat-label">Trận Đấu</span>
				</div>
				<div class="stat-card success">
					<span class="stat-icon">⚽</span>
					<span class="stat-value">{{ stats.total_goals }}</span>
					<span class="stat-label">Bàn Thắng</span>
				</div>
				<div class="stat-card danger">
					<span class="stat-icon">🥅</span>
					<span class="stat-value">{{ stats.total_own_goals }}</span>
					<span class="stat-label">Phản Lưới</span>
				</div>
				<div class="stat-card warning">
					<span class="stat-icon">🟨</span>
					<span class="stat-value">{{ stats.yellow_cards }}</span>
					<span class="stat-label">Thẻ Vàng</span>
				</div>
				<div class="stat-card danger">
					<span class="stat-icon">🟥</span>
					<span class="stat-value">{{ stats.red_cards }}</span>
					<span class="stat-label">Thẻ Đỏ</span>
				</div>
			</section>

			<!-- Advanced Stats -->
			<section class="advanced-stats">
				<h2 class="section-title">📈 Thống Kê Nâng Cao</h2>
				<div class="advanced-grid">
					<div class="advanced-card">
						<div class="advanced-icon">📊</div>
						<div class="advanced-content">
							<span class="advanced-value">{{
								stats.avg_goals_per_match
							}}</span>
							<span class="advanced-label">TB bàn/trận</span>
						</div>
					</div>
					<div class="advanced-card">
						<div class="advanced-icon">✌️</div>
						<div class="advanced-content">
							<span class="advanced-value">{{
								stats.braces
							}}</span>
							<span class="advanced-label">Cú Đúp</span>
						</div>
					</div>
					<div class="advanced-card">
						<div class="advanced-icon">🎩</div>
						<div class="advanced-content">
							<span class="advanced-value">{{
								stats.hat_tricks
							}}</span>
							<span class="advanced-label">Hat-trick</span>
						</div>
					</div>
					<div class="advanced-card">
						<div class="advanced-icon">🃏</div>
						<div class="advanced-content">
							<span class="advanced-value">{{
								stats.pokers
							}}</span>
							<span class="advanced-label">Poker (4+)</span>
						</div>
					</div>
				</div>
			</section>

			<!-- Best Match -->
			<section v-if="stats.best_match" class="highlight-section">
				<h2 class="section-title">🔥 Trận Nhiều Bàn Nhất</h2>
				<div class="highlight-card best">
					<div class="highlight-icon">⚽</div>
					<div class="highlight-content">
						<div class="highlight-teams">
							<span v-if="stats.best_match.home_team">{{
								stats.best_match.home_team.name
							}}</span>
							<span v-else>Đội A</span>
							<span class="score"
								>{{ stats.best_match_goals }} bàn</span
							>
							<span v-if="stats.best_match.away_team">{{
								stats.best_match.away_team.name
							}}</span>
							<span v-else>Đội B</span>
						</div>
						<div class="highlight-date">
							{{ formatDate(stats.best_match.match_date) }}
						</div>
					</div>
				</div>
			</section>

			<!-- Worst Match -->
			<section
				v-if="stats.worst_match && stats.worst_match_cards > 0"
				class="highlight-section"
			>
				<h2 class="section-title">🔴 Trận Nhiều Thẻ Nhất</h2>
				<div class="highlight-card worst">
					<div class="highlight-icon">🟨🟥</div>
					<div class="highlight-content">
						<div class="highlight-teams">
							<span v-if="stats.worst_match.home_team">{{
								stats.worst_match.home_team.name
							}}</span>
							<span v-else>Đội A</span>
							<span class="score danger"
								>{{ stats.worst_match_cards }} thẻ</span
							>
							<span v-if="stats.worst_match.away_team">{{
								stats.worst_match.away_team.name
							}}</span>
							<span v-else>Đội B</span>
						</div>
						<div class="highlight-date">
							{{ formatDate(stats.worst_match.match_date) }}
						</div>
					</div>
				</div>
			</section>

			<!-- Team Stats (League only) -->
			<section
				v-if="stats.team_most_goals || stats.team_most_cards"
				class="team-stats"
			>
				<h2 class="section-title">🏟️ Thống Kê Đội Bóng</h2>
				<div class="team-grid">
					<div v-if="stats.team_most_goals" class="team-card success">
						<div class="team-icon">⚔️</div>
						<div class="team-name">
							{{ stats.team_most_goals.name }}
						</div>
						<div class="team-stat">
							{{ stats.team_most_goals_count }} bàn
						</div>
						<div class="team-label">Đội Ghi Nhiều Nhất</div>
					</div>
					<div v-if="stats.team_most_cards" class="team-card danger">
						<div class="team-icon">🎴</div>
						<div class="team-name">
							{{ stats.team_most_cards.name }}
						</div>
						<div class="team-stat">
							{{ stats.team_most_cards_count }} thẻ
						</div>
						<div class="team-label">Đội Nhiều Thẻ Nhất</div>
					</div>
				</div>
			</section>

			<!-- Top Rankings -->
			<section class="rankings-section">
				<h2 class="section-title">🏆 Bảng Xếp Hạng Cá Nhân</h2>
				<div class="rankings-grid">
					<!-- Top Scorers -->
					<div class="ranking-card">
						<h3 class="ranking-title">⚽ Top Ghi Bàn</h3>
						<div class="ranking-list">
							<div
								v-for="(item, idx) in stats.top_scorers"
								:key="item.player.id"
								class="ranking-item"
							>
								<span
									class="ranking-pos"
									:class="getRankClass(idx)"
									>{{ idx + 1 }}</span
								>
								<span class="ranking-name">{{
									item.player.nickname || item.player.name
								}}</span>
								<span class="ranking-value success">{{
									item.goals
								}}</span>
							</div>
						</div>
					</div>

					<!-- Top Assists -->
					<div class="ranking-card">
						<h3 class="ranking-title">🎯 Top Kiến Tạo</h3>
						<div class="ranking-list">
							<div
								v-for="(item, idx) in stats.top_assists"
								:key="item.player.id"
								class="ranking-item"
							>
								<span
									class="ranking-pos"
									:class="getRankClass(idx)"
									>{{ idx + 1 }}</span
								>
								<span class="ranking-name">{{
									item.player.nickname || item.player.name
								}}</span>
								<span class="ranking-value primary">{{
									item.assists
								}}</span>
							</div>
						</div>
					</div>

					<!-- Top Cards -->
					<div class="ranking-card">
						<h3 class="ranking-title">🟨 Top Thẻ Phạt</h3>
						<div class="ranking-list">
							<div
								v-for="(item, idx) in stats.top_cards"
								:key="item.player.id"
								class="ranking-item"
							>
								<span
									class="ranking-pos"
									:class="getRankClass(idx)"
									>{{ idx + 1 }}</span
								>
								<span class="ranking-name">{{
									item.player.nickname || item.player.name
								}}</span>
								<span class="ranking-value warning"
									>{{ item.yellow }}🟨 {{ item.red }}🟥</span
								>
							</div>
						</div>
					</div>
				</div>
			</section>
		</template>

		<!-- Empty State -->
		<div v-else class="empty-state">
			<p>Không tìm thấy dữ liệu mùa giải</p>
			<router-link to="/">← Về trang chủ</router-link>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import { seasonsApi } from "../services/api";

const route = useRoute();
const loading = ref(true);
const stats = ref(null);

const formatDate = (dateStr) => {
	if (!dateStr) return "";
	const date = new Date(dateStr);
	return date.toLocaleDateString("vi-VN", {
		day: "2-digit",
		month: "2-digit",
		year: "numeric",
	});
};

const getRankClass = (idx) => {
	if (idx === 0) return "gold";
	if (idx === 1) return "silver";
	if (idx === 2) return "bronze";
	return "";
};

const fetchStats = async () => {
	loading.value = true;
	try {
		const response = await seasonsApi.stats(route.params.id);
		stats.value = response.data;
	} catch (err) {
		console.error("Failed to fetch season stats:", err);
	} finally {
		loading.value = false;
	}
};

watch(() => route.params.id, fetchStats);
onMounted(fetchStats);
</script>

<style scoped>
.season-stats-page {
	max-width: 1100px;
	margin: 0 auto;
	padding: 1.5rem 1rem;
}

.loading-state,
.empty-state {
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

/* Header */
.page-header {
	text-align: center;
	margin-bottom: 2rem;
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

.season-badge {
	display: inline-flex;
	width: 56px;
	height: 56px;
	align-items: center;
	justify-content: center;
	font-size: 1.75rem;
	margin-bottom: 0.75rem;
	border-radius: 50%;
	background: rgba(30, 64, 175, 0.2);
	border: 2px solid rgba(30, 64, 175, 0.4);
}

.season-badge.league {
	background: rgba(245, 158, 11, 0.2);
	border-color: rgba(245, 158, 11, 0.4);
}

.page-title {
	font-size: 2rem;
	font-weight: 800;
	color: #fff;
	margin: 0;
}

.page-subtitle {
	font-size: 0.875rem;
	color: #9ca3af;
	margin: 0.25rem 0 0;
}

/* Overview Stats */
.stats-overview {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
	gap: 1rem;
	margin-bottom: 2rem;
}

.stat-card {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 1.25rem 1rem;
	background: rgba(255, 255, 255, 0.05);
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 16px;
	text-align: center;
}

.stat-card.primary {
	border-color: rgba(30, 64, 175, 0.4);
	background: rgba(30, 64, 175, 0.1);
}
.stat-card.success {
	border-color: rgba(16, 185, 129, 0.4);
	background: rgba(16, 185, 129, 0.1);
}
.stat-card.warning {
	border-color: rgba(245, 158, 11, 0.4);
	background: rgba(245, 158, 11, 0.1);
}
.stat-card.danger {
	border-color: rgba(239, 68, 68, 0.4);
	background: rgba(239, 68, 68, 0.1);
}

.stat-icon {
	font-size: 1.5rem;
	margin-bottom: 0.5rem;
}
.stat-value {
	font-size: 2rem;
	font-weight: 800;
	color: #fff;
}
.stat-label {
	font-size: 0.75rem;
	color: #9ca3af;
	margin-top: 0.25rem;
}

/* Section Title */
.section-title {
	font-size: 1.125rem;
	font-weight: 700;
	color: #fff;
	margin: 0 0 1rem;
}

/* Advanced Stats */
.advanced-stats {
	margin-bottom: 2rem;
}

.advanced-grid {
	display: grid;
	grid-template-columns: repeat(4, 1fr);
	gap: 1rem;
}

.advanced-card {
	display: flex;
	align-items: center;
	gap: 0.75rem;
	padding: 1rem;
	background: rgba(255, 255, 255, 0.05);
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 12px;
}

.advanced-icon {
	font-size: 1.5rem;
}

.advanced-value {
	font-size: 1.5rem;
	font-weight: 700;
	color: #10b981;
	display: block;
}
.advanced-label {
	font-size: 0.75rem;
	color: #9ca3af;
}

/* Highlight Section */
.highlight-section {
	margin-bottom: 2rem;
}

.highlight-card {
	display: flex;
	align-items: center;
	gap: 1.25rem;
	padding: 1.25rem;
	border-radius: 16px;
}

.highlight-card.best {
	background: linear-gradient(
		135deg,
		rgba(16, 185, 129, 0.15),
		rgba(16, 185, 129, 0.05)
	);
	border: 1px solid rgba(16, 185, 129, 0.3);
}

.highlight-card.worst {
	background: linear-gradient(
		135deg,
		rgba(239, 68, 68, 0.15),
		rgba(239, 68, 68, 0.05)
	);
	border: 1px solid rgba(239, 68, 68, 0.3);
}

.highlight-icon {
	font-size: 2rem;
}

.highlight-teams {
	display: flex;
	align-items: center;
	gap: 0.75rem;
	font-weight: 600;
	color: #fff;
}

.score {
	padding: 0.5rem 1rem;
	background: rgba(16, 185, 129, 0.2);
	color: #10b981;
	border-radius: 8px;
	font-weight: 700;
}

.score.danger {
	background: rgba(239, 68, 68, 0.2);
	color: #ef4444;
}

.highlight-date {
	font-size: 0.75rem;
	color: #9ca3af;
	margin-top: 0.25rem;
}

/* Team Stats */
.team-stats {
	margin-bottom: 2rem;
}

.team-grid {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
	gap: 1rem;
}

.team-card {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 1.5rem;
	border-radius: 16px;
	text-align: center;
}

.team-card.success {
	background: linear-gradient(
		135deg,
		rgba(16, 185, 129, 0.15),
		rgba(16, 185, 129, 0.05)
	);
	border: 1px solid rgba(16, 185, 129, 0.3);
}

.team-card.danger {
	background: linear-gradient(
		135deg,
		rgba(239, 68, 68, 0.15),
		rgba(239, 68, 68, 0.05)
	);
	border: 1px solid rgba(239, 68, 68, 0.3);
}

.team-icon {
	font-size: 2rem;
	margin-bottom: 0.5rem;
}
.team-name {
	font-size: 1.125rem;
	font-weight: 700;
	color: #fff;
}
.team-stat {
	font-size: 1.5rem;
	font-weight: 800;
	color: #10b981;
	margin: 0.25rem 0;
}
.team-card.danger .team-stat {
	color: #ef4444;
}
.team-label {
	font-size: 0.75rem;
	color: #9ca3af;
}

/* Rankings */
.rankings-section {
	margin-bottom: 2rem;
}

.rankings-grid {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
	gap: 1rem;
}

.ranking-card {
	background: rgba(255, 255, 255, 0.05);
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 16px;
	padding: 1.25rem;
}

.ranking-title {
	font-size: 0.875rem;
	font-weight: 600;
	color: #fff;
	margin: 0 0 0.75rem;
}

.ranking-list {
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
}

.ranking-item {
	display: flex;
	align-items: center;
	gap: 0.75rem;
	padding: 0.5rem;
	background: rgba(255, 255, 255, 0.02);
	border-radius: 8px;
}

.ranking-pos {
	width: 24px;
	height: 24px;
	display: flex;
	align-items: center;
	justify-content: center;
	background: rgba(255, 255, 255, 0.1);
	border-radius: 50%;
	font-size: 0.75rem;
	font-weight: 700;
	color: #9ca3af;
}

.ranking-pos.gold {
	background: #eab308;
	color: #000;
}
.ranking-pos.silver {
	background: #9ca3af;
	color: #000;
}
.ranking-pos.bronze {
	background: #b45309;
	color: #fff;
}

.ranking-name {
	flex: 1;
	font-size: 0.875rem;
	color: #fff;
}
.ranking-value {
	font-weight: 700;
	font-size: 0.875rem;
}
.ranking-value.success {
	color: #10b981;
}
.ranking-value.primary {
	color: #3b82f6;
}
.ranking-value.warning {
	color: #9ca3af;
}

@media (max-width: 768px) {
	.advanced-grid {
		grid-template-columns: repeat(2, 1fr);
	}
	.rankings-grid {
		grid-template-columns: 1fr;
	}
	.highlight-teams {
		flex-wrap: wrap;
		justify-content: center;
	}
}
</style>
