<template>
	<div class="ranking-table">
		<table>
			<thead>
				<tr>
					<th class="rank">#</th>
					<th class="player">Cầu thủ</th>
					<th class="number">Trận</th>
					<th class="number value">{{ valueLabel }}</th>
					<th v-if="showRatio" class="number">Tỷ lệ</th>
					<th v-if="showTrend" class="trend">Trend</th>
				</tr>
			</thead>
			<tbody>
				<tr
					v-for="(item, index) in rankings"
					:key="item.player?.id || index"
				>
					<td class="rank">
						<span
							class="rank-badge"
							:class="{ 'top-three': index < 3 }"
						>
							{{ getRankIcon(index + 1) }}
						</span>
					</td>
					<td class="player">
						<router-link
							v-if="item.player"
							:to="`/players/${item.player.id}`"
							class="player-link"
						>
							<div class="player-avatar">
								<img
									v-if="item.player.avatar_url"
									:src="item.player.avatar_url"
									:alt="item.player.name"
								/>
								<div v-else class="avatar-placeholder">
									{{ getInitials(item.player.name) }}
								</div>
							</div>
							<span class="player-name">{{
								item.player.name
							}}</span>
						</router-link>
					</td>
					<td class="number">
						{{ item.player?.matches_played || "-" }}
					</td>
					<td class="number value">{{ item.value }}</td>
					<td v-if="showRatio" class="number ratio">
						{{ calculateRatio(item) }}
					</td>
					<td v-if="showTrend" class="trend">
						<span v-if="item.trend > 0" class="trend-up"
							>📈 +{{ item.trend }}</span
						>
						<span v-else-if="item.trend < 0" class="trend-down"
							>📉 {{ item.trend }}</span
						>
						<span v-else class="trend-same">➡️ 0</span>
					</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>

<script setup>
const props = defineProps({
	rankings: {
		type: Array,
		required: true,
	},
	type: {
		type: String,
		default: "goals", // goals, assists, cards
	},
	showRatio: {
		type: Boolean,
		default: false,
	},
	showTrend: {
		type: Boolean,
		default: false,
	},
});

const valueLabel =
	{
		goals: "Bàn",
		assists: "Kiến tạo",
		cards: "Thẻ",
		matches: "Trận",
	}[props.type] || "Giá trị";

const getRankIcon = (rank) => {
	if (rank === 1) return "👑";
	if (rank === 2) return "🥈";
	if (rank === 3) return "🥉";
	return rank;
};

const getInitials = (name) => {
	const names = name.split(" ");
	if (names.length >= 2) {
		return names[0][0] + names[names.length - 1][0];
	}
	return name.slice(0, 2).toUpperCase();
};

const calculateRatio = (item) => {
	const matches = item.player?.matches_played || 0;
	if (matches === 0) return "-";
	return (item.value / matches).toFixed(2);
};
</script>

<style scoped>
.ranking-table {
	overflow-x: auto;
}

table {
	width: 100%;
	border-collapse: collapse;
}

th,
td {
	padding: 0.75rem 0.5rem;
	text-align: left;
	border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

th {
	font-size: 0.75rem;
	font-weight: 600;
	color: #9ca3af;
	text-transform: uppercase;
	letter-spacing: 0.05em;
}

td {
	color: #d1d5db;
}

.rank {
	width: 50px;
	text-align: center;
}

.rank-badge {
	font-size: 1rem;
}

.rank-badge.top-three {
	font-size: 1.25rem;
}

.player {
	min-width: 200px;
}

.player-link {
	display: flex;
	align-items: center;
	gap: 0.75rem;
	text-decoration: none;
	color: inherit;
}

.player-link:hover .player-name {
	color: #10b981;
}

.player-avatar {
	width: 36px;
	height: 36px;
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
	font-size: 0.75rem;
	color: #fff;
}

.player-name {
	font-weight: 600;
	color: #fff;
	transition: color 0.2s;
}

.number {
	width: 60px;
	text-align: center;
}

.value {
	font-weight: 700;
	color: #10b981;
	font-size: 1.125rem;
}

.ratio {
	color: #f59e0b;
}

.trend {
	width: 80px;
	text-align: center;
}

.trend-up {
	color: #10b981;
}

.trend-down {
	color: #ef4444;
}

.trend-same {
	color: #9ca3af;
}

tr:hover {
	background: rgba(255, 255, 255, 0.05);
}
</style>
