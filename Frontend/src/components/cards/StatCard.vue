<template>
	<div class="stat-card">
		<div class="stat-icon">{{ icon }}</div>
		<div class="stat-content">
			<div class="stat-value">{{ value }}</div>
			<div class="stat-label">{{ label }}</div>
		</div>
	</div>
</template>

<script setup>
defineProps({
	icon: {
		type: String,
		required: true,
	},
	value: {
		type: [String, Number],
		required: true,
	},
	label: {
		type: String,
		required: true,
	},
});
</script>

<style scoped>
.stat-card {
	background: linear-gradient(
		135deg,
		rgba(255, 255, 255, 0.1),
		rgba(255, 255, 255, 0.05)
	);
	backdrop-filter: blur(10px);
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 16px;
	padding: 1.5rem;
	display: flex;
	align-items: center;
	gap: 1rem;
	transition: all 0.3s ease;
}

.stat-card:hover {
	transform: translateY(-4px);
	box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
	border-color: rgba(16, 185, 129, 0.5);
}

.stat-icon {
	font-size: 2.5rem;
	background: linear-gradient(135deg, #10b981, #059669);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
}

.stat-content {
	flex: 1;
}

.stat-value {
	font-size: 2rem;
	font-weight: 700;
	color: #fff;
	line-height: 1;
}

.stat-label {
	font-size: 0.875rem;
	color: #9ca3af;
	margin-top: 0.25rem;
}
</style>
