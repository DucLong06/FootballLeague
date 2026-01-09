<template>
	<header class="app-header">
		<div class="header-container">
			<router-link to="/" class="logo">
				<span class="logo-icon">⚽</span>
				<span class="logo-text">CSOC Football</span>
			</router-link>

			<nav class="nav-menu">
				<router-link
					to="/"
					class="nav-link"
					exact-active-class="active"
				>
					<span class="nav-icon">🏠</span>
					<span class="nav-text">Tổng quan</span>
				</router-link>
				<router-link
					to="/standings"
					class="nav-link"
					active-class="active"
				>
					<span class="nav-icon">🏆</span>
					<span class="nav-text">BXH</span>
				</router-link>
				<router-link
					to="/players"
					class="nav-link"
					active-class="active"
				>
					<span class="nav-icon">👥</span>
					<span class="nav-text">Cầu thủ</span>
				</router-link>
				<router-link
					to="/matches"
					class="nav-link"
					active-class="active"
				>
					<span class="nav-icon">📅</span>
					<span class="nav-text">Trận đấu</span>
				</router-link>
			</nav>

			<div class="header-actions">
				<a href="/admin/" target="_blank" class="admin-link">
					⚙️ Admin
				</a>
			</div>
		</div>
	</header>
</template>

<style scoped>
.app-header {
	position: fixed;
	top: 0;
	left: 0;
	right: 0;
	z-index: 100;
	background: rgba(17, 24, 39, 0.98);
	backdrop-filter: blur(10px);
	border-bottom: 1px solid rgba(30, 64, 175, 0.3);
}

.header-container {
	max-width: 1400px;
	margin: 0 auto;
	padding: 0 1rem;
	height: 56px;
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1rem;
}

.logo {
	display: flex;
	align-items: center;
	gap: 0.5rem;
	text-decoration: none;
	color: #fff;
	flex-shrink: 0;
}

.logo-icon {
	font-size: 1.5rem;
}

.logo-text {
	font-size: 1.125rem;
	font-weight: 700;
	background: linear-gradient(135deg, #1e40af, #10b981);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
}

.nav-menu {
	display: flex;
	align-items: center;
	gap: 0.25rem;
}

.nav-link {
	display: flex;
	align-items: center;
	gap: 0.375rem;
	padding: 0.5rem 0.75rem;
	border-radius: 8px;
	text-decoration: none;
	color: #9ca3af;
	font-weight: 500;
	transition: all 0.2s ease;
	white-space: nowrap;
}

.nav-link:hover {
	color: #fff;
	background: rgba(255, 255, 255, 0.1);
}

.nav-link.active {
	color: #10b981;
	background: rgba(16, 185, 129, 0.1);
}

.nav-icon {
	font-size: 1rem;
}

.nav-text {
	font-size: 0.875rem;
}

.header-actions {
	display: flex;
	align-items: center;
	flex-shrink: 0;
}

.admin-link {
	display: flex;
	align-items: center;
	gap: 0.375rem;
	padding: 0.5rem 0.75rem;
	background: rgba(59, 130, 246, 0.2);
	border: 1px solid rgba(59, 130, 246, 0.3);
	border-radius: 8px;
	color: #3b82f6;
	text-decoration: none;
	font-size: 0.875rem;
	font-weight: 500;
	transition: all 0.2s ease;
}

.admin-link:hover {
	background: rgba(59, 130, 246, 0.3);
}

@media (max-width: 768px) {
	.nav-text {
		display: none;
	}

	.nav-link {
		padding: 0.5rem;
	}

	.logo-text {
		font-size: 1rem;
	}

	.admin-link {
		padding: 0.5rem;
	}

	.admin-link span:last-child {
		display: none;
	}
}
</style>
