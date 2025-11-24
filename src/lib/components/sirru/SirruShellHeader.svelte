<script lang="ts">
	import { getContext } from 'svelte';
	import { page } from '$app/stores';
	import { user, showSettings, showSearch } from '$lib/stores';
	import SirruLogo from './SirruLogo.svelte';
	import SirruGlobalSearch from './SirruGlobalSearch.svelte';

	const i18n = getContext('i18n');

	export let currentApp: 'home' | 'chat' | 'docs' | 'presentations' = 'home';
	export let organization: { name: string; logo?: string } | null = null;

	let searchOpen = false;

	const navItems = [
		{ id: 'home', label: 'Home', href: '/home', icon: 'home' },
		{ id: 'chat', label: 'Chat AI', href: '/', icon: 'chat' },
		{ id: 'docs', label: 'Docs AI', href: '/docs', icon: 'docs' },
		{ id: 'presentations', label: 'Slides AI', href: '/presentations', icon: 'slides' }
	];
</script>

<header class="sirru-header">
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
		<div class="flex items-center justify-between h-16">
			<!-- Left: Logo & Org -->
			<div class="flex items-center gap-4">
				<a href="/home" class="flex items-center">
					<SirruLogo size="md" showText={true} />
				</a>

				{#if organization}
					<div class="hidden sm:flex items-center">
						<span class="text-gray-300 dark:text-gray-600 mx-3">|</span>
						<div class="sirru-org-badge">
							{#if organization.logo}
								<img src={organization.logo} alt={organization.name} class="w-5 h-5 rounded" />
							{/if}
							<span>{organization.name}</span>
						</div>
					</div>
				{/if}
			</div>

			<!-- Center: Navigation (Desktop) -->
			<nav class="hidden md:flex items-center gap-1">
				{#each navItems as item}
					<a
						href={item.href}
						class="sirru-nav-item {currentApp === item.id ? 'active' : ''}"
					>
						{#if item.icon === 'home'}
							<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
							</svg>
						{:else if item.icon === 'chat'}
							<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
							</svg>
						{:else if item.icon === 'docs'}
							<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
							</svg>
						{:else if item.icon === 'slides'}
							<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
							</svg>
						{/if}
						<span>{item.label}</span>
					</a>
				{/each}
			</nav>

			<!-- Right: Search & User -->
			<div class="flex items-center gap-3">
				<!-- Global Search Button -->
				<button
					class="p-2 rounded-lg text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
					on:click={() => showSearch.set(true)}
					title="Search (Ctrl+K)"
				>
					<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
					</svg>
				</button>

				<!-- Settings -->
				<button
					class="p-2 rounded-lg text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
					on:click={() => showSettings.set(true)}
					title="Settings"
				>
					<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
						<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
					</svg>
				</button>

				<!-- User Menu -->
				{#if $user}
					<button
						class="flex items-center gap-2 p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
						on:click={() => showSettings.set(true)}
					>
						<img
							src={$user.profile_image_url}
							alt={$user.name}
							class="w-8 h-8 rounded-full object-cover border-2 border-gray-200 dark:border-gray-700"
						/>
						<span class="hidden sm:block text-sm font-medium text-gray-700 dark:text-gray-300">
							{$user.name}
						</span>
					</button>
				{/if}
			</div>
		</div>
	</div>

	<!-- Mobile Navigation -->
	<div class="md:hidden border-t border-gray-200 dark:border-gray-800">
		<div class="flex justify-around py-2">
			{#each navItems as item}
				<a
					href={item.href}
					class="flex flex-col items-center gap-1 px-3 py-2 rounded-lg transition-colors {currentApp === item.id ? 'text-sirru-primary-600 dark:text-sirru-primary-400' : 'text-gray-500 dark:text-gray-400'}"
				>
					{#if item.icon === 'home'}
						<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
						</svg>
					{:else if item.icon === 'chat'}
						<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
						</svg>
					{:else if item.icon === 'docs'}
						<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
						</svg>
					{:else if item.icon === 'slides'}
						<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
						</svg>
					{/if}
					<span class="text-xs">{item.label}</span>
				</a>
			{/each}
		</div>
	</div>
</header>
