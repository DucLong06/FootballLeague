<template>
	<div class="standings-table">
		<table>
			<thead>
				<tr>
					<th class="rank">#</th>
					<th class="team">Đội</th>
					<th class="number">Trận</th>
					<th class="number">Thắng</th>
					<th class="number">Hòa</th>
					<th class="number">Thua</th>
					<th class="number">Ghi</th>
					<th class="number">Nhận</th>
					<th class="number">HS</th>
					<th class="number points">Điểm</th>
					<th v-if="showForm" class="form">Phong độ</th>
				</tr>
			</thead>
			<tbody>
				<tr
					v-for="standing in standings"
					:key="standing.id"
					:class="getRowClass(standing.rank)"
				>
					<td class="rank">
						<span class="rank-badge">{{
							getRankIcon(standing.rank)
						}}</span>
					</td>
					<td class="team">
						<div class="team-info">
							<img
								v-if="standing.team?.logo_url"
								:src="standing.team.logo_url"
								:alt="standing.team.name"
								class="team-logo"
							/>
							<span class="team-name">{{
								standing.team?.name || "Đội " + standing.rank
							}}</span>
						</div>
					</td>
					<td class="number">{{ standing.played }}</td>
					<td class="number win">{{ standing.won }}</td>
					<td class="number draw">{{ standing.drawn }}</td>
					<td class="number loss">{{ standing.lost }}</td>
					<td class="number">{{ standing.goals_for }}</td>
					<td class="number">{{ standing.goals_against }}</td>
					<td
						class="number"
						:class="{
							positive: standing.goal_diff > 0,
							negative: standing.goal_diff < 0,
						}"
					>
						{{ standing.goal_diff > 0 ? "+" : ""
						}}{{ standing.goal_diff }}
					</td>
					<td class="number points">{{ standing.points }}</td>
					<td v-if="showForm" class="form">
						<div class="form-badges">
							<span
								v-for="(result, index) in standing.form"
								:key="index"
								class="form-badge"
								:class="result.toLowerCase()"
							>
								{{
									result === "W"
										? "✅"
										: result === "D"
										? "⬜"
										: "❌"
								}}
							</span>
						</div>
					</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>

<script setup>
defineProps({
	standings: {
		type: Array,
		required: true,
	},
	showForm: {
		type: Boolean,
		default: true,
	},
});

const getRankIcon = (rank) => {
	if (rank === 1) return "🥇";
	if (rank === 2) return "🥈";
	if (rank === 3) return "🥉";
	return rank;
};

const getRowClass = (rank) => {
	if (rank === 1) return "champion";
	if (rank <= 3) return "top-three";
	return "";
};
</script>

<style scoped>
.standings-table {
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

.team {
	min-width: 150px;
}

.team-info {
	display: flex;
	align-items: center;
	gap: 0.75rem;
}

.team-logo {
	width: 24px;
	height: 24px;
	border-radius: 4px;
	object-fit: cover;
}

.team-name {
	font-weight: 600;
	color: #fff;
}

.number {
	width: 40px;
	text-align: center;
}

.points {
	font-weight: 700;
	color: #10b981;
	font-size: 1rem;
}

.positive {
	color: #10b981;
}

.negative {
	color: #ef4444;
}

.win {
	color: #10b981;
}

.draw {
	color: #f59e0b;
}

.loss {
	color: #ef4444;
}

.form {
	width: 120px;
}

.form-badges {
	display: flex;
	gap: 0.25rem;
}

.form-badge {
	font-size: 0.75rem;
}

tr.champion {
	background: linear-gradient(90deg, rgba(16, 185, 129, 0.2), transparent);
}

tr.top-three {
	background: rgba(255, 255, 255, 0.02);
}

tr:hover {
	background: rgba(255, 255, 255, 0.05);
}
</style>
