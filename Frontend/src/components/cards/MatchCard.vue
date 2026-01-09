<template>
	<div class="match-card">
		<div class="match-header">
			<span class="match-date"
				>📅 {{ formatDate(match.match_date) }}</span
			>
			<span class="match-season">{{ match.season_name }}</span>
		</div>

		<!-- League match với 2 đội -->
		<div
			v-if="match.home_team_name && match.away_team_name"
			class="match-teams"
		>
			<div class="team home">
				<span class="team-name">{{ match.home_team_name }}</span>
				<span class="team-score">{{
					match.home_score ?? homeGoals
				}}</span>
			</div>
			<span class="vs">-</span>
			<div class="team away">
				<span class="team-score">{{
					match.away_score ?? awayGoals
				}}</span>
				<span class="team-name">{{ match.away_team_name }}</span>
			</div>
		</div>

		<!-- Weekly match không có đội -->
		<div v-else class="match-info">
			<div v-if="match.venue" class="match-venue">
				📍 {{ match.venue }}
			</div>
		</div>

		<div class="match-stats">
			<div v-if="match.goal_count > 0" class="match-stat">
				⚽ {{ match.goal_count }} bàn thắng
			</div>
			<div v-if="match.card_count > 0" class="match-stat">
				🟨 {{ match.card_count }} thẻ phạt
			</div>
		</div>

		<!-- Chi tiết bàn thắng -->
		<div v-if="match.goals && match.goals.length" class="match-details">
			<div
				v-for="goal in match.goals"
				:key="goal.id"
				class="detail-item goal"
			>
				<span class="detail-icon">⚽</span>
				<span class="detail-text">
					{{ goal.player_name }}
					<span v-if="goal.minute">({{ goal.minute }}')</span>
					<span v-if="goal.assist_by_name" class="assist">
						- 🎯 {{ goal.assist_by_name }}</span
					>
				</span>
			</div>
		</div>

		<!-- Chi tiết thẻ phạt -->
		<div v-if="match.cards && match.cards.length" class="match-details">
			<div
				v-for="card in match.cards"
				:key="card.id"
				class="detail-item card"
			>
				<span class="detail-icon">{{
					card.card_type === "YELLOW" ? "🟨" : "🟥"
				}}</span>
				<span class="detail-text">
					{{ card.player_name }}
					<span v-if="card.minute">({{ card.minute }}')</span>
				</span>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed } from "vue";
import dayjs from "dayjs";

const props = defineProps({
	match: {
		type: Object,
		required: true,
	},
});

// Tính score từ goals nếu không có sẵn
const homeGoals = computed(() => {
	if (!props.match.goals) return 0;
	return (
		props.match.goals.filter(
			(g) =>
				g.for_team_id === props.match.home_team?.id ||
				g.for_team === props.match.home_team_name
		).length ||
		Math.ceil(props.match.goal_count / 2) ||
		0
	);
});

const awayGoals = computed(() => {
	if (!props.match.goals) return 0;
	return (
		props.match.goals.filter(
			(g) =>
				g.for_team_id === props.match.away_team?.id ||
				g.for_team === props.match.away_team_name
		).length ||
		Math.floor(props.match.goal_count / 2) ||
		0
	);
});

const formatDate = (date) => {
	if (!date) return "TBD";
	return dayjs(date).format("DD/MM/YYYY");
};
</script>

<style scoped>
.match-card {
	background: rgba(255, 255, 255, 0.05);
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 12px;
	padding: 1rem;
	transition: all 0.3s ease;
}

.match-card:hover {
	background: rgba(255, 255, 255, 0.08);
	border-color: rgba(16, 185, 129, 0.3);
}

.match-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 0.75rem;
	padding-bottom: 0.75rem;
	border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.match-date {
	font-size: 0.875rem;
	color: #9ca3af;
}

.match-season {
	font-size: 0.75rem;
	color: #10b981;
	background: rgba(16, 185, 129, 0.2);
	padding: 0.25rem 0.5rem;
	border-radius: 4px;
}

.match-teams {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 1rem;
	padding: 0.5rem 0;
}

.team {
	display: flex;
	align-items: center;
	gap: 0.75rem;
}

.team.home {
	flex-direction: row;
}

.team.away {
	flex-direction: row-reverse;
}

.team-name {
	font-weight: 600;
	color: #fff;
}

.team-score {
	font-size: 1.5rem;
	font-weight: 700;
	color: #10b981;
	min-width: 2rem;
	text-align: center;
}

.vs {
	color: #6b7280;
	font-weight: 600;
}

.match-info {
	padding: 0.5rem 0;
}

.match-venue {
	font-size: 0.875rem;
	color: #9ca3af;
}

.match-stats {
	display: flex;
	gap: 1rem;
	margin-top: 0.75rem;
	padding-top: 0.75rem;
	border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.match-stat {
	font-size: 0.875rem;
	color: #9ca3af;
}

.match-details {
	margin-top: 0.75rem;
	padding-top: 0.75rem;
	border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.detail-item {
	display: flex;
	align-items: center;
	gap: 0.5rem;
	padding: 0.25rem 0;
	font-size: 0.875rem;
}

.detail-icon {
	font-size: 0.875rem;
}

.detail-text {
	color: #d1d5db;
}

.assist {
	color: #9ca3af;
	font-size: 0.75rem;
}
</style>
