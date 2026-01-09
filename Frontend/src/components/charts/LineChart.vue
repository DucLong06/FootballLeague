<template>
	<Line :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { computed } from "vue";
import { Line } from "vue-chartjs";
import {
	Chart as ChartJS,
	CategoryScale,
	LinearScale,
	PointElement,
	LineElement,
	Title,
	Tooltip,
	Legend,
	Filler,
} from "chart.js";

ChartJS.register(
	CategoryScale,
	LinearScale,
	PointElement,
	LineElement,
	Title,
	Tooltip,
	Legend,
	Filler
);

const props = defineProps({
	labels: {
		type: Array,
		required: true,
	},
	datasets: {
		type: Array,
		required: true,
	},
	title: {
		type: String,
		default: "",
	},
});

const chartData = computed(() => ({
	labels: props.labels,
	datasets: props.datasets.map((ds, index) => ({
		label: ds.label,
		data: ds.data,
		borderColor: ds.color || `hsl(${index * 60}, 70%, 50%)`,
		backgroundColor: ds.color
			? `${ds.color}20`
			: `hsla(${index * 60}, 70%, 50%, 0.2)`,
		fill: ds.fill || false,
		tension: 0.4,
		pointRadius: 4,
		pointHoverRadius: 6,
	})),
}));

const chartOptions = computed(() => ({
	responsive: true,
	maintainAspectRatio: false,
	plugins: {
		legend: {
			display: props.datasets.length > 1,
			labels: {
				color: "#9ca3af",
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
	scales: {
		x: {
			grid: {
				color: "rgba(255, 255, 255, 0.1)",
			},
			ticks: {
				color: "#9ca3af",
			},
		},
		y: {
			grid: {
				color: "rgba(255, 255, 255, 0.1)",
			},
			ticks: {
				color: "#9ca3af",
			},
		},
	},
}));
</script>
