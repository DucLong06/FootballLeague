<script setup>
import AppHeader from "./components/common/AppHeader.vue";
import AppFooter from "./components/common/AppFooter.vue";
</script>

<template>
	<div class="app">
		<AppHeader />
		<main class="main-content">
			<router-view />
		</main>
		<AppFooter />
	</div>
</template>

<style>
/* Global Styles */
:root {
	--color-primary: #10b981;
	--color-primary-dark: #059669;
	--color-accent: #f59e0b;
	--color-csoc: #1e40af;
	--color-csoc-light: #3b82f6;
	--color-bg: #0f172a;
	--color-bg-secondary: #1e293b;
	--color-text: #f1f5f9;
	--color-text-muted: #94a3b8;
}

* {
	box-sizing: border-box;
}

html {
	font-size: 16px;
}

body {
	margin: 0;
	padding: 0;
	font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
		sans-serif;
	background: var(--color-bg);
	color: var(--color-text);
	line-height: 1.6;
	min-height: 100vh;
}

#app {
	min-height: 100vh;
}

.app {
	display: flex;
	flex-direction: column;
	min-height: 100vh;
}

.main-content {
	flex: 1;
	padding-top: 64px; /* Header height */
}

/* Scrollbar Styling */
::-webkit-scrollbar {
	width: 8px;
	height: 8px;
}

::-webkit-scrollbar-track {
	background: var(--color-bg-secondary);
}

::-webkit-scrollbar-thumb {
	background: #4b5563;
	border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
	background: #6b7280;
}

/* Selection */
::selection {
	background: var(--color-primary);
	color: white;
}

/* Link Styles */
a {
	color: var(--color-primary);
	text-decoration: none;
	transition: color 0.2s;
}

a:hover {
	color: var(--color-primary-dark);
}

/* Focus Styles */
:focus-visible {
	outline: 2px solid var(--color-primary);
	outline-offset: 2px;
}

/* Utility Classes */
.text-center {
	text-align: center;
}

.text-muted {
	color: var(--color-text-muted);
}

/* CSOC Brand Gradient */
.csoc-gradient {
	background: linear-gradient(135deg, #1e40af, #10b981);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
}
</style>
