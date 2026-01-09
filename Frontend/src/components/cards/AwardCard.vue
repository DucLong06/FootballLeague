<template>
	<div class="award-card" :class="{ 'award-card--shame': isShame }">
		<div class="award-icon">{{ award.icon }}</div>
		<div class="award-content">
			<h3 class="award-title">{{ award.title }}</h3>
			<p class="award-description">{{ award.description }}</p>
		</div>
		<div class="award-winner">
			<div class="winner-avatar">
				<img
					v-if="award.player?.avatar_url"
					:src="award.player.avatar_url"
					:alt="award.player.name"
				/>
				<div v-else class="avatar-placeholder">{{ initials }}</div>
			</div>
			<div class="winner-info">
				<span class="winner-name">{{
					award.player?.name || award.team?.name
				}}</span>
				<span class="winner-stat"
					>{{ formatValue(award.value) }} {{ statLabel }}</span
				>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
	award: {
		type: Object,
		required: true,
	},
	isShame: {
		type: Boolean,
		default: false,
	},
});

const initials = computed(() => {
	const name = props.award.player?.name || props.award.team?.name || "";
	const names = name.split(" ");
	if (names.length >= 2) {
		return names[0][0] + names[names.length - 1][0];
	}
	return name.slice(0, 2).toUpperCase();
});

const statLabel = computed(() => {
	const labels = {
		goals: "bàn",
		assists: "kiến tạo",
		matches_played: "trận",
		clean_sheets: "trận giữ sạch lưới",
		contribution: "điểm đóng góp",
		goal_ratio: "bàn/trận",
		red_cards: "thẻ đỏ",
		yellow_cards: "thẻ vàng",
		goals_conceded: "bàn thua",
		own_goals: "phản lưới",
	};
	return labels[props.award.stat] || "";
});

const formatValue = (value) => {
	if (typeof value === "number" && value % 1 !== 0) {
		return value.toFixed(2);
	}
	return value;
};
</script>

<style scoped>
.award-card {
	background: linear-gradient(
		135deg,
		rgba(16, 185, 129, 0.2),
		rgba(16, 185, 129, 0.05)
	);
	border: 1px solid rgba(16, 185, 129, 0.3);
	border-radius: 16px;
	padding: 1.5rem;
	display: flex;
	flex-direction: column;
	align-items: center;
	text-align: center;
	gap: 1rem;
	transition: all 0.3s ease;
}

.award-card:hover {
	transform: translateY(-4px);
	box-shadow: 0 10px 30px rgba(16, 185, 129, 0.2);
}

.award-card--shame {
	background: linear-gradient(
		135deg,
		rgba(239, 68, 68, 0.2),
		rgba(239, 68, 68, 0.05)
	);
	border-color: rgba(239, 68, 68, 0.3);
}

.award-card--shame:hover {
	box-shadow: 0 10px 30px rgba(239, 68, 68, 0.2);
}

.award-icon {
	font-size: 3rem;
	line-height: 1;
}

.award-content {
	flex: 1;
}

.award-title {
	font-size: 1rem;
	font-weight: 700;
	color: #fff;
	margin: 0;
	text-transform: uppercase;
	letter-spacing: 0.05em;
}

.award-description {
	font-size: 0.75rem;
	color: #9ca3af;
	margin: 0.5rem 0 0;
	font-style: italic;
}

.award-winner {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 0.5rem;
	padding-top: 1rem;
	border-top: 1px solid rgba(255, 255, 255, 0.1);
	width: 100%;
}

.winner-avatar {
	width: 56px;
	height: 56px;
	border-radius: 50%;
	overflow: hidden;
	border: 2px solid rgba(255, 255, 255, 0.2);
}

.winner-avatar img {
	width: 100%;
	height: 100%;
	object-fit: cover;
}

.avatar-placeholder {
	width: 100%;
	height: 100%;
	background: linear-gradient(135deg, #374151, #1f2937);
	display: flex;
	align-items: center;
	justify-content: center;
	font-weight: 600;
	color: #fff;
}

.winner-info {
	display: flex;
	flex-direction: column;
	align-items: center;
}

.winner-name {
	font-weight: 600;
	color: #fff;
}

.winner-stat {
	font-size: 0.875rem;
	color: #10b981;
}

.award-card--shame .winner-stat {
	color: #ef4444;
}
</style>
