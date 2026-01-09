<template>
	<footer class="app-footer">
		<div class="footer-container">
			<div class="footer-content">
				<div class="footer-logo">
					<span>⚽</span>
					<span>CSOC Football</span>
				</div>
				<div class="footer-links">
					<router-link to="/">Tổng quan</router-link>
					<router-link to="/standings">BXH</router-link>
					<router-link to="/players">Cầu thủ</router-link>
					<router-link to="/matches">Trận đấu</router-link>
				</div>
			</div>
			<p class="copyright">© {{ currentYear }} CSOC Football</p>
		</div>
	</footer>
</template>

<script setup>
const currentYear = new Date().getFullYear();
</script>

<style scoped>
.app-footer {
	background: rgba(17, 24, 39, 0.95);
	border-top: 1px solid rgba(30, 64, 175, 0.3);
	padding: 1.5rem 0;
	margin-top: auto;
}

.footer-container {
	max-width: 1400px;
	margin: 0 auto;
	padding: 0 1rem;
	text-align: center;
}

.footer-content {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 1rem;
	flex-wrap: wrap;
	gap: 1rem;
}

.footer-logo {
	display: flex;
	align-items: center;
	gap: 0.5rem;
	font-weight: 700;
	background: linear-gradient(135deg, #1e40af, #10b981);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
}

.footer-links {
	display: flex;
	gap: 1.5rem;
	flex-wrap: wrap;
}

.footer-links a {
	color: #9ca3af;
	text-decoration: none;
	font-size: 0.875rem;
	transition: color 0.2s;
}

.footer-links a:hover {
	color: #10b981;
}

.copyright {
	font-size: 0.75rem;
	color: #6b7280;
	margin: 0;
}

@media (max-width: 640px) {
	.footer-content {
		flex-direction: column;
	}

	.footer-links {
		gap: 1rem;
		justify-content: center;
	}
}
</style>
