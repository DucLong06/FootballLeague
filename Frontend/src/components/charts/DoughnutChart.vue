<template>
	<Doughnut :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { computed } from "vue";
import { Doughnut } from "vue-chartjs";
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
	centerText: {
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
];

const chartData = computed(() => ({
	labels: props.labels,
	datasets: [
		{
			data: props.data,
			backgroundColor: colors.slice(0, props.data.length),
			borderWidth: 0,
			cutout: "60%",
		},
	],
}));

const chartOptions = computed(() => ({
	responsive: true,
	maintainAspectRatio: false,
	plugins: {
		legend: {
			position: "bottom",
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
