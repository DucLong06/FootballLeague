<template>
	<router-link :to="`/players/${player.id}`" class="player-card">
		<div class="player-avatar">
			<img
				v-if="player.avatar_url"
				:src="player.avatar_url"
				:alt="player.name"
			/>
			<div v-else class="avatar-placeholder">{{ initials }}</div>
		</div>
		<div class="player-info">
			<h3 class="player-name">{{ player.name }}</h3>
			<p v-if="player.nickname" class="player-nickname">
				{{ player.nickname }}
			</p>

			<!-- Stats summary -->
			<div
				v-if="player.matches_played !== undefined"
				class="player-stats-summary"
			>
				<div class="stat-item" title="Số trận">
					<span>🎮</span> {{ player.matches_played }}
				</div>
				<div class="stat-item" title="Bàn thắng">
					<span>⚽</span> {{ player.goals }}
				</div>
				<div class="stat-item" title="Kiến tạo">
					<span>🎯</span> {{ player.assists }}
				</div>
			</div>
		</div>

		<div v-if="stat" class="player-stat">
			<span class="stat-icon">{{ statIcon }}</span>
			<span class="stat-value">{{ statValue }}</span>
		</div>
		<div v-if="awards && awards.length" class="player-awards">
			<span
				v-for="award in awards.slice(0, 2)"
				:key="award.title"
				class="award-badge"
				:title="award.title"
			>
				{{ award.icon }}
			</span>
		</div>
	</router-link>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
	player: {
		type: Object,
		required: true,
	},
	stat: {
		type: String,
		default: null, // 'goals', 'assists', 'cards', 'matches'
	},
	statValue: {
		type: [String, Number],
		default: null,
	},
	awards: {
		type: Array,
		default: () => [],
	},
});

const initials = computed(() => {
	const names = props.player.name.split(" ");
	if (names.length >= 2) {
		return names[0][0] + names[names.length - 1][0];
	}
	return names[0].slice(0, 2).toUpperCase();
});

const statIcon = computed(() => {
	const icons = {
		goals: "⚽",
		assists: "🎯",
		cards: "🟨",
		matches: "🎮",
		red_cards: "🟥",
		yellow_cards: "🟨",
	};
	return icons[props.stat] || "📊";
});
</script>

<style scoped>
.player-card {
	display: flex;
	align-items: center;
	gap: 1rem;
	padding: 1rem;
	background: rgba(255, 255, 255, 0.05);
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 12px;
	text-decoration: none;
	color: inherit;
	transition: all 0.3s ease;
}

.player-card:hover {
	background: rgba(255, 255, 255, 0.1);
	transform: translateX(4px);
	border-color: rgba(16, 185, 129, 0.5);
}

.player-avatar {
	width: 48px;
	height: 48px;
	border-radius: 50%;
	overflow: hidden;
	flex-shrink: 0;
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
	font-weight: 600;
	font-size: 1rem;
	color: #fff;
}

.player-info {
	flex: 1;
	min-width: 0;
}

.player-name {
	font-size: 1rem;
	font-weight: 600;
	color: #fff;
	margin: 0;
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
}

.player-nickname {
	font-size: 0.75rem;
	color: #9ca3af;
	margin: 0.25rem 0 0;
}

.player-stats-summary {
	display: flex;
	gap: 0.75rem;
	margin-top: 0.5rem;
}

.stat-item {
	display: flex;
	align-items: center;
	gap: 0.25rem;
	font-size: 0.75rem;
	color: #d1d5db;
	background: rgba(255, 255, 255, 0.05);
	padding: 0.25rem 0.5rem;
	border-radius: 6px;
}

.stat-item span {
	font-size: 0.875rem;
}

.player-stat {
	display: flex;
	align-items: center;
	gap: 0.5rem;
	padding: 0.5rem 0.75rem;
	background: rgba(16, 185, 129, 0.2);
	border-radius: 8px;
}

.stat-icon {
	font-size: 1rem;
}

.stat-value {
	font-weight: 700;
	color: #10b981;
}

.player-awards {
	display: flex;
	gap: 0.25rem;
}

.award-badge {
	font-size: 1.25rem;
	cursor: help;
}
</style>
