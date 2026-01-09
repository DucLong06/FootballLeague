<template>
	<Pie :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { computed } from "vue";
import { Pie } from "vue-chartjs";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

const props = defineProps({
	labels: {
		type: Array,
		required: true,
	},
	data: {
		type: Array,
		required: true,
	},
	title: {
		type: String,
		default: "",
	},
});

const colors = [
	"rgba(16, 185, 129, 0.8)",
	"rgba(59, 130, 246, 0.8)",
	"rgba(245, 158, 11, 0.8)",
	"rgba(239, 68, 68, 0.8)",
	"rgba(139, 92, 246, 0.8)",
	"rgba(236, 72, 153, 0.8)",
	"rgba(14, 165, 233, 0.8)",
	"rgba(34, 197, 94, 0.8)",
];

const chartData = computed(() => ({
	labels: props.labels,
	datasets: [
		{
			data: props.data,
			backgroundColor: colors.slice(0, props.data.length),
			borderWidth: 0,
		},
	],
}));

const chartOptions = computed(() => ({
	responsive: true,
	maintainAspectRatio: false,
	plugins: {
		legend: {
			position: "right",
			labels: {
				color: "#9ca3af",
				padding: 20,
			},
		},
		title: {
			display: !!props.title,
			text: props.title,
			color: "#fff",
			font: {
				size: 14,
				weight: "bold",
			},
		},
	},
}));
</script>
