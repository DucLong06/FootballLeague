<template>
	<Bar :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { computed } from "vue";
import { Bar } from "vue-chartjs";
import {
	Chart as ChartJS,
	CategoryScale,
	LinearScale,
	BarElement,
	Title,
	Tooltip,
	Legend,
} from "chart.js";

ChartJS.register(
	CategoryScale,
	LinearScale,
	BarElement,
	Title,
	Tooltip,
	Legend
);

const props = defineProps({
	labels: {
		type: Array,
		required: true,
	},
	data: {
		type: Array,
		required: true,
	},
	label: {
		type: String,
		default: "Data",
	},
	backgroundColor: {
		type: String,
		default: "rgba(16, 185, 129, 0.8)",
	},
	horizontal: {
		type: Boolean,
		default: true,
	},
	title: {
		type: String,
		default: "",
	},
});

const chartData = computed(() => ({
	labels: props.labels,
	datasets: [
		{
			label: props.label,
			data: props.data,
			backgroundColor: props.backgroundColor,
			borderRadius: 4,
		},
	],
}));

const chartOptions = computed(() => ({
	indexAxis: props.horizontal ? "y" : "x",
	responsive: true,
	maintainAspectRatio: false,
	plugins: {
		legend: {
			display: false,
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
