<script lang="ts">
	export let size: 'sm' | 'md' | 'lg' | 'xl' = 'md';
	export let showText = true;
	export let className = '';

	const sizeClasses = {
		sm: 'w-6 h-6',
		md: 'w-8 h-8',
		lg: 'w-10 h-10',
		xl: 'w-12 h-12'
	};

	const textSizeClasses = {
		sm: 'text-lg',
		md: 'text-xl',
		lg: 'text-2xl',
		xl: 'text-3xl'
	};
</script>

<div class="sirru-logo flex items-center gap-2 {className}">
	<!-- Sirru Icon - African-inspired abstract mark -->
	<svg
		viewBox="0 0 48 48"
		class={sizeClasses[size]}
		fill="none"
		xmlns="http://www.w3.org/2000/svg"
	>
		<!-- Background circle with gradient -->
		<defs>
			<linearGradient id="sirruGradient" x1="0%" y1="0%" x2="100%" y2="100%">
				<stop offset="0%" style="stop-color:#16a34a" />
				<stop offset="50%" style="stop-color:#15803d" />
				<stop offset="100%" style="stop-color:#166534" />
			</linearGradient>
			<linearGradient id="goldAccent" x1="0%" y1="0%" x2="100%" y2="100%">
				<stop offset="0%" style="stop-color:#fde047" />
				<stop offset="100%" style="stop-color:#eab308" />
			</linearGradient>
		</defs>

		<!-- Main circle -->
		<circle cx="24" cy="24" r="22" fill="url(#sirruGradient)" />

		<!-- African-inspired abstract pattern - represents growth, connectivity, and sovereignty -->
		<!-- Central diamond/rhombus - symbolizes strength -->
		<path
			d="M24 10 L34 24 L24 38 L14 24 Z"
			fill="none"
			stroke="url(#goldAccent)"
			stroke-width="2.5"
			stroke-linejoin="round"
		/>

		<!-- Inner connecting lines - represent network/connection -->
		<path
			d="M24 14 L30 24 L24 34 L18 24 Z"
			fill="rgba(255,255,255,0.15)"
			stroke="white"
			stroke-width="1.5"
			stroke-linejoin="round"
		/>

		<!-- Central dot - represents unity -->
		<circle cx="24" cy="24" r="3" fill="url(#goldAccent)" />

		<!-- Radiating lines - represent growth -->
		<path
			d="M24 6 L24 10 M24 38 L24 42 M6 24 L10 24 M38 24 L42 24"
			stroke="rgba(255,255,255,0.4)"
			stroke-width="2"
			stroke-linecap="round"
		/>
	</svg>

	{#if showText}
		<span class="font-sirru-display font-bold tracking-tight {textSizeClasses[size]} text-gray-900 dark:text-white">
			Sirru
		</span>
	{/if}
</div>
