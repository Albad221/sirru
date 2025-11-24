<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import type { SirruAppType } from '$lib/constants';

	export let app: SirruAppType;
	export let title: string;
	export let description: string;
	export let href: string;
	export let badge: string | null = null;
	export let disabled = false;

	const dispatch = createEventDispatcher();

	const appConfig = {
		chat: {
			icon: 'chat',
			color: 'sirru-primary',
			bgClass: 'sirru-app-card--chat'
		},
		docs: {
			icon: 'docs',
			color: 'blue',
			bgClass: 'sirru-app-card--docs'
		},
		presentations: {
			icon: 'presentations',
			color: 'purple',
			bgClass: 'sirru-app-card--presentations'
		}
	};

	$: config = appConfig[app];
</script>

<a
	{href}
	class="sirru-app-card {config.bgClass} block cursor-pointer {disabled ? 'opacity-50 pointer-events-none' : ''}"
	on:click={() => dispatch('click')}
	aria-disabled={disabled}
>
	<div class="relative z-10">
		<!-- App Icon -->
		<div class="mb-4">
			{#if app === 'chat'}
				<div class="w-12 h-12 rounded-xl bg-sirru-primary-100 dark:bg-sirru-primary-900/30 flex items-center justify-center">
					<svg class="w-6 h-6 text-sirru-primary-600 dark:text-sirru-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
					</svg>
				</div>
			{:else if app === 'docs'}
				<div class="w-12 h-12 rounded-xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
					<svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
					</svg>
				</div>
			{:else if app === 'presentations'}
				<div class="w-12 h-12 rounded-xl bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
					<svg class="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
					</svg>
				</div>
			{/if}
		</div>

		<!-- Title & Badge -->
		<div class="flex items-center gap-2 mb-2">
			<h3 class="text-lg font-semibold text-gray-900 dark:text-white">
				{title}
			</h3>
			{#if badge}
				<span class="sirru-badge {app === 'chat' ? 'sirru-badge-success' : app === 'docs' ? 'sirru-badge-info' : 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400'}">
					{badge}
				</span>
			{/if}
		</div>

		<!-- Description -->
		<p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
			{description}
		</p>

		<!-- Launch Button -->
		<div class="flex items-center text-sm font-medium {app === 'chat' ? 'text-sirru-primary-600 dark:text-sirru-primary-400' : app === 'docs' ? 'text-blue-600 dark:text-blue-400' : 'text-purple-600 dark:text-purple-400'}">
			<span>Launch</span>
			<svg class="w-4 h-4 ml-1 transition-transform group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
			</svg>
		</div>
	</div>
</a>
